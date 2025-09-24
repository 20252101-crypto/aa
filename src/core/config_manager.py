"""
Configuration Manager for API Keys and Settings
"""

import json
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".vulnersearch"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "config.json"
        self.key_file = self.config_dir / ".key"
        
        # Generate or load encryption key
        if not self.key_file.exists():
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
        else:
            with open(self.key_file, 'rb') as f:
                key = f.read()
        
        self.cipher = Fernet(key)
        
    def save_api_key(self, api_key: str):
        """Save encrypted API key"""
        config = self._load_config()
        
        # Encrypt the API key
        encrypted_key = self.cipher.encrypt(api_key.encode())
        config['api_key'] = base64.b64encode(encrypted_key).decode()
        
        self._save_config(config)
        
    def get_api_key(self) -> str:
        """Get decrypted API key"""
        config = self._load_config()
        
        if 'api_key' not in config:
            return None
            
        try:
            # Decrypt the API key
            encrypted_key = base64.b64decode(config['api_key'])
            decrypted_key = self.cipher.decrypt(encrypted_key)
            return decrypted_key.decode()
        except:
            return None
    
    def save_setting(self, key: str, value):
        """Save a setting"""
        config = self._load_config()
        config[key] = value
        self._save_config(config)
    
    def get_setting(self, key: str, default=None):
        """Get a setting"""
        config = self._load_config()
        return config.get(key, default)
    
    def reset_settings(self):
        """Reset all settings"""
        if self.config_file.exists():
            os.remove(self.config_file)
        print("✅ Settings reset successfully")
    
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_config(self, config: dict):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)