"""
Web Dashboard Module
Provides real-time visualization and monitoring
"""

from flask import Flask, render_template, jsonify
import json
import time
from datetime import datetime
import threading
import logging

class WebDashboard:
    def __init__(self, analysis_dir):
        self.analysis_dir = analysis_dir
        self.app = Flask(__name__)
        self.data = {
            'keystrokes': [],
            'threats': [],
            'stats': {
                'total_keystrokes': 0,
                'risk_level': 'LOW',
                'threats_detected': 0
            }
        }
        
        self._setup_routes()
        logging.info("[*] Web Dashboard initialized")
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html')
        
        @self.app.route('/api/data')
        def get_data():
            return jsonify(self.data)
        
        @self.app.route('/api/stats')
        def get_stats():
            return jsonify(self.data['stats'])
        
        @self.app.route('/api/keystrokes')
        def get_keystrokes():
            return jsonify(self.data['keystrokes'][-100:])
    
    def update_data(self, keystroke, threat=None):
        """Update dashboard data"""
        self.data['keystrokes'].append(keystroke)
        self.data['stats']['total_keystrokes'] += 1
        
        if threat:
            self.data['threats'].append(threat)
            self.data['stats']['threats_detected'] += 1
            
            # Update risk level
            if self.data['stats']['threats_detected'] > 10:
                self.data['stats']['risk_level'] = 'HIGH'
            elif self.data['stats']['threats_detected'] > 5:
                self.data['stats']['risk_level'] = 'MEDIUM'
        
        # Keep only last 1000 keystrokes
        if len(self.data['keystrokes']) > 1000:
            self.data['keystrokes'] = self.data['keystrokes'][-1000:]
    
    def run(self, host='127.0.0.1', port=5000):
        """Run the web dashboard"""
        logging.info(f"[*] Starting dashboard at http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False, use_reloader=False)