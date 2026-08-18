"""
Enhanced Detection Module
Implements pattern detection and anomaly detection
"""

import re
import json
from datetime import datetime
from collections import defaultdict
import logging

class EnhancedDetector:
    def __init__(self, analysis_dir):
        self.analysis_dir = analysis_dir
        self.threats = []
        self.patterns = {
            'credential_harvesting': {
                'regex': r'(password|pass|login|username|email|user|admin|token|secret)',
                'severity': 8
            },
            'financial_data': {
                'regex': r'(credit\s*card|card\s*number|ccv|cvv|ssn|social\s*security|bank|account|routing)',
                'severity': 9
            },
            'system_commands': {
                'regex': r'(cmd|powershell|regedit|msconfig|taskkill|netstat|ipconfig)',
                'severity': 6
            },
            'url_pattern': {
                'regex': r'(https?://[^\s]+|www\.[^\s]+)',
                'severity': 5
            },
            'email_pattern': {
                'regex': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
                'severity': 7
            }
        }
        
        self.anomaly_threshold = 2.0
        self.baseline = {
            'typing_speed': 50,
            'key_pause': 0.2,
            'typing_variance': 0.1
        }
        
        logging.info("[*] Enhanced Detector initialized")
    
    def analyze(self, keystroke_stream):
        """Analyze keystroke stream for threats"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'threats': [],
            'anomalies': [],
            'risk_score': 0
        }
        
        # Pattern detection
        pattern_results = self._detect_patterns(keystroke_stream)
        if pattern_results['threats']:
            results['threats'].extend(pattern_results['threats'])
        
        # Anomaly detection
        anomaly_results = self._detect_anomalies(keystroke_stream)
        if anomaly_results['anomalies']:
            results['anomalies'].extend(anomaly_results['anomalies'])
        
        # Calculate risk score
        results['risk_score'] = self._calculate_risk(results)
        
        return results
    
    def _detect_patterns(self, stream):
        """Detect patterns in keystroke stream"""
        results = {
            'threats': [],
            'severity': 0
        }
        
        # Convert to string
        text = self._keystrokes_to_text(stream)
        
        # Check each pattern
        for pattern_name, pattern_data in self.patterns.items():
            matches = re.finditer(pattern_data['regex'], text, re.IGNORECASE)
            
            for match in matches:
                threat = {
                    'type': pattern_name,
                    'matched': match.group(),
                    'position': match.span(),
                    'severity': pattern_data['severity'],
                    'timestamp': datetime.now().isoformat()
                }
                results['threats'].append(threat)
                results['severity'] = max(results['severity'], pattern_data['severity'])
                
                logging.warning(f"[!] Threat detected: {pattern_name} - {match.group()}")
        
        self.threats.extend(results['threats'])
        return results
    
    def _detect_anomalies(self, stream):
        """Detect behavioral anomalies"""
        results = {
            'anomalies': [],
            'anomaly_score': 0
        }
        
        if len(stream) < 5:
            return results
        
        # Calculate statistics
        stats = self._calculate_stats(stream)
        
        # Check for anomalies
        anomalies = self._check_for_anomalies(stats)
        
        if anomalies:
            results['anomalies'] = anomalies
            results['anomaly_score'] = self._calculate_anomaly_score(anomalies)
        
        return results
    
    def _calculate_stats(self, stream):
        """Calculate statistical metrics"""
        stats = {
            'typing_speed': 0,
            'avg_pause': 0,
            'key_count': len(stream),
            'time_span': 0
        }
        
        if len(stream) < 2:
            return stats
        
        # Time calculations
        start_time = datetime.fromisoformat(stream[0]['timestamp'])
        end_time = datetime.fromisoformat(stream[-1]['timestamp'])
        time_span = (end_time - start_time).total_seconds()
        stats['time_span'] = time_span
        
        if time_span > 0:
            stats['typing_speed'] = (len(stream) / time_span) * 60
        
        # Pause calculations
        pauses = []
        for i in range(1, len(stream)):
            prev_time = datetime.fromisoformat(stream[i-1]['timestamp'])
            curr_time = datetime.fromisoformat(stream[i]['timestamp'])
            pause = (curr_time - prev_time).total_seconds()
            pauses.append(pause)
        
        if pauses:
            stats['avg_pause'] = sum(pauses) / len(pauses)
        
        return stats
    
    def _check_for_anomalies(self, stats):
        """Check for anomalies based on statistics"""
        anomalies = []
        
        # Check typing speed
        if stats['typing_speed'] > 0:
            deviation = abs(stats['typing_speed'] - self.baseline['typing_speed']) / self.baseline['typing_speed']
            if deviation > self.anomaly_threshold:
                anomalies.append({
                    'type': 'typing_speed',
                    'expected': self.baseline['typing_speed'],
                    'actual': stats['typing_speed'],
                    'deviation': deviation
                })
        
        # Check pause patterns
        if stats['avg_pause'] > 0:
            deviation = abs(stats['avg_pause'] - self.baseline['key_pause']) / self.baseline['key_pause']
            if deviation > self.anomaly_threshold:
                anomalies.append({
                    'type': 'key_pause',
                    'expected': self.baseline['key_pause'],
                    'actual': stats['avg_pause'],
                    'deviation': deviation
                })
        
        return anomalies
    
    def _calculate_anomaly_score(self, anomalies):
        """Calculate overall anomaly score"""
        score = 0
        for anomaly in anomalies:
            if anomaly['type'] == 'typing_speed':
                score += min(anomaly['deviation'] * 10, 30)
            elif anomaly['type'] == 'key_pause':
                score += min(anomaly['deviation'] * 10, 30)
        return min(score, 100)
    
    def _calculate_risk(self, results):
        """Calculate overall risk score"""
        risk = 0
        
        # From pattern detection
        if results['threats']:
            threat_severity = max(t['severity'] for t in results['threats'])
            risk += threat_severity * 5
        
        # From anomalies
        if results['anomalies']:
            risk += results.get('anomaly_score', 0) * 0.3
        
        return min(risk, 100)
    
    def _keystrokes_to_text(self, stream):
        """Convert keystrokes to text"""
        text = []
        for keystroke in stream:
            key = keystroke.get('key', '')
            if len(key) == 1 and key.isprintable():
                text.append(key)
        return ''.join(text)