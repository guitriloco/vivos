import time
import random
import logging
import requests
from typing import Optional, Dict
import json
import threading

class UserAgentRotator:
    """
    Rotates User-Agent headers to simulate different browser environments.
    Useful for legitimate stress-testing and data-mining projects.
    """

    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]

    def get_random_user_agent(self) -> str:
        """Returns a randomly selected user agent string."""
        return random.choice(self.user_agents)


class RateLimiter:
    """
    Implements rate limiting with Gaussian distribution to mimic human-like interactions.
    """

    def __init__(self, base_delay: float = 1.0, variance: float = 0.3):
        """
        Initializes the rate limiter.
        """
        self.base_delay = base_delay
        self.variance = variance
        self._lock = threading.Lock()

    def wait(self):
        """Waits for a randomized period based on Gaussian distribution."""
        with self._lock:
            delay = random.gauss(self.base_delay, self.variance)
            delay = max(0.1, delay)
            time.sleep(delay)


class CentralizedLogger:
    """
    Centralized logging system for HTTP errors and connection issues.
    """

    def __init__(self, log_file_path: str = "./error_log.txt"):
        """
        Initializes the logger.
        """
        self.log_file_path = log_file_path
        self._setup_logger()

    def _setup_logger(self):
        """Sets up the internal logger."""
        self.logger = logging.getLogger("RequestHandlerLogger")
        self.logger.setLevel(logging.ERROR)

        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_file_path, mode='a', encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_error(self, error_type: str, url: str, status_code: Optional[int] = None,
                  response_text: Optional[str] = None, additional_info: Optional[Dict] = None):
        """
        Logs an error to the centralized log file.
        """
        log_message = f"Error Type: {error_type} | URL: {url}"

        if status_code is not None:
            log_message += f" | Status Code: {status_code}"

        if response_text is not None:
            truncated_response = response_text[:200] + "..." if len(response_text) > 200 else response_text
            log_message += f" | Response: {truncated_response}"

        if additional_info:
            log_message += f" | Additional Info: {json.dumps(additional_info)}"

        self.logger.error(log_message)

    def log_http_error(self, url: str, status_code: int, response_text: Optional[str] = None):
        """Logs HTTP errors specifically."""
        error_type = f"HTTP_{status_code}"
        self.log_error(error_type, url, status_code, response_text)

    def log_connection_error(self, url: str, error_message: str):
        """Logs connection errors."""
        self.log_error("ConnectionError", url, additional_info={"error_message": error_message})


class RequestHandler:
    """
    Main request handler that combines User-Agent rotation, rate limiting, and centralized logging.
    """

    def __init__(self,
                 base_delay: float = 1.0,
                 variance: float = 0.3,
                 log_file_path: str = "./error_log.txt",
                 timeout: int = 30):
        """
        Initializes the request handler.
        """
        self.user_agent_rotator = UserAgentRotator()
        self.rate_limiter = RateLimiter(base_delay, variance)
        self.logger = CentralizedLogger(log_file_path)
        self.timeout = timeout
        self.session = requests.Session()

    def make_request(self,
                     method: str,
                     url: str,
                     custom_headers: Optional[Dict[str, str]] = None,
                     **kwargs) -> Optional[requests.Response]:
        """
        Makes an HTTP request with rotated User-Agent and rate limiting.
        """
        # Wait according to rate limiting
        self.rate_limiter.wait()

        # Prepare headers with rotated User-Agent
        headers = custom_headers or {}
        headers['User-Agent'] = self.user_agent_rotator.get_random_user_agent()

        try:
            # Make the request
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )

            # Log specific error codes
            if response.status_code == 403:
                self.logger.log_http_error(url, response.status_code, response.text[:500])
            elif response.status_code >= 500:
                # Log server errors as well
                self.logger.log_http_error(url, response.status_code, response.text[:500])

            return response

        except requests.exceptions.ConnectionError as e:
            self.logger.log_connection_error(url, str(e))
            return None
        except requests.exceptions.Timeout as e:
            self.logger.log_error("TimeoutError", url, additional_info={"timeout": self.timeout})
            return None
        except requests.exceptions.RequestException as e:
            self.logger.log_error("RequestException", url, additional_info={"error": str(e)})
            return None

    def get(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Optional[requests.Response]:
        """Makes a GET request."""
        return self.make_request('GET', url, headers, **kwargs)

    def post(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Optional[requests.Response]:
        """Makes a POST request."""
        return self.make_request('POST', url, headers, **kwargs)

    def put(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Optional[requests.Response]:
        """Makes a PUT request."""
        return self.make_request('PUT', url, headers, **kwargs)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None, **kwargs) -> Optional[requests.Response]:
        """Makes a DELETE request."""
        return self.make_request('DELETE', url, headers, **kwargs)

# Simple test
if __name__ == "__main__":
    print("Minimal RequestHandler module loaded successfully")
    handler = RequestHandler()
    print("RequestHandler initialized successfully")