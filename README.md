# JIRA Test Case Generator & Automation

A comprehensive Streamlit web application that creates JIRA issues, generates test cases, and executes them automatically using BrowserClark AI automation.

## 📺 Demo

**Watch the Demo Video:** [https://youtu.be/vtD-GRIPDz4](https://youtu.be/vtD-GRIPDz4)

## ✨ Features

### 🎯 JIRA Integration
- 🔍 Fetch existing JIRA issues using the JIRA REST API
- 🆕 Create new JIRA issues from feature descriptions
- 📝 Auto-generate structured manual test cases
- 💾 Save test cases as text files
- 📥 Download test cases directly from the browser

### 🤖 Browser Automation
- 🚀 **Execute test steps automatically** using BrowserClark
- 👁️ **Visual Browser Mode** - Watch the automation happen in real-time!
- 🧠 **AI-powered testing** with DeepSeek integration
- 📸 **Automatic screenshot capture** at every step
- 📊 **Real-time status updates** during execution
- 📄 **Comprehensive HTML reports** with results and screenshots

### 🔐 Security & Usability
- 🔐 Secure API key handling with environment variables
- 🎨 Clean, responsive web interface
- ⚡ Real-time automation status updates
- 📱 Mobile-friendly design

## 🚀 Quick Start

> **For browser automation to work, you MUST complete the BrowserClark setup below!**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kunnath/deepcase.git
   cd deepcase
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browser drivers for automation
   ```

3. **Set up BrowserClark for browser automation:**
   ```bash
   # Install additional browser automation dependencies
   pip install browser-use playwright asyncio
   
   # Install Playwright browsers (required for automation)
   playwright install chromium firefox webkit
   ```

4. **Configure your API credentials:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual API keys
   nano .env  # or use your preferred editor
   ```

5. **Get your API tokens:**
   - **JIRA API Token:** [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
   - **DeepSeek API Key:** [DeepSeek Platform](https://platform.deepseek.com/api_keys)

6. **Verify browser automation setup:**
   ```bash
   # Test if browsers are installed correctly
   playwright --version
   
   # Test browser automation (optional)
   python -c "
   try:
       from browser_use import Agent
       from browser_use.llm.deepseek.chat import ChatDeepSeek
       print('✅ BrowserClark automation ready!')
   except ImportError as e:
       print('❌ Browser automation setup incomplete:', e)
   "
   ```

7. **Verify installation (recommended):**
   ```bash
   python verify_setup.py
   ```

8. **Run the application:**
   ```bash
   streamlit run jira_test_generator.py
   ```

## 📖 Usage

1. **Open your browser** to `http://localhost:8501`

2. **Choose your workflow:**

### 🆕 Create New Issue → Test → Automate
   - Fill in feature details (title, description, module, complexity)
   - Click "Create JIRA Issue" ✅
   - Review the auto-generated test case
   - Choose **Show Browser** in sidebar to watch automation live! 👁️
   - Click "🚀 Run Test Steps" to execute automation
   - Watch real-time progress and get detailed reports

### 📋 Fetch Existing Issue → Test → Automate
   - Enter existing JIRA Issue ID (e.g., `PROJ-123`)
   - Click "Fetch Issue" ✅
   - Review the auto-generated test case
   - Choose **Show Browser** in sidebar to watch automation live! 👁️
   - Click "🚀 Run Test Steps" to execute automation  
   - Get comprehensive test results and screenshots

## 📁 File Structure

```
deepcase/
├── jira_test_generator.py  # Main Streamlit application
├── verify_setup.py         # Installation verification script
├── requirements.txt        # Python dependencies with BrowserClark
├── .env.example           # Template for environment variables
├── .env                   # Your API keys (not in git)
├── .gitignore            # Git ignore file
├── LICENSE               # MIT License
├── README.md             # This documentation
└── automation_reports/   # Generated test reports (auto-created)
```

## Generated Test Case Format

The application generates structured test cases with:
- Test Case ID
- Title (from JIRA summary)
- Objective
- Preconditions
- Test Steps
- Expected Results
- Priority and Status fields

## 🤖 BrowserClark Automation Setup

### Prerequisites for Browser Automation

1. **Python 3.8+** (required for browser-use library)
2. **DeepSeek API Key** from [DeepSeek Platform](https://platform.deepseek.com/api_keys)
3. **Playwright browsers** installed

### Detailed Setup Steps

```bash
# 1. Install core browser automation
pip install browser-use>=0.9.5

# 2. Install Playwright and browsers
pip install playwright>=1.55.0
playwright install

# 3. Verify installation
python -c "import playwright; print('Playwright installed:', playwright.__version__)"

# 4. Test browser launch (optional)
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://example.com')
    print('✅ Browser automation working!')
    browser.close()
"
```

### Environment Variables Required

Your `.env` file must include:
```bash
# For JIRA integration
jira_base_url="https://your-domain.atlassian.net"
jira_email="your.email@company.com"
jira_api_token="your_jira_api_token"

# For browser automation (REQUIRED)
DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

### Browser Automation Modes

- **🔍 Visual Mode (Default)**: Browser window is visible - watch automation happen!
  - Great for debugging and learning
  - See exactly what the AI is doing
  - Slower but more transparent

- **⚡ Headless Mode**: Browser runs in background
  - Faster execution
  - No visual window
  - Better for batch processing

## 🔐 Security Notes

- **API keys are handled securely** through environment variables
- **`.env` file is excluded** from git repository (see `.gitignore`)
- **Sensitive information is not stored** in the application
- **API keys are masked** in the UI input field
- **Use `.env.example`** as a template for your local `.env` file

## 🔧 Troubleshooting

### JIRA Issues
- **Authentication Error**: Verify your JIRA URL, email, and API key
- **Issue Not Found**: Check that the issue ID exists and you have access
- **Connection Issues**: Ensure your JIRA instance is accessible

### Browser Automation Issues

#### "Browser automation not available, running in demo mode"
```bash
# Fix: Install browser-use library
pip install browser-use

# Or reinstall if corrupted
pip uninstall browser-use
pip install browser-use>=0.9.5
```

#### "No module named 'playwright'"
```bash
# Fix: Install Playwright
pip install playwright
playwright install
```

#### "DeepSeek API Error" or "Invalid API Key"
- Verify your `DEEPSEEK_API_KEY` in `.env` file
- Check API key is valid at [DeepSeek Platform](https://platform.deepseek.com/api_keys)
- Ensure no extra spaces or quotes in the API key

#### "Browser failed to launch"
```bash
# Fix: Reinstall browser drivers
playwright uninstall
playwright install

# Or install specific browser
playwright install chromium
```

#### "Headless mode not working"
- Switch to "Show Browser" mode in the sidebar
- Check if any antivirus is blocking browser automation
- Try running with administrator privileges (Windows) or sudo (Linux/Mac)

#### Performance Issues
- **Slow automation**: Use "Headless" mode for faster execution
- **High CPU usage**: Close other browser instances
- **Memory issues**: Restart the Streamlit application

### Debug Mode
Enable debug logging by running:
```bash
# Run with verbose output
PYTHONPATH=. streamlit run jira_test_generator.py --logger.level=debug
```

## 📋 Requirements

- **Python 3.7+**
- **Valid JIRA account** with API access
- **DeepSeek API account** for browser automation
- **Internet connection** to fetch JIRA issues and run automation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you have any questions or issues:
- Open an issue on [GitHub](https://github.com/kunnath/deepcase/issues)
- Check the troubleshooting section above

---

**Built with ❤️ using Streamlit & BrowserClark**
