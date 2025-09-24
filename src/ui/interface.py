"""
Advanced User Interface for VulnerSearch AI
"""

import os
import time
import psutil
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from colorama import init, Fore, Back, Style
import pyfiglet

init(autoreset=True)

class VulnerSearchUI:
    def __init__(self):
        self.console = Console()
        
    def show_banner(self):
        """Display colorful banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner = pyfiglet.figlet_format("VulnerSearch AI", font="slant")
        
        self.console.print(Panel(
            f"[bold cyan]{banner}[/bold cyan]\n"
            f"[bold green]🔥 Advanced AI-Powered Bug Hunting Tool v2.0 🔥[/bold green]\n"
            f"[yellow]🚀 GitHub Integration | AI Analysis | Multi-Threading 🚀[/yellow]\n"
            f"[red]⚡ Powered by Google Gemini AI ⚡[/red]",
            border_style="bright_magenta",
            padding=(1, 2)
        ))
        
        # System info
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        
        system_info = Table(show_header=False, box=None)
        system_info.add_column("", style="cyan")
        system_info.add_column("", style="green")
        
        system_info.add_row("💻 CPU Cores:", f"{cpu_count}")
        system_info.add_row("🧠 Memory:", f"{memory.total // (1024**3)} GB")
        system_info.add_row("⚡ Status:", "[bold green]READY[/bold green]")
        
        self.console.print(Panel(system_info, title="[bold blue]System Info[/bold blue]", border_style="blue"))
        
    def show_main_menu(self):
        """Display main menu"""
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("", style="bold cyan", width=3)
        menu_table.add_column("", style="bold white", width=40)
        menu_table.add_column("", style="dim", width=30)
        
        menu_table.add_row("1", "🎯 Automated Vulnerability Scan", "AI-powered scanning")
        menu_table.add_row("2", "🔍 GitHub Tool Search & Download", "Find security tools")
        menu_table.add_row("3", "🛠️  Manual Testing Mode", "Interactive testing")
        menu_table.add_row("4", "🧠 AI Vulnerability Analysis", "Deep AI analysis")
        menu_table.add_row("5", "⚙️  Settings & Configuration", "Manage settings")
        menu_table.add_row("6", "🚪 Exit", "Quit application")
        
        self.console.print(Panel(
            menu_table,
            title="[bold green]🏠 Main Menu[/bold green]",
            border_style="green"
        ))
        
        return Prompt.ask("[bold yellow]Select option[/bold yellow]", choices=["1", "2", "3", "4", "5", "6"])
    
    def get_api_key(self):
        """Get API key from user"""
        self.console.print(Panel(
            "[yellow]🔑 Google Gemini API Key Required[/yellow]\n"
            "[dim]Get your API key from: https://makersuite.google.com/app/apikey[/dim]",
            border_style="yellow"
        ))
        
        return Prompt.ask("[bold cyan]Enter your Gemini API key[/bold cyan]", password=True)
    
    def get_target(self):
        """Get target from user"""
        return Prompt.ask("[bold green]🎯 Enter target (URL/IP)[/bold green]")
    
    def get_thread_count(self):
        """Get thread count with recommendations"""
        cpu_count = psutil.cpu_count()
        
        thread_table = Table(show_header=False, box=None)
        thread_table.add_column("", style="cyan", width=15)
        thread_table.add_column("", style="white", width=20)
        thread_table.add_column("", style="dim", width=25)
        
        thread_table.add_row("1", "🐌 Low (4 threads)", "For potato PCs")
        thread_table.add_row("2", "⚡ Medium (8 threads)", "Balanced performance")
        thread_table.add_row("3", "🚀 High (12 threads)", "High-end systems")
        thread_table.add_row("4", f"💥 Max ({cpu_count} threads)", "Use all CPU cores")
        
        self.console.print(Panel(
            thread_table,
            title="[bold blue]🔧 Thread Configuration[/bold blue]",
            border_style="blue"
        ))
        
        choice = Prompt.ask("[bold yellow]Select thread mode[/bold yellow]", choices=["1", "2", "3", "4"])
        
        thread_map = {"1": 4, "2": 8, "3": 12, "4": cpu_count}
        return thread_map[choice]
    
    def get_search_query(self):
        """Get GitHub search query"""
        return Prompt.ask("[bold cyan]🔍 Enter search query for security tools[/bold cyan]")
    
    def select_tool(self, tools):
        """Display tools and let user select"""
        if not tools:
            self.show_error("No tools found!")
            return None
        
        tool_table = Table(show_header=True, box=None)
        tool_table.add_column("ID", style="cyan", width=5)
        tool_table.add_column("Name", style="bold green", width=25)
        tool_table.add_column("Description", style="white", width=40)
        tool_table.add_column("Stars", style="yellow", width=8)
        
        for i, tool in enumerate(tools[:10], 1):
            tool_table.add_row(
                str(i),
                tool['name'],
                tool['description'][:37] + "..." if len(tool['description']) > 40 else tool['description'],
                str(tool['stars'])
            )
        
        self.console.print(Panel(
            tool_table,
            title="[bold green]🛠️ Available Tools[/bold green]",
            border_style="green"
        ))
        
        try:
            choice = IntPrompt.ask("[bold yellow]Select tool (1-10)[/bold yellow]", default=1)
            if 1 <= choice <= len(tools):
                return tools[choice - 1]
        except:
            pass
        
        return None
    
    def show_progress(self, description):
        """Show progress spinner"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        )
    
    def show_analysis_results(self, analysis):
        """Display AI analysis results"""
        self.console.print(Panel(
            f"[bold green]🧠 AI Analysis Results[/bold green]\n\n{analysis}",
            border_style="green",
            padding=(1, 2)
        ))
    
    def show_settings_menu(self):
        """Display settings menu"""
        settings_table = Table(show_header=False, box=None, padding=(0, 2))
        settings_table.add_column("", style="bold cyan", width=3)
        settings_table.add_column("", style="bold white", width=30)
        
        settings_table.add_row("1", "🔑 Update API Key")
        settings_table.add_row("2", "🔄 Reset Settings")
        settings_table.add_row("3", "📊 System Information")
        settings_table.add_row("4", "🔙 Back to Main Menu")
        
        self.console.print(Panel(
            settings_table,
            title="[bold blue]⚙️ Settings[/bold blue]",
            border_style="blue"
        ))
        
        return Prompt.ask("[bold yellow]Select option[/bold yellow]", choices=["1", "2", "3", "4"])
    
    def show_system_info(self):
        """Display detailed system information"""
        cpu_info = psutil.cpu_freq()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info_table = Table(show_header=True, box=None)
        info_table.add_column("Component", style="cyan", width=15)
        info_table.add_column("Details", style="white", width=40)
        
        info_table.add_row("CPU", f"{psutil.cpu_count()} cores @ {cpu_info.current:.0f}MHz")
        info_table.add_row("Memory", f"{memory.total // (1024**3)} GB ({memory.percent}% used)")
        info_table.add_row("Disk", f"{disk.total // (1024**3)} GB ({disk.percent}% used)")
        info_table.add_row("Platform", f"{os.name}")
        
        self.console.print(Panel(
            info_table,
            title="[bold green]💻 System Information[/bold green]",
            border_style="green"
        ))
        
        input("\nPress Enter to continue...")
    
    def show_info(self, message):
        """Display info message"""
        self.console.print(f"[bold blue]ℹ️  {message}[/bold blue]")
    
    def show_success(self, message):
        """Display success message"""
        self.console.print(f"[bold green]✅ {message}[/bold green]")
    
    def show_warning(self, message):
        """Display warning message"""
        self.console.print(f"[bold yellow]⚠️  {message}[/bold yellow]")
    
    def show_error(self, message):
        """Display error message"""
        self.console.print(f"[bold red]❌ {message}[/bold red]")