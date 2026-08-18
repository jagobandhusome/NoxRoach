"""
Logging Utilities
Custom logging configuration
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging(config=None):
    """Setup logging configuration"""
    
    # Default config
    default_config = {
        'log_level': 'INFO',
        'log_file': 'analysis.log',
        'max_size_mb': 10,
        'backup_count': 5
    }
    
    if config:
        default_config.update(config)
    
    # Convert level
    log_level = getattr(logging, default_config['log_level'].upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup file handler with rotation
    log_dir = os.path.dirname(default_config['log_file'])
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        default_config['log_file'],
        maxBytes=default_config['max_size_mb'] * 1024 * 1024,
        backupCount=default_config['backup_count']
    )
    file_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger

class Logger:
    """Custom logger with additional features"""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def success(self, message):
        self.logger.info(f"✓ {message}")
    
    def failure(self, message):
        self.logger.error(f"✗ {message}")
    
    def highlight(self, message):
        self.logger.warning(f"★ {message}")