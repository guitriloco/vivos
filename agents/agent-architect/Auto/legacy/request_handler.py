import time
import random
import logging
import requests
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import json
import threading
from datetime import datetime

class UserAgentRotator:
    """
    Rotates User-Agent headers to simulate different browser environments.
    Useful for legitimate stress-testing and data-mining projects.
    """

    def __init__(self):
        self.user_agents = [
            # Chrome on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Firefox on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            # Safari on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            # Chrome on macOS
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Edge on Windows
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            # Chrome on Linux
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # Mobile - iPhone Safari
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            # Mobile - Android Chrome
            "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
        ]

    def get_random_user_agent(self) -> str:
        """Returns a randomly selected user agent string."""
        return random.choice(self.user_agents)

    def get_user_agent_with_custom(self, custom_ua: Optional[str] = None) -> str:
        """Returns either a custom user agent or a random one."""
        if custom_ua:
            return custom_ua
        return self.get_random_user_agent()


class RateLimiter:
    """
    Implements rate limiting with Gaussian distribution to mimic human-like interactions.
    Useful for legitimate stress-testing and data-mining projects.
    """

    def __init__(self, base_delay: float = 1.0, variance: float = 0.3):
        """
        Initializes the rate limiter.

        Args:
            base_delay: Base delay in seconds between requests
            variance: Variance for Gaussian distribution (higher = more randomness)
        """
        self.base_delay = base_delay
        self.variance = variance
        self._last_request_time = 0
        self._lock = threading.Lock()

    def wait(self):
        """Waits for a randomized period based on Gaussian distribution."""
        with self._lock:
            # Calculate delay using Gaussian distribution
            delay = random.gauss(self.base_delay, self.variance)

            # Ensure delay is positive
            delay = max(0.1, delay)

            # Sleep for the calculated delay
            time.sleep(delay)

    def wait_with_jitter(self, multiplier: float = 1.0):
        """Waits with additional jitter for more realistic timing."""
        with self._lock:
            # Calculate base delay with Gaussian distribution
            base_delay = random.gauss(self.base_delay, self.variance)

            # Add some jitter (random variation)
            jitter = random.uniform(-0.1, 0.1) * multiplier

            # Final delay with jitter
            delay = max(0.1, base_delay + jitter)

            time.sleep(delay)


class CentralizedLogger:
    """
    Centralized logging system for HTTP errors and connection issues.
    Logs to local files for diagnostic purposes in legitimate testing projects.
    """

    def __init__(self, log_file_path: str = "./error_log.txt"):
        """
        Initializes the logger.

        Args:
            log_file_path: Path to the log file
        """
        self.log_file_path = log_file_path
        self._setup_logger()

    def _setup_logger(self):
        """Sets up the internal logger."""
        self.logger = logging.getLogger("RequestHandlerLogger")
        self.logger.setLevel(logging.ERROR)

        # Prevent adding multiple handlers if called multiple times
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

        Args:
            error_type: Type of error (e.g., 'HTTP_403', 'ConnectionError')
            url: The URL that caused the error
            status_code: HTTP status code if applicable
            response_text: Response text if applicable
            additional_info: Additional information to log
        """
        log_message = f"Error Type: {error_type} | URL: {url}"

        if status_code is not None:
            log_message += f" | Status Code: {status_code}"

        if response_text is not None:
            # Truncate long response texts to prevent huge log files
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
    Designed for legitimate stress-testing and data-mining projects.
    """

    def __init__(self,
                 base_delay: float = 1.0,
                 variance: float = 0.3,
                 log_file_path: str = "./error_log.txt",
                 timeout: int = 30):
        """
        Initializes the request handler.

        Args:
            base_delay: Base delay between requests in seconds
            variance: Variance for Gaussian distribution
            log_file_path: Path for error logging
            timeout: Request timeout in seconds
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

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Target URL
            custom_headers: Custom headers to add/override
            **kwargs: Additional arguments to pass to requests

        Returns:
            requests.Response object or None if request failed
        """
        # Wait according to rate limiting
        self.rate_limiter.wait_with_jitter()

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


# Example usage and testing function
def example_usage():
    """
    Example of how to use the RequestHandler for legitimate testing purposes.
    """
    print("Initializing RequestHandler for legitimate testing...")

    # Initialize the handler
    handler = RequestHandler(
        base_delay=1.0,      # Average 1 second between requests
        variance=0.3,        # Some variation in timing
        log_file_path="./test_error_log.txt"
    )

    # Example of making requests
    urls_to_test = [
        "https://httpbin.org/user-agent",  # Returns the user agent
        "https://httpbin.org/status/200",  # Returns 200 status
        "https://httpbin.org/status/403",  # Returns 403 status (will be logged)
    ]

    for url in urls_to_test:
        print(f"Making request to: {url}")
        response = handler.get(url)

        if response:
            print(f"Response status: {response.status_code}")
            if response.status_code == 403:
                print("403 error was logged to error_log.txt")
        else:
            print("Request failed and was logged")

        print("---")

    print("Testing complete. Check test_error_log.txt for any logged errors.")


if __name__ == "__main__":
    example_usage()