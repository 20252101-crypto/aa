"""
GitHub Integration Manager
"""

import requests
import json
import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any
import zipfile
import tempfile
import git

class GitHubManager:
    def __init__(self):
        self.api_base = "https://api.github.com"
        self.tools_dir = Path("downloaded_tools")
        self.tools_dir.mkdir(exist_ok=True)
        
    def search_tools(self, query: str, category: str = "security") -> List[Dict[str, Any]]:
        """Search for security tools on GitHub"""
        search_query = f"{query} {category} tool"
        url = f"{self.api_base}/search/repositories"
        
        params = {
            "q": search_query,
            "sort": "stars",
            "order": "desc",
            "per_page": 20
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tools = []
            
            for repo in data.get("items", []):
                tool = {
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo["description"] or "No description",
                    "stars": repo["stargazers_count"],
                    "language": repo["language"],
                    "clone_url": repo["clone_url"],
                    "html_url": repo["html_url"],
                    "topics": repo.get("topics", [])
                }
                tools.append(tool)
            
            return tools
            
        except Exception as e:
            print(f"Error searching GitHub: {e}")
            return []
    
    def download_tool(self, tool: Dict[str, Any]) -> bool:
        """Download and setup tool from GitHub"""
        tool_name = tool["name"]
        clone_url = tool["clone_url"]
        tool_path = self.tools_dir / tool_name
        
        try:
            if tool_path.exists():
                shutil.rmtree(tool_path)
            
            print(f"🔄 Cloning {tool_name}...")
            git.Repo.clone_from(clone_url, tool_path)
            
            # Try to setup the tool
            self._setup_tool(tool_path, tool)
            
            print(f"✅ Successfully downloaded {tool_name}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download {tool_name}: {e}")
            return False
    
    def _setup_tool(self, tool_path: Path, tool: Dict[str, Any]):
        """Setup downloaded tool"""
        # Check for setup files
        setup_files = ["setup.py", "requirements.txt", "install.sh", "Makefile"]
        
        for setup_file in setup_files:
            setup_path = tool_path / setup_file
            if setup_path.exists():
                if setup_file == "requirements.txt":
                    subprocess.run([
                        "pip", "install", "-r", str(setup_path)
                    ], cwd=tool_path, capture_output=True)
                elif setup_file == "setup.py":
                    subprocess.run([
                        "python", "setup.py", "install"
                    ], cwd=tool_path, capture_output=True)
                elif setup_file == "install.sh":
                    subprocess.run([
                        "bash", "install.sh"
                    ], cwd=tool_path, capture_output=True)
                break
    
    def get_tool_usage(self, tool_name: str) -> str:
        """Get tool usage instructions"""
        tool_path = self.tools_dir / tool_name
        
        if not tool_path.exists():
            return "Tool not found. Please download it first."
        
        # Look for documentation files
        doc_files = ["README.md", "README.txt", "USAGE.md", "help.txt"]
        
        for doc_file in doc_files:
            doc_path = tool_path / doc_file
            if doc_path.exists():
                try:
                    with open(doc_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        return content[:2000]  # Limit content
                except:
                    continue
        
        return "No documentation found for this tool."
    
    def list_downloaded_tools(self) -> List[str]:
        """List all downloaded tools"""
        if not self.tools_dir.exists():
            return []
        
        return [d.name for d in self.tools_dir.iterdir() if d.is_dir()]
    
    def run_tool(self, tool_name: str, args: List[str] = None) -> str:
        """Run a downloaded tool"""
        tool_path = self.tools_dir / tool_name
        
        if not tool_path.exists():
            return f"Tool {tool_name} not found"
        
        # Look for executable files
        executables = ["main.py", f"{tool_name}.py", "run.py", tool_name]
        
        for exe in executables:
            exe_path = tool_path / exe
            if exe_path.exists():
                try:
                    cmd = ["python", str(exe_path)]
                    if args:
                        cmd.extend(args)
                    
                    result = subprocess.run(
                        cmd, 
                        cwd=tool_path, 
                        capture_output=True, 
                        text=True,
                        timeout=30
                    )
                    
                    return result.stdout + result.stderr
                    
                except subprocess.TimeoutExpired:
                    return "Tool execution timed out"
                except Exception as e:
                    return f"Error running tool: {e}"
        
        return f"No executable found for {tool_name}"