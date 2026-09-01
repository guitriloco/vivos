import json
import time
import logging
import threading
import queue
import os
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import ijson
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProcessingState(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"

@dataclass
class ProcessingCheckpoint:
    """Persistent state object for tracking processing progress"""
    job_id: str
    dataset_path: str
    current_offset: int
    processed_records: int
    total_records: int
    last_processed_timestamp: float
    state: ProcessingState
    module_name: str
    checkpoint_file: str

    def to_dict(self):
        d = asdict(self)
        d['state'] = self.state.value
        d['last_processed_timestamp'] = self.last_processed_timestamp
        return d

    @classmethod
    def from_dict(cls, data: dict):
        data['state'] = ProcessingState(data['state'])
        return cls(**data)

class CircuitBreaker:
    """Circuit breaker pattern for network resilience"""
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self._lock = threading.Lock()

    def call(self, func, *args, **kwargs):
        with self._lock:
            if self.is_open():
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e

    def is_open(self):
        if self.failure_count >= self.failure_threshold:
            if time.time() - self.last_failure_time < self.timeout:
                return True
            else:
                # Reset after timeout
                self.failure_count = 0
        return False

    def on_success(self):
        self.failure_count = 0

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

class NetworkResilienceWrapper:
    """Wrapper for resilient API calls with retry logic and circuit breaker"""
    def __init__(self, max_retries=3, backoff_factor=0.3, circuit_breaker=None):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.circuit_breaker = circuit_breaker or CircuitBreaker()

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, url, **kwargs):
        def _get():
            return self.session.get(url, **kwargs)
        return self.circuit_breaker.call(_get)

    def post(self, url, **kwargs):
        def _post():
            return self.session.post(url, **kwargs)
        return self.circuit_breaker.call(_post)

class StreamProcessor:
    """Memory-efficient stream processor using ijson for TB+ scale datasets"""
    def __init__(self, checkpoint_manager):
        self.checkpoint_manager = checkpoint_manager

    def process_json_stream(self, file_path: str, transform_func: Callable, chunk_size: int = 8192):
        """
        Process large JSON files with constant memory usage
        Handles both JSON arrays and JSONL (JSON Lines) formats
        """
        processed_count = 0

        # Determine if the file is in JSONL format (one JSON object per line)
        # or a JSON array by checking the first character
        with open(file_path, 'r', encoding='utf-8') as f:
            first_char = f.read(1)
            f.seek(0)

            if first_char == '[':  # JSON array format
                processed_count = self._process_json_array(file_path, transform_func)
            elif first_char == '{':  # Likely JSONL format (first char of an object)
                processed_count = self._process_json_lines(file_path, transform_func)

        return processed_count

    def _process_json_array(self, file_path: str, transform_func: Callable):
        """Process a JSON file containing an array of objects"""
        processed_count = 0

        with open(file_path, 'rb') as file:
            # Parse items from the array
            try:
                parser = ijson.items(file, 'item')

                for record in parser:
                    try:
                        # Apply transformation
                        transformed_record = transform_func(record)

                        # Update checkpoint periodically
                        processed_count += 1
                        if processed_count % 1000 == 0:  # Update every 1000 records
                            self.checkpoint_manager.update_checkpoint(
                                current_offset=file.tell(),
                                processed_records=processed_count
                            )

                    except Exception as e:
                        logger.error(f"Error processing record #{processed_count + 1}: {e}")
                        continue

            except Exception as e:
                logger.error(f"Error parsing JSON array: {e}")

        return processed_count

    def _process_json_lines(self, file_path: str, transform_func: Callable):
        """Process a JSONL file (one JSON object per line)"""
        processed_count = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    import json
                    record = json.loads(line)

                    # Apply transformation
                    transformed_record = transform_func(record)

                    # Update checkpoint periodically
                    processed_count += 1
                    if processed_count % 1000 == 0:  # Update every 1000 records
                        # For JSONL, we can't easily track byte offset, so we'll just update record count
                        self.checkpoint_manager.update_checkpoint(
                            processed_records=processed_count
                        )

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON on line {line_num + 1}: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Error processing record on line {line_num + 1}: {e}")
                    continue

        return processed_count

class CheckpointManager:
    """Manages persistent state checkpoints"""
    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.checkpoint_dir = checkpoint_dir
        os.makedirs(checkpoint_dir, exist_ok=True)

    def save_checkpoint(self, checkpoint: ProcessingCheckpoint):
        """Save checkpoint to persistent storage"""
        file_path = os.path.join(self.checkpoint_dir, f"{checkpoint.job_id}.json")
        with open(file_path, 'w') as f:
            json.dump(checkpoint.to_dict(), f, indent=2)
        logger.info(f"Checkpoint saved: {file_path}")

    def load_checkpoint(self, job_id: str) -> Optional[ProcessingCheckpoint]:
        """Load checkpoint from persistent storage"""
        file_path = os.path.join(self.checkpoint_dir, f"{job_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Checkpoint loaded: {file_path}")
            return ProcessingCheckpoint.from_dict(data)
        return None

    def update_checkpoint(self, job_id: str, **kwargs):
        """Update existing checkpoint with new values"""
        checkpoint = self.load_checkpoint(job_id)
        if checkpoint:
            for key, value in kwargs.items():
                if hasattr(checkpoint, key):
                    setattr(checkpoint, key, value)
            self.save_checkpoint(checkpoint)

    def delete_checkpoint(self, job_id: str):
        """Delete checkpoint file"""
        file_path = os.path.join(self.checkpoint_dir, f"{job_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Checkpoint deleted: {file_path}")

class PluginLoader:
    """Dynamic plugin loader for transformation modules"""
    def __init__(self, plugins_dir: str = "./plugins"):
        self.plugins_dir = plugins_dir
        os.makedirs(plugins_dir, exist_ok=True)

    def load_plugin(self, module_name: str) -> Callable:
        """Dynamically load a transformation module"""
        module_path = os.path.join(self.plugins_dir, f"{module_name}.py")

        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Plugin module not found: {module_path}")

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Assume the module has a 'transform' function
        if hasattr(module, 'transform'):
            logger.info(f"Plugin loaded: {module_name}")
            return module.transform
        else:
            raise AttributeError(f"Module {module_name} does not have a 'transform' function")

    def list_available_plugins(self) -> List[str]:
        """List all available plugin modules"""
        plugins = []
        for file in os.listdir(self.plugins_dir):
            if file.endswith('.py') and file != '__init__.py':
                plugins.append(file[:-3])  # Remove .py extension
        return plugins

class HEDPOrchestrator:
    """Main orchestrator for high-efficiency data processing"""
    def __init__(self, checkpoint_dir: str = "./checkpoints", plugins_dir: str = "./plugins"):
        self.checkpoint_manager = CheckpointManager(checkpoint_dir)
        self.plugin_loader = PluginLoader(plugins_dir)
        self.stream_processor = StreamProcessor(self.checkpoint_manager)
        self.network_wrapper = NetworkResilienceWrapper()

        # Thread-safe queues for job management
        self.job_queue = queue.Queue()
        self.result_queue = queue.Queue()

    def submit_job(self, job_config: Dict[str, Any]):
        """Submit a new processing job"""
        job_id = job_config.get('job_id', f"job_{int(time.time())}")

        # Create initial checkpoint
        checkpoint = ProcessingCheckpoint(
            job_id=job_id,
            dataset_path=job_config['dataset_path'],
            current_offset=0,
            processed_records=0,
            total_records=job_config.get('total_records', 0),
            last_processed_timestamp=time.time(),
            state=ProcessingState.PENDING,
            module_name=job_config['module_name'],
            checkpoint_file=f"{job_id}.json"
        )

        self.checkpoint_manager.save_checkpoint(checkpoint)

        # Add to job queue
        self.job_queue.put({
            'job_id': job_id,
            'config': job_config,
            'checkpoint': checkpoint
        })

        logger.info(f"Job submitted: {job_id}")
        return job_id

    def resume_job_from_checkpoint(self, job_id: str):
        """Resume a job from its last checkpoint"""
        checkpoint = self.checkpoint_manager.load_checkpoint(job_id)
        if not checkpoint:
            raise ValueError(f"No checkpoint found for job: {job_id}")

        if checkpoint.state == ProcessingState.COMPLETED:
            logger.info(f"Job {job_id} already completed")
            return

        # Update state to in progress
        checkpoint.state = ProcessingState.IN_PROGRESS
        self.checkpoint_manager.save_checkpoint(checkpoint)

        # Load transformation module
        transform_func = self.plugin_loader.load_plugin(checkpoint.module_name)

        # Process from checkpoint offset
        processed_count = self.stream_processor.process_json_stream(
            checkpoint.dataset_path,
            transform_func
        )

        # Update final state
        checkpoint.state = ProcessingState.COMPLETED
        checkpoint.processed_records = processed_count
        self.checkpoint_manager.save_checkpoint(checkpoint)

        logger.info(f"Job completed: {job_id}, processed {processed_count} records")
        return processed_count

    def process_jobs(self):
        """Process jobs from the queue"""
        while True:
            try:
                job_data = self.job_queue.get(timeout=1)
                job_id = job_data['job_id']

                logger.info(f"Starting job: {job_id}")
                self.resume_job_from_checkpoint(job_id)

                self.job_queue.task_done()
            except queue.Empty:
                time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Shutting down orchestrator...")
                break