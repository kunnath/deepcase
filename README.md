# JIRA Test Case Generator & Automation

A comprehensive Streamlit web application that creates JIRA issues, generates test cases, and executes them automatically using BrowserClark AI automation.

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

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kunnath/deepcase.git
   cd deepcase
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browser drivers
   ```

3. **Configure your API credentials:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual API keys
   nano .env  # or use your preferred editor
   ```

4. **Get your API tokens:**
   - **JIRA API Token:** [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
   - **DeepSeek API Key:** [DeepSeek Platform](https://platform.deepseek.com/api_keys)

5. **Run the application:**
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
├── requirements.txt        # Python dependencies
├── .env.example           # Template for environment variables
├── .env                   # Your API keys (not in git)
├── .gitignore            # Git ignore file
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

## 🔐 Security Notes

- **API keys are handled securely** through environment variables
- **`.env` file is excluded** from git repository (see `.gitignore`)
- **Sensitive information is not stored** in the application
- **API keys are masked** in the UI input field
- **Use `.env.example`** as a template for your local `.env` file

## Troubleshooting

- **Authentication Error**: Verify your JIRA URL, email, and API key
- **Issue Not Found**: Check that the issue ID exists and you have access
- **Connection Issues**: Ensure your JIRA instance is accessible

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
