#!/usr/bin/env python3
"""
VulnerSearch AI - Advanced Bug Hunting Tool
Author: AI Assistant
Version: 2.0.0
"""

import os
import sys
import json
import time
import threading
import subprocess
import psutil
from pathlib import Path

# Import UI and core modules
from src.ui.interface import VulnerSearchUI
from src.core.ai_engine import AIEngine
from src.core.github_manager import GitHubManager
from src.core.tool_manager import ToolManager
from src.core.config_manager import ConfigManager
from src.utils.logger import Logger
from src.utils.voice import VoiceAssistant

class VulnerSearchAI:
    def __init__(self):
        self.config = ConfigManager()
        self.logger = Logger()
        self.ui = VulnerSearchUI()
        self.voice = VoiceAssistant()
        self.ai_engine = None
        self.github_manager = None
        self.tool_manager = None
        
    def initialize(self):
        """Initialize the application"""
        try:
            self.ui.show_banner()
            self.voice.speak("Initializing VulnerSearch AI Advanced")
            
            # Check API key
            api_key = self.config.get_api_key()
            if not api_key:
                api_key = self.ui.get_api_key()
                self.config.save_api_key(api_key)
                self.voice.speak("API key saved successfully")
            
            # Initialize components
            self.ai_engine = AIEngine(api_key)
            self.github_manager = GitHubManager()
            self.tool_manager = ToolManager(self.ai_engine, self.github_manager)
            
            self.logger.info("VulnerSearch AI initialized successfully")
            self.voice.speak("System ready for bug hunting")
            return True
            
        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")
            self.ui.show_error(f"Failed to initialize: {e}")
            return False
    
    def run(self):
        """Main application loop"""
        if not self.initialize():
            return
        
        while True:
            try:
                choice = self.ui.show_main_menu()
                
                if choice == "1":
                    self.automated_scan()
                elif choice == "2":
                    self.github_tool_search()
                elif choice == "3":
                    self.manual_testing()
                elif choice == "4":
                    self.vulnerability_analysis()
                elif choice == "5":
                    self.settings_menu()
                elif choice == "6":
                    self.voice.speak("Goodbye! Happy bug hunting!")
                    break
                else:
                    self.ui.show_error("Invalid choice!")
                    
            except KeyboardInterrupt:
                self.ui.show_info("\nExiting VulnerSearch AI...")
                self.voice.speak("Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Runtime error: {e}")
                self.ui.show_error(f"Error: {e}")
    
    def automated_scan(self):
        """Automated vulnerability scanning"""
        self.voice.speak("Starting automated vulnerability scan")
        target = self.ui.get_target()
        threads = self.ui.get_thread_count()
        
        self.tool_manager.run_automated_scan(target, threads)
    
    def github_tool_search(self):
        """Search and download tools from GitHub"""
        self.voice.speak("Searching GitHub for security tools")
        query = self.ui.get_search_query()
        
        tools = self.github_manager.search_tools(query)
        if tools:
            selected_tool = self.ui.select_tool(tools)
            if selected_tool:
                self.tool_manager.download_and_setup_tool(selected_tool)
    
    def manual_testing(self):
        """Manual testing interface"""
        self.voice.speak("Entering manual testing mode")
        self.tool_manager.manual_testing_mode()
    
    def vulnerability_analysis(self):
        """AI-powered vulnerability analysis"""
        self.voice.speak("Starting AI vulnerability analysis")
        target = self.ui.get_target()
        
        analysis = self.ai_engine.analyze_target(target)
        self.ui.show_analysis_results(analysis)
    
    def settings_menu(self):
        """Settings and configuration"""
        while True:
            choice = self.ui.show_settings_menu()
            
            if choice == "1":
                api_key = self.ui.get_api_key()
                self.config.save_api_key(api_key)
                self.ai_engine.update_api_key(api_key)
                self.voice.speak("API key updated")
            elif choice == "2":
                self.config.reset_settings()
                self.voice.speak("Settings reset")
            elif choice == "3":
                self.ui.show_system_info()
            elif choice == "4":
                break

if __name__ == "__main__":
    app = VulnerSearchAI()
    app.run()