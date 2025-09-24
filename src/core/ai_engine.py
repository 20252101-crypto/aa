"""
AI Engine using Google Gemini
"""

import google.generativeai as genai
import json
import time
from typing import Dict, List, Any

class AIEngine:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    def update_api_key(self, api_key: str):
        """Update API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        
    def analyze_target(self, target: str) -> str:
        """Analyze target for vulnerabilities"""
        prompt = f"""
        As an advanced cybersecurity AI, analyze the target: {target}
        
        Provide a comprehensive vulnerability assessment including:
        1. Potential attack vectors
        2. Common vulnerabilities to check
        3. Recommended security tools
        4. Testing methodology
        5. Risk assessment
        
        Format the response in a clear, actionable manner.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Analysis failed: {e}"
    
    def suggest_tools(self, vulnerability_type: str) -> List[str]:
        """Suggest tools for specific vulnerability types"""
        prompt = f"""
        Suggest the best GitHub security tools for testing {vulnerability_type}.
        Return only tool names, one per line, maximum 10 tools.
        Focus on popular, well-maintained tools.
        """
        
        try:
            response = self.model.generate_content(prompt)
            tools = [tool.strip() for tool in response.text.split('\n') if tool.strip()]
            return tools[:10]
        except Exception as e:
            return [f"Error getting suggestions: {e}"]
    
    def explain_tool_usage(self, tool_name: str, tool_description: str) -> str:
        """Explain how to use a specific tool"""
        prompt = f"""
        Explain how to use the security tool: {tool_name}
        Description: {tool_description}
        
        Provide:
        1. Installation steps
        2. Basic usage commands
        3. Common use cases
        4. Important parameters
        5. Example commands
        
        Keep it practical and beginner-friendly.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Failed to get tool explanation: {e}"
    
    def analyze_scan_results(self, results: Dict[str, Any]) -> str:
        """Analyze scan results and provide insights"""
        prompt = f"""
        Analyze these security scan results and provide insights:
        
        {json.dumps(results, indent=2)}
        
        Provide:
        1. Summary of findings
        2. Risk prioritization
        3. Exploitation possibilities
        4. Remediation recommendations
        5. Next steps for testing
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Analysis failed: {e}"
    
    def generate_payload(self, vulnerability_type: str, target_info: str) -> str:
        """Generate testing payloads"""
        prompt = f"""
        Generate testing payloads for {vulnerability_type} on target: {target_info}
        
        Provide:
        1. Basic test payloads
        2. Advanced exploitation attempts
        3. Bypass techniques
        4. Detection evasion methods
        
        IMPORTANT: This is for authorized security testing only.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Payload generation failed: {e}"