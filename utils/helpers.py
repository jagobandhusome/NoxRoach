"""
Helper Functions
Common utility functions
"""

import os
import sys
import time
import random
import socket
import platform
from datetime import datetime
import logging

def get_system_info():
    """Get system information"""
    return {
        'hostname': socket.gethostname(),
        'ip': socket.gethostbyname(socket.gethostname()),
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'username': os.getlogin(),
        'timestamp': datetime.now().isoformat()
    }

def random_delay(min_sec=0.1, max_sec=2.0):
    """Add random delay"""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def ensure_directory(path):
    """Ensure directory exists"""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def is_admin():
    """Check if running as administrator"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch with admin privileges"""
    if not is_admin():
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

def chunk_data(data, chunk_size=1000):
    """Split data into chunks"""
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]

def get_timestamp():
    """Get timestamp string"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def safe_filename(filename):
    """Make filename safe"""
    return "".join(c for c in filename if c.isalnum() or c in "._- ").strip()