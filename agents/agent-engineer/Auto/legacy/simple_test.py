import time
import random
import logging
import requests
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

    def get_random_user_agent(self):
        """Returns a randomly selected user agent string."""
        return random.choice(self.user_agents)


print("Module loaded successfully")
handler_rotator = UserAgentRotator()
print("UserAgentRotator initialized successfully")
print("Random UA:", handler_rotator.get_random_user_agent())