# 🔥 VulnerSearch AI - Advanced Bug Hunting Tool

<div align="center">

![VulnerSearch AI](https://img.shields.io/badge/VulnerSearch-AI%20Powered-red?style=for-the-badge&logo=python)
![Version](https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**🚀 The Most Advanced AI-Powered Bug Hunting Tool with GitHub Integration**

</div>

## ✨ Features

### 🧠 AI-Powered Analysis
- **Google Gemini Integration** - Advanced AI analysis of vulnerabilities
- **Smart Payload Generation** - AI generates custom payloads for testing
- **Intelligent Reporting** - AI provides detailed vulnerability assessments
- **Voice Assistant** - AI speaks and guides you through the process

### 🔍 Advanced Scanning
- **Multi-threaded Scanning** - Choose from 4, 8, 12 threads or max CPU cores
- **Comprehensive Port Scanning** - Advanced Nmap integration
- **Directory Enumeration** - Smart directory discovery
- **Subdomain Discovery** - Find hidden subdomains
- **Technology Detection** - Identify web technologies and frameworks
- **SSL/TLS Analysis** - Security certificate analysis
- **HTTP Header Analysis** - Security headers assessment
- **SQL Injection Testing** - Advanced SQLi detection
- **Web Crawling** - Intelligent web application mapping

### 🛠️ GitHub Integration
- **Tool Discovery** - Search and find security tools on GitHub
- **Automatic Download** - Clone and setup tools automatically
- **AI Tool Explanation** - AI explains how to use downloaded tools
- **Tool Management** - Organize and run downloaded tools

### 🎨 User Experience
- **Colorful Interface** - Beautiful Rich-based UI with colors and animations
- **Voice Feedback** - AI speaks status updates and results
- **Progress Tracking** - Real-time progress bars and spinners
- **Threaded Performance** - Optimized for both potato PCs and high-end systems
- **Secure API Storage** - Encrypted API key storage
- **Auto-save Results** - Automatic result saving with timestamps

## 🚀 Installation

### Quick Install
```bash
# Clone the repository
git clone <your-repo-url>
cd vulnersearch-ai

# Run the installer
python install.py

# Start the tool
python main.py
```

### Manual Install
```bash
# Install requirements
pip install -r requirements.txt

# Create directories
mkdir logs scan_results downloaded_tools tools

# Run the tool
python main.py
```

## 🔑 Setup

1. **Get Google Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - The tool will prompt you for the key on first run

2. **API Key Storage**
   - Keys are encrypted and stored securely
   - No need to re-enter after first setup
   - Stored in `~/.vulnersearch/config.json`

## 🎯 Usage

### Main Menu Options

1. **🎯 Automated Vulnerability Scan**
   - Full automated scanning with AI analysis
   - Multi-threaded performance
   - Comprehensive vulnerability assessment

2. **🔍 GitHub Tool Search & Download**
   - Search for security tools on GitHub
   - Automatic download and setup
   - AI-powered usage instructions

3. **🛠️ Manual Testing Mode**
   - Interactive command-line interface
   - Run specific tools and commands
   - Ask AI for help during testing

4. **🧠 AI Vulnerability Analysis**
   - Deep AI analysis of targets
   - Custom vulnerability assessments
   - Intelligent recommendations

5. **⚙️ Settings & Configuration**
   - Update API keys
   - Configure voice settings
   - System information

### Thread Configuration

Choose your performance level:
- **🐌 Low (4 threads)** - For potato PCs
- **⚡ Medium (8 threads)** - Balanced performance  
- **🚀 High (12 threads)** - High-end systems
- **💥 Max (CPU cores)** - Use all available cores

### Voice Assistant

The AI voice assistant will:
- Guide you through the process
- Announce scan progress
- Provide status updates
- Celebrate successful findings

## 📊 Scan Results

Results are automatically saved to:
- **Location**: `scan_results/`
- **Format**: JSON with timestamp
- **Content**: Complete scan data + AI analysis

## 🛠️ Downloaded Tools

Tools from GitHub are stored in:
- **Location**: `downloaded_tools/`
- **Auto-setup**: Requirements and dependencies
- **AI Integration**: Usage instructions provided

## 🔧 Advanced Features

### Manual Testing Commands
```bash
scan <target>           # Quick vulnerability scan
exploit <target> <type> # Run specific exploit
tools                   # List downloaded tools
run <tool> <args>       # Execute specific tool
ai <question>           # Ask AI for help
exit                    # Exit manual mode
```

### API Integration
- **Secure Storage**: Encrypted API keys
- **Auto-retry**: Handles API failures gracefully
- **Rate Limiting**: Respects API limits

## 🎨 Screenshots

The tool features a beautiful, colorful interface with:
- 🌈 Rich color schemes
- 📊 Progress bars and spinners
- 🎯 Organized menu systems
- 📋 Formatted result displays
- 🔊 Voice feedback

## ⚠️ Legal Disclaimer

**FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ Security research and education
- ✅ Bug bounty programs
- ✅ Your own systems and applications

**DO NOT USE FOR:**
- ❌ Unauthorized access to systems
- ❌ Illegal activities
- ❌ Malicious purposes

Users are responsible for complying with all applicable laws and regulations.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:
1. Check the logs in `logs/` directory
2. Ensure all requirements are installed
3. Verify your API key is valid
4. Check your internet connection

## 🔮 Future Features

- [ ] Web interface
- [ ] More AI models support
- [ ] Advanced exploit modules
- [ ] Report generation
- [ ] Team collaboration features
- [ ] Cloud integration

---

<div align="center">

**Made with ❤️ for the cybersecurity community**

⭐ Star this repo if you find it useful!

</div>