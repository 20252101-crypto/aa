"""
Advanced Tool Manager with Multi-threading Support
"""

import threading
import time
import subprocess
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import json
from pathlib import Path
import os
import sys

class ToolManager:
    def __init__(self, ai_engine, github_manager):
        self.ai_engine = ai_engine
        self.github_manager = github_manager
        self.results = {}
        self.active_threads = 0
        self.tools_dir = Path("tools")
        self.tools_dir.mkdir(exist_ok=True)
        
    def run_automated_scan(self, target: str, thread_count: int):
        """Run automated vulnerability scan with multi-threading"""
        from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
        from rich.console import Console
        
        console = Console()
        console.print(f"🚀 [bold green]Starting automated scan on {target} with {thread_count} threads[/bold green]")
        
        scan_tasks = [
            ("🔍 Port Scan", self._port_scan),
            ("📁 Directory Enumeration", self._dir_enum),
            ("🌐 Subdomain Discovery", self._subdomain_scan),
            ("🔧 Technology Detection", self._tech_detection),
            ("🔒 SSL/TLS Analysis", self._ssl_analysis),
            ("📋 HTTP Headers Analysis", self._header_analysis),
            ("⚠️ Vulnerability Assessment", self._vuln_assessment),
            ("🌍 DNS Enumeration", self._dns_enum),
            ("🕷️ Web Crawler", self._web_crawl),
            ("💉 SQL Injection Test", self._sql_injection_test)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                task_progress = progress.add_task("Scanning...", total=len(scan_tasks))
                
                future_to_task = {
                    executor.submit(task_func, target): task_name 
                    for task_name, task_func in scan_tasks
                }
                
                for future in as_completed(future_to_task):
                    task_name = future_to_task[future]
                    try:
                        result = future.result()
                        self.results[task_name] = result
                        console.print(f"✅ [bold green]{task_name} completed[/bold green]")
                    except Exception as e:
                        console.print(f"❌ [bold red]{task_name} failed: {e}[/bold red]")
                        self.results[task_name] = f"Error: {e}"
                    
                    progress.update(task_progress, advance=1)
        
        # AI Analysis of results
        console.print("🧠 [bold cyan]Running AI analysis...[/bold cyan]")
        ai_analysis = self.ai_engine.analyze_scan_results(self.results)
        self.results["AI_Analysis"] = ai_analysis
        
        self._save_results(target)
        self._display_results()
        
    def _port_scan(self, target: str) -> Dict[str, Any]:
        """Advanced port scanning"""
        try:
            import nmap
            nm = nmap.PortScanner()
            
            # Common ports + additional security-focused ports
            ports = "21,22,23,25,53,80,110,111,135,139,143,443,993,995,1723,3306,3389,5432,5900,6379,8080,8443,9200,27017"
            
            result = nm.scan(target, ports, arguments='-sS -sV -O --script vuln')
            
            open_ports = []
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    ports_list = nm[host][proto].keys()
                    for port in ports_list:
                        if nm[host][proto][port]['state'] == 'open':
                            service = nm[host][proto][port].get('name', 'unknown')
                            version = nm[host][proto][port].get('version', '')
                            open_ports.append({
                                'port': port,
                                'service': service,
                                'version': version,
                                'state': 'open'
                            })
            
            return {
                'open_ports': open_ports,
                'total_ports_scanned': len(ports.split(',')),
                'scan_info': nm.scaninfo()
            }
            
        except Exception as e:
            return {'error': str(e), 'fallback': self._basic_port_scan(target)}
    
    def _basic_port_scan(self, target: str) -> Dict[str, Any]:
        """Basic port scan fallback"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append({'port': port, 'state': 'open'})
                sock.close()
            except:
                continue
                
        return {'open_ports': open_ports, 'method': 'basic_scan'}
    
    def _dir_enum(self, target: str) -> Dict[str, Any]:
        """Directory enumeration"""
        common_dirs = [
            'admin', 'administrator', 'login', 'wp-admin', 'wp-login',
            'phpmyadmin', 'cpanel', 'webmail', 'mail', 'email',
            'user', 'users', 'test', 'demo', 'backup', 'backups',
            'config', 'configuration', 'database', 'db', 'sql',
            'upload', 'uploads', 'files', 'file', 'download',
            'api', 'v1', 'v2', 'rest', 'graphql', 'swagger',
            'dashboard', 'panel', 'control', 'manage', 'manager'
        ]
        
        found_dirs = []
        base_url = f"http://{target}" if not target.startswith('http') else target
        
        for directory in common_dirs:
            try:
                url = f"{base_url}/{directory}"
                response = requests.get(url, timeout=3, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    found_dirs.append({
                        'directory': directory,
                        'url': url,
                        'status_code': response.status_code,
                        'size': len(response.content)
                    })
            except:
                continue
                
        return {'found_directories': found_dirs, 'total_tested': len(common_dirs)}
    
    def _subdomain_scan(self, target: str) -> Dict[str, Any]:
        """Subdomain discovery"""
        subdomains = [
            'www', 'mail', 'ftp', 'admin', 'test', 'dev', 'staging',
            'api', 'app', 'blog', 'shop', 'store', 'support',
            'help', 'docs', 'portal', 'secure', 'vpn', 'remote',
            'cdn', 'static', 'assets', 'img', 'images', 'media'
        ]
        
        found_subdomains = []
        
        for subdomain in subdomains:
            try:
                full_domain = f"{subdomain}.{target}"
                socket.gethostbyname(full_domain)
                found_subdomains.append({
                    'subdomain': full_domain,
                    'type': 'A',
                    'status': 'active'
                })
            except:
                continue
                
        return {'found_subdomains': found_subdomains, 'total_tested': len(subdomains)}
    
    def _tech_detection(self, target: str) -> Dict[str, Any]:
        """Technology stack detection"""
        try:
            url = f"http://{target}" if not target.startswith('http') else target
            response = requests.get(url, timeout=5)
            
            headers = response.headers
            content = response.text.lower()
            
            technologies = []
            
            # Server detection
            if 'server' in headers:
                technologies.append({'type': 'Server', 'name': headers['server']})
            
            # Framework detection
            frameworks = {
                'wordpress': 'wp-content' in content or 'wp-includes' in content,
                'drupal': 'drupal' in content,
                'joomla': 'joomla' in content,
                'laravel': 'laravel_session' in content,
                'django': 'csrfmiddlewaretoken' in content,
                'react': 'react' in content,
                'angular': 'ng-' in content,
                'vue': 'vue' in content
            }
            
            for framework, detected in frameworks.items():
                if detected:
                    technologies.append({'type': 'Framework', 'name': framework})
            
            return {'technologies': technologies, 'headers': dict(headers)}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _ssl_analysis(self, target: str) -> Dict[str, Any]:
        """SSL/TLS security analysis"""
        try:
            import ssl
            import socket
            
            context = ssl.create_default_context()
            
            with socket.create_connection((target, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    return {
                        'certificate': {
                            'subject': cert.get('subject'),
                            'issuer': cert.get('issuer'),
                            'version': cert.get('version'),
                            'serial_number': cert.get('serialNumber'),
                            'not_before': cert.get('notBefore'),
                            'not_after': cert.get('notAfter')
                        },
                        'cipher': {
                            'name': cipher[0] if cipher else None,
                            'version': cipher[1] if cipher else None,
                            'bits': cipher[2] if cipher else None
                        },
                        'protocol': ssock.version()
                    }
                    
        except Exception as e:
            return {'error': str(e), 'ssl_available': False}
    
    def _header_analysis(self, target: str) -> Dict[str, Any]:
        """HTTP security headers analysis"""
        try:
            url = f"http://{target}" if not target.startswith('http') else target
            response = requests.get(url, timeout=5)
            
            security_headers = {
                'X-Frame-Options': response.headers.get('X-Frame-Options'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security'),
                'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                'Referrer-Policy': response.headers.get('Referrer-Policy'),
                'Feature-Policy': response.headers.get('Feature-Policy')
            }
            
            missing_headers = [k for k, v in security_headers.items() if v is None]
            
            return {
                'security_headers': security_headers,
                'missing_headers': missing_headers,
                'security_score': len([v for v in security_headers.values() if v]) / len(security_headers) * 100
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _vuln_assessment(self, target: str) -> Dict[str, Any]:
        """Basic vulnerability assessment"""
        vulnerabilities = []
        
        # Check for common vulnerabilities
        try:
            url = f"http://{target}" if not target.startswith('http') else target
            
            # Directory traversal test
            traversal_payloads = ['../../../etc/passwd', '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts']
            for payload in traversal_payloads:
                try:
                    response = requests.get(f"{url}/{payload}", timeout=3)
                    if 'root:' in response.text or 'localhost' in response.text:
                        vulnerabilities.append({
                            'type': 'Directory Traversal',
                            'severity': 'High',
                            'payload': payload
                        })
                except:
                    continue
            
            # SQL injection basic test
            sql_payloads = ["'", "1' OR '1'='1", "'; DROP TABLE users; --"]
            for payload in sql_payloads:
                try:
                    response = requests.get(f"{url}?id={payload}", timeout=3)
                    if 'sql' in response.text.lower() or 'mysql' in response.text.lower():
                        vulnerabilities.append({
                            'type': 'Possible SQL Injection',
                            'severity': 'Critical',
                            'payload': payload
                        })
                except:
                    continue
                    
        except Exception as e:
            vulnerabilities.append({'type': 'Assessment Error', 'error': str(e)})
        
        return {'vulnerabilities': vulnerabilities, 'total_tests': 6}
    
    def _dns_enum(self, target: str) -> Dict[str, Any]:
        """DNS enumeration"""
        try:
            import dns.resolver
            
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME']
            dns_records = {}
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(target, record_type)
                    dns_records[record_type] = [str(answer) for answer in answers]
                except:
                    dns_records[record_type] = []
            
            return {'dns_records': dns_records}
            
        except Exception as e:
            return {'error': str(e)}
    
    def _web_crawl(self, target: str) -> Dict[str, Any]:
        """Basic web crawler"""
        try:
            from bs4 import BeautifulSoup
            
            url = f"http://{target}" if not target.startswith('http') else target
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = []
            forms = []
            
            # Extract links
            for link in soup.find_all('a', href=True):
                links.append(link['href'])
            
            # Extract forms
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET'),
                    'inputs': []
                }
                
                for input_tag in form.find_all('input'):
                    form_data['inputs'].append({
                        'name': input_tag.get('name', ''),
                        'type': input_tag.get('type', 'text')
                    })
                
                forms.append(form_data)
            
            return {
                'links': links[:20],  # Limit to first 20 links
                'forms': forms,
                'total_links': len(links),
                'total_forms': len(forms)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _sql_injection_test(self, target: str) -> Dict[str, Any]:
        """Advanced SQL injection testing"""
        try:
            url = f"http://{target}" if not target.startswith('http') else target
            
            # SQL injection payloads
            payloads = [
                "1' OR '1'='1",
                "1' OR '1'='1' --",
                "1' OR '1'='1' /*",
                "1'; DROP TABLE users; --",
                "1' UNION SELECT 1,2,3 --",
                "1' AND (SELECT COUNT(*) FROM information_schema.tables) > 0 --"
            ]
            
            vulnerable_params = []
            
            # Test common parameters
            test_params = ['id', 'user', 'page', 'cat', 'item', 'product']
            
            for param in test_params:
                for payload in payloads:
                    try:
                        test_url = f"{url}?{param}={payload}"
                        response = requests.get(test_url, timeout=3)
                        
                        # Check for SQL error messages
                        error_indicators = [
                            'mysql_fetch_array',
                            'ORA-01756',
                            'Microsoft OLE DB Provider',
                            'SQLServer JDBC Driver',
                            'PostgreSQL query failed',
                            'Warning: mysql_',
                            'MySQLSyntaxErrorException'
                        ]
                        
                        for indicator in error_indicators:
                            if indicator.lower() in response.text.lower():
                                vulnerable_params.append({
                                    'parameter': param,
                                    'payload': payload,
                                    'error_type': indicator
                                })
                                break
                                
                    except:
                        continue
            
            return {
                'vulnerable_parameters': vulnerable_params,
                'total_payloads_tested': len(payloads) * len(test_params)
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _save_results(self, target: str):
        """Save scan results to file"""
        results_dir = Path("scan_results")
        results_dir.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = results_dir / f"scan_{target.replace(':', '_')}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"📄 Results saved to: {filename}")
    
    def _display_results(self):
        """Display scan results in a formatted way"""
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        for task_name, result in self.results.items():
            if task_name == "AI_Analysis":
                console.print(Panel(
                    result,
                    title="🧠 AI Analysis",
                    border_style="cyan"
                ))
            else:
                console.print(f"\n[bold green]{task_name}[/bold green]")
                if isinstance(result, dict):
                    console.print_json(data=result)
                else:
                    console.print(result)
    
    def download_and_setup_tool(self, tool: Dict[str, Any]):
        """Download and setup tool from GitHub"""
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, TextColumn
        
        console = Console()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Downloading {tool['name']}...", total=None)
            
            success = self.github_manager.download_tool(tool)
            
            if success:
                progress.update(task, description=f"✅ {tool['name']} downloaded successfully")
                
                # Get AI explanation of tool usage
                explanation = self.ai_engine.explain_tool_usage(
                    tool['name'], 
                    tool['description']
                )
                
                console.print(Panel(
                    explanation,
                    title=f"🛠️ How to use {tool['name']}",
                    border_style="green"
                ))
            else:
                progress.update(task, description=f"❌ Failed to download {tool['name']}")
    
    def manual_testing_mode(self):
        """Interactive manual testing mode"""
        from rich.console import Console
        from rich.prompt import Prompt
        
        console = Console()
        console.print(Panel(
            "[bold cyan]Manual Testing Mode[/bold cyan]\n"
            "Available commands:\n"
            "• scan <target> - Quick scan\n"
            "• exploit <target> <type> - Run specific exploit\n"
            "• tools - List downloaded tools\n"
            "• run <tool> <args> - Run specific tool\n"
            "• ai <question> - Ask AI for help\n"
            "• exit - Exit manual mode",
            border_style="blue"
        ))
        
        while True:
            try:
                command = Prompt.ask("[bold yellow]manual>[/bold yellow]").strip()
                
                if command == "exit":
                    break
                elif command.startswith("scan "):
                    target = command.split(" ", 1)[1]
                    self._quick_scan(target)
                elif command.startswith("ai "):
                    question = command.split(" ", 1)[1]
                    response = self.ai_engine.model.generate_content(question)
                    console.print(Panel(response.text, title="🧠 AI Response", border_style="cyan"))
                elif command == "tools":
                    tools = self.github_manager.list_downloaded_tools()
                    console.print(f"Downloaded tools: {', '.join(tools)}")
                elif command.startswith("run "):
                    parts = command.split(" ")
                    tool_name = parts[1]
                    args = parts[2:] if len(parts) > 2 else []
                    result = self.github_manager.run_tool(tool_name, args)
                    console.print(result)
                else:
                    console.print("[red]Unknown command. Type 'exit' to quit.[/red]")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
    
    def _quick_scan(self, target: str):
        """Quick vulnerability scan"""
        from rich.console import Console
        
        console = Console()
        console.print(f"🔍 Quick scanning {target}...")
        
        # Run basic checks
        port_result = self._basic_port_scan(target)
        dir_result = self._dir_enum(target)
        
        console.print(f"Open ports: {len(port_result.get('open_ports', []))}")
        console.print(f"Found directories: {len(dir_result.get('found_directories', []))}")