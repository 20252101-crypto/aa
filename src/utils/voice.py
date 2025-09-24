"""
Voice Assistant for VulnerSearch AI
"""

import pyttsx3
import threading
from typing import Optional

class VoiceAssistant:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.8)  # Volume level
            
            # Try to set a better voice
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    # Use first available voice
                    self.engine.setProperty('voice', voices[0].id)
            
            self.enabled = True
            
        except Exception as e:
            print(f"⚠️ Voice assistant not available: {e}")
            self.engine = None
            self.enabled = False
    
    def speak(self, text: str, async_mode: bool = True):
        """Speak the given text"""
        if not self.enabled or not self.engine:
            return
        
        try:
            if async_mode:
                # Speak in background thread
                thread = threading.Thread(target=self._speak_sync, args=(text,))
                thread.daemon = True
                thread.start()
            else:
                self._speak_sync(text)
                
        except Exception as e:
            print(f"Voice error: {e}")
    
    def _speak_sync(self, text: str):
        """Synchronous speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass
    
    def set_voice_speed(self, rate: int):
        """Set speech rate (words per minute)"""
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        if self.engine:
            self.engine.setProperty('volume', volume)
    
    def toggle(self):
        """Toggle voice assistant on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"🔊 Voice assistant {status}")
        
        if self.enabled:
            self.speak("Voice assistant enabled")
    
    def list_voices(self):
        """List available voices"""
        if not self.engine:
            return []
        
        voices = self.engine.getProperty('voices')
        voice_list = []
        
        for i, voice in enumerate(voices):
            voice_info = {
                'id': i,
                'name': voice.name,
                'language': getattr(voice, 'languages', ['Unknown'])[0] if hasattr(voice, 'languages') else 'Unknown'
            }
            voice_list.append(voice_info)
        
        return voice_list
    
    def set_voice(self, voice_id: int):
        """Set voice by ID"""
        if not self.engine:
            return False
        
        voices = self.engine.getProperty('voices')
        if 0 <= voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)
            self.speak(f"Voice changed to {voices[voice_id].name}")
            return True
        
        return False