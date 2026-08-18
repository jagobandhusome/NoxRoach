"""
Base Transmission Class
Defines interface for all transmission methods
"""

import zlib
import json
import base64
import time
import logging
from abc import ABC, abstractmethod

class BaseTransmission(ABC):
    """Base class for all transmission methods"""
    
    def __init__(self):
        self.compression_enabled = True
        self.retry_count = 3
        self.timeout = 30
        self.method_name = self.__class__.__name__
        
        logging.info(f"[*] {self.method_name} initialized")
    
    @abstractmethod
    def send(self, data):
        """Send data using this transmission method"""
        pass
    
    def prepare_data(self, data):
        """Prepare data for transmission"""
        # Convert to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Compress
        if self.compression_enabled:
            data = zlib.compress(data)
        
        # Encode for transmission
        return base64.b64encode(data).decode('utf-8')
    
    def retry_send(self, data, max_retries=None):
        """Send with retry logic"""
        max_retries = max_retries or self.retry_count
        
        for attempt in range(max_retries):
            try:
                result = self.send(data)
                if result:
                    logging.info(f"[✓] {self.method_name}: Send successful")
                    return True
            except Exception as e:
                logging.error(f"[X] {self.method_name}: Attempt {attempt+1} failed: {e}")
                
                # Exponential backoff
                wait_time = 2 ** attempt
                time.sleep(wait_time)
        
        logging.error(f"[X] {self.method_name}: All retries failed")
        return False
    
    def log_attempt(self, success, data_size):
        """Log transmission attempt"""
        status = "SUCCESS" if success else "FAILED"
        logging.info(f"[{self.method_name}] {status} - Size: {data_size} bytes")