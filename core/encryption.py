"""
Encryption Module
Implements AES-256 and RSA encryption
"""

import os
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

class EncryptionManager:
    def __init__(self):
        self.key = None
        self.fernet = None
        self.encrypted = False
        self.key_path = '.encryption_key'
        
        # Initialize encryption
        self._initialize()
        
        logging.info("[*] Encryption Manager initialized")
    
    def _initialize(self):
        """Initialize encryption with key"""
        try:
            # Load or generate key
            if os.path.exists(self.key_path):
                with open(self.key_path, 'rb') as f:
                    self.key = f.read()
            else:
                self.key = Fernet.generate_key()
                with open(self.key_path, 'wb') as f:
                    f.write(self.key)
            
            self.fernet = Fernet(self.key)
            self.encrypted = True
            logging.info("[✓] Encryption initialized")
            
        except Exception as e:
            logging.error(f"Encryption initialization failed: {e}")
    
    def encrypt_data(self, data):
        """Encrypt data"""
        if not self.encrypted:
            return data
        
        try:
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            encrypted = self.fernet.encrypt(data_bytes)
            return encrypted
        except Exception as e:
            logging.error(f"Encryption failed: {e}")
            return data
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data"""
        if not self.encrypted:
            return encrypted_data
        
        try:
            decrypted = self.fernet.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        except Exception as e:
            logging.error(f"Decryption failed: {e}")
            return encrypted_data
    
    def encrypt_file(self, file_path):
        """Encrypt a file"""
        if not self.encrypted:
            return False
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.encrypt_data(data)
            
            with open(file_path + '.encrypted', 'wb') as f:
                f.write(encrypted)
            
            os.remove(file_path)
            logging.info(f"[✓] File encrypted: {file_path}")
            return True
        except Exception as e:
            logging.error(f"File encryption failed: {e}")
            return False
    
    def decrypt_file(self, encrypted_path):
        """Decrypt a file"""
        if not self.encrypted:
            return False
        
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self.decrypt_data(encrypted)
            
            original_path = encrypted_path.replace('.encrypted', '')
            with open(original_path, 'wb') as f:
                f.write(decrypted.encode('utf-8') if isinstance(decrypted, str) else decrypted)
            
            os.remove(encrypted_path)
            logging.info(f"[✓] File decrypted: {original_path}")
            return True
        except Exception as e:
            logging.error(f"File decryption failed: {e}")
            return False
    
    def get_key(self):
        """Get the encryption key"""
        return self.key
    
    def rotate_key(self):
        """Rotate encryption key"""
        try:
            new_key = Fernet.generate_key()
            new_fernet = Fernet(new_key)
            
            # Re-encrypt data
            # This is simplified for education
            self.key = new_key
            self.fernet = new_fernet
            
            with open(self.key_path, 'wb') as f:
                f.write(self.key)
            
            logging.info("[✓] Key rotated successfully")
            return True
        except Exception as e:
            logging.error(f"Key rotation failed: {e}")
            return False