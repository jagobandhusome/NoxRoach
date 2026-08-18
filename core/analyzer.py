"""
Advanced Analysis Module
Implements behavioral and temporal analysis
"""

import re
import json
from datetime import datetime, timedelta
from collections import defaultdict
import logging

class AdvancedAnalyzer:
    def __init__(self, analysis_dir):
        self.analysis_dir = analysis_dir
        self.analysis_results = []
        self.behavioral_patterns = {
            'copy_paste': {'threshold': 0.8, 'description': 'Copy-paste detected'},
            'rapid_typing': {'threshold': 100, 'description': 'Unusual typing speed'},
            'hesitation': {'threshold': 2.0, 'description': 'Suspicious pauses'},
            'repetition': {'threshold': 0.3, 'description': 'Repetitive patterns'},
            'command_usage': {'threshold': 0.5, 'description': 'System commands'}
        }
        
        logging.info("[*] Advanced Analyzer initialized")
    
    def analyze(self, keystroke_stream):
        """Perform comprehensive analysis"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'behavioral': self._analyze_behavior(keystroke_stream),
            'temporal': self._analyze_temporal(keystroke_stream),
            'credential': self._detect_credentials(keystroke_stream),
            'risk_level': 'LOW'
        }
        
        # Calculate overall risk
        results['risk_level'] = self._calculate_risk_level(results)
        
        self.analysis_results.append(results)
        return results
    
    def _analyze_behavior(self, stream):
        """Analyze behavioral patterns"""
        if len(stream) < 5:
            return {'is_suspicious': False, 'behaviors': []}
        
        features = self._extract_features(stream)
        behaviors = []
        
        for behavior, config in self.behavioral_patterns.items():
            is_detected, score = self._check_behavior(behavior, features, config['threshold'])
            if is_detected:
                behaviors.append({
                    'type': behavior,
                    'description': config['description'],
                    'score': score
                })
        
        return {
            'is_suspicious': len(behaviors) > 0,
            'behaviors': behaviors,
            'behavior_score': sum(b['score'] for b in behaviors) / max(len(behaviors), 1)
        }
    
    def _extract_features(self, stream):
        """Extract behavioral features"""
        features = {
            'typing_speed': 0,
            'pause_lengths': [],
            'sequence_repeats': 0,
            'commands_detected': 0,
            'time_span': 0,
            'key_count': len(stream)
        }
        
        if len(stream) < 2:
            return features
        
        # Time features
        start_time = datetime.fromisoformat(stream[0]['timestamp'])
        end_time = datetime.fromisoformat(stream[-1]['timestamp'])
        time_span = (end_time - start_time).total_seconds()
        features['time_span'] = time_span
        
        if time_span > 0:
            features['typing_speed'] = (len(stream) / time_span) * 60
        
        # Pauses
        pauses = []
        for i in range(1, len(stream)):
            prev_time = datetime.fromisoformat(stream[i-1]['timestamp'])
            curr_time = datetime.fromisoformat(stream[i]['timestamp'])
            pause = (curr_time - prev_time).total_seconds()
            pauses.append(pause)
        features['pause_lengths'] = pauses
        
        # Command detection
        text = self._keystrokes_to_text(stream)
        commands = ['cmd', 'powershell', 'regedit', 'taskkill', 'netstat']
        text_lower = text.lower()
        features['commands_detected'] = sum(1 for cmd in commands if cmd in text_lower)
        
        return features
    
    def _check_behavior(self, behavior, features, threshold):
        """Check if behavior is detected"""
        if behavior == 'copy_paste':
            if features['typing_speed'] > 100 and features['time_span'] < 2:
                return True, 0.8
            return False, 0
        
        elif behavior == 'rapid_typing':
            if features['typing_speed'] > threshold and features['key_count'] > 10:
                return True, min(features['typing_speed'] / 150, 1)
            return False, 0
        
        elif behavior == 'hesitation':
            if features['pause_lengths'] and max(features['pause_lengths']) > threshold:
                return True, 0.7
            return False, 0
        
        elif behavior == 'repetition':
            repeat_ratio = features.get('sequence_repeats', 0) / max(features['key_count'], 1)
            if repeat_ratio > threshold:
                return True, min(repeat_ratio, 1)
            return False, 0
        
        elif behavior == 'command_usage':
            if features['commands_detected'] > threshold * 2:
                return True, 0.9
            return False, 0
        
        return False, 0
    
    def _analyze_temporal(self, stream):
        """Analyze temporal patterns"""
        results = {
            'is_time_based_risk': False,
            'activity_hours': {}
        }
        
        if not stream:
            return results
        
        # Hour distribution
        hour_count = defaultdict(int)
        for keystroke in stream:
            try:
                dt = datetime.fromisoformat(keystroke['timestamp'])
                hour_count[dt.hour] += 1
            except:
                continue
        
        results['activity_hours'] = dict(hour_count)
        
        # Check suspicious hours (midnight to 6 AM)
        suspicious_hours = [h for h in range(0, 6) if h in hour_count and hour_count[h] > 0]
        if suspicious_hours:
            results['is_time_based_risk'] = True
            logging.warning(f"[!] Suspicious activity during hours: {suspicious_hours}")
        
        return results
    
    def _detect_credentials(self, stream):
        """Detect credential-like patterns"""
        results = {
            'detected': False,
            'credentials': [],
            'sensitivity': 'low'
        }
        
        text = self._keystrokes_to_text(stream)
        
        # Credential patterns
        patterns = {
            'password': r'(?:pass(?:word|phrase)?|pwd)[=\s:]*([^\s\n]+)',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'credit_card': r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}',
            'ssn': r'\d{3}-\d{2}-\d{4}'
        }
        
        for cred_type, pattern in patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                results['credentials'].append({
                    'type': cred_type,
                    'value': match.group(1) if match.groups() else match.group(),
                    'position': match.span()
                })
                results['detected'] = True
        
        if results['credentials']:
            results['sensitivity'] = 'high' if any(c['type'] in ['password', 'credit_card'] for c in results['credentials']) else 'medium'
            logging.warning(f"[!] Credentials detected: {len(results['credentials'])} items")
        
        return results
    
    def _calculate_risk_level(self, results):
        """Calculate overall risk level"""
        risk_score = 0
        
        # Behavioral risk
        behavioral = results['behavioral']
        if behavioral.get('is_suspicious'):
            risk_score += 30
            risk_score += behavioral.get('behavior_score', 0) * 30
        
        # Temporal risk
        if results['temporal'].get('is_time_based_risk'):
            risk_score += 10
        
        # Credential risk
        if results['credential'].get('detected'):
            risk_score += 40
            if results['credential'].get('sensitivity') == 'high':
                risk_score += 20
        
        # Categorize
        if risk_score >= 70:
            return 'HIGH'
        elif risk_score >= 40:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _keystrokes_to_text(self, stream):
        """Convert keystrokes to text"""
        text = []
        for keystroke in stream:
            key = keystroke.get('key', '')
            if len(key) == 1 and key.isprintable():
                text.append(key)
        return ''.join(text)