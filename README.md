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

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install  # Install browser drivers
   ```

2. **Configure your API credentials in `.env`:**
   ```bash
   jira_base_url="https://your-domain.atlassian.net"
   jira_email="your.email@company.com"
   jira_api_token="your_jira_api_token"
   DEEPSEEK_API_KEY="your_deepseek_api_key"
   ```

3. **Get your API tokens:**
   - **JIRA API Token:** [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
   - **DeepSeek API Key:** [DeepSeek Platform](https://platform.deepseek.com/api_keys)

## 📖 Usage

1. **Run the application:**
   ```bash
   streamlit run jira_test_generator.py
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Choose your workflow:**

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

## File Structure

```
├── jira_test_generator.py  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (JIRA API key)
└── README.md             # This file
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

## Security Notes

- API keys are handled securely through environment variables
- Sensitive information is not stored in the application
- API keys are masked in the UI input field

## Troubleshooting

- **Authentication Error**: Verify your JIRA URL, email, and API key
- **Issue Not Found**: Check that the issue ID exists and you have access
- **Connection Issues**: Ensure your JIRA instance is accessible

## Requirements

- Python 3.7+
- Valid JIRA account with API access
- Internet connection to fetch JIRA issues# deepcase
