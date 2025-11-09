import streamlit as st

# Set page config FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="JIRA Test Case Generator & Automation",
    page_icon="🤖",
    layout="wide"
)

import requests
from requests.auth import HTTPBasicAuth
import os
import json
import asyncio
import time
import threading
import queue
from datetime import datetime
from pathlib import Path
import re
import pandas as pd
import csv
import random
import string

# Load environment variables (optional dependency)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    st.warning("python-dotenv not installed. Environment variables from .env file won't be loaded automatically.")
    pass

# Load Faker for test data generation (optional dependency)
try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    st.sidebar.warning("📦 Install 'faker' for enhanced test data generation: `pip install faker`")

class TestDataManager:
    """Manage test data generation from both Faker and CSV sources"""
    
    def __init__(self):
        self.fake = Faker() if FAKER_AVAILABLE else None
        self.csv_data = None
        self.current_row_index = 0
        
    def detect_feature_type(self, title, description):
        """Detect the type of feature based on title and description"""
        text = (title + " " + description).lower()
        
        if any(keyword in text for keyword in ['login', 'signin', 'auth', 'password', 'credential']):
            return 'login'
        elif any(keyword in text for keyword in ['register', 'signup', 'create account', 'new user']):
            return 'registration'
        elif any(keyword in text for keyword in ['product', 'catalog', 'item', 'inventory', 'shop', 'buy']):
            return 'product'
        elif any(keyword in text for keyword in ['search', 'find', 'query', 'filter']):
            return 'search'
        elif any(keyword in text for keyword in ['contact', 'feedback', 'support', 'message']):
            return 'contact'
        elif any(keyword in text for keyword in ['payment', 'checkout', 'billing', 'card']):
            return 'payment'
        elif any(keyword in text for keyword in ['profile', 'account', 'settings', 'preferences']):
            return 'profile'
        else:
            return 'generic'
    
    def load_csv_data(self, uploaded_file):
        """Load test data from uploaded CSV file"""
        try:
            self.csv_data = pd.read_csv(uploaded_file)
            self.current_row_index = 0
            return True, f"✅ Loaded {len(self.csv_data)} rows of test data"
        except Exception as e:
            return False, f"❌ Error loading CSV: {str(e)}"
    
    def generate_faker_data(self, feature_type):
        """Generate test data using Faker based on feature type"""
        if not self.fake:
            return {}
            
        base_data = {
            'email': self.fake.email(),
            'username': self.fake.user_name(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'company': self.fake.company(),
            'text_field': f"Test Input {random.randint(1, 999)}",
            'number_field': random.randint(1, 100),
            'date_field': self.fake.date(),
        }
        
        if feature_type == 'login':
            return {
                **base_data,
                'password': 'TestPassword123!',
                'login_email': 'test.user@example.com',
                'login_username': 'testuser123'
            }
        elif feature_type == 'registration':
            return {
                **base_data,
                'password': 'TestPassword123!',
                'confirm_password': 'TestPassword123!',
                'age': random.randint(18, 65),
                'gender': random.choice(['Male', 'Female', 'Other'])
            }
        elif feature_type == 'product':
            return {
                **base_data,
                'product_name': f"Test Product {random.randint(1, 999)}",
                'quantity': random.randint(1, 5),
                'price': round(random.uniform(10, 1000), 2),
                'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home']),
                'sku': f"SKU{random.randint(1000, 9999)}"
            }
        elif feature_type == 'search':
            return {
                **base_data,
                'search_query': self.fake.word(),
                'search_terms': [self.fake.word() for _ in range(3)],
                'filter_category': random.choice(['All', 'Recent', 'Popular']),
                'sort_order': random.choice(['Newest', 'Oldest', 'Relevance'])
            }
        elif feature_type == 'contact':
            return {
                **base_data,
                'subject': 'Test Inquiry',
                'message': 'This is a test message for automation testing.',
                'inquiry_type': random.choice(['General', 'Support', 'Sales', 'Technical'])
            }
        elif feature_type == 'payment':
            return {
                **base_data,
                'card_number': '4111111111111111',  # Test Visa card
                'expiry_month': f"{random.randint(1, 12):02d}",
                'expiry_year': str(random.randint(2024, 2030)),
                'cvv': f"{random.randint(100, 999)}",
                'cardholder_name': self.fake.name(),
                'billing_address': self.fake.address()
            }
        elif feature_type == 'profile':
            return {
                **base_data,
                'bio': self.fake.text(max_nb_chars=200),
                'website': self.fake.url(),
                'linkedin': f"linkedin.com/in/{self.fake.user_name()}",
                'timezone': random.choice(['UTC', 'EST', 'PST', 'GMT'])
            }
        else:  # generic
            return base_data
    
    def get_csv_data_row(self, row_index=None):
        """Get a specific row from CSV data or next row cyclically"""
        if self.csv_data is None or len(self.csv_data) == 0:
            return {}
            
        if row_index is None:
            row_index = self.current_row_index
            self.current_row_index = (self.current_row_index + 1) % len(self.csv_data)
        
        row_index = row_index % len(self.csv_data)
        return self.csv_data.iloc[row_index].to_dict()
    
    def get_test_data(self, feature_type, data_mode='faker', row_index=None):
        """Get test data based on mode (faker or csv)"""
        if data_mode == 'csv' and self.csv_data is not None:
            csv_row = self.get_csv_data_row(row_index)
            return {
                'source': 'csv',
                'data': csv_row,
                'row_index': self.current_row_index - 1 if row_index is None else row_index
            }
        else:
            faker_data = self.generate_faker_data(feature_type)
            return {
                'source': 'faker',
                'data': faker_data,
                'feature_type': feature_type
            }
    
    def create_sample_csv_template(self):
        """Create a sample CSV template for users"""
        sample_data = {
            'email': ['test1@example.com', 'test2@example.com', 'test3@example.com'],
            'username': ['testuser1', 'testuser2', 'testuser3'],
            'password': ['TestPass123!', 'TestPass456!', 'TestPass789!'],
            'first_name': ['John', 'Jane', 'Bob'],
            'last_name': ['Doe', 'Smith', 'Johnson'],
            'phone': ['+1-555-0101', '+1-555-0102', '+1-555-0103'],
            'company': ['Test Corp', 'Sample Inc', 'Demo LLC'],
            'product_name': ['Test Product A', 'Test Product B', 'Test Product C'],
            'quantity': [1, 2, 3],
            'search_query': ['automation', 'testing', 'quality'],
            'message': ['Test message 1', 'Test message 2', 'Test message 3']
        }
        
        df = pd.DataFrame(sample_data)
        return df

def get_issue_types(base_url, username, api_key, project_key):
    """Get available issue types for the project"""
    url = f"{base_url}/rest/api/3/project/{project_key}"
    auth = HTTPBasicAuth(username, api_key)
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            data = response.json()
            issue_types = [it["name"] for it in data.get("issueTypes", [])]
            return issue_types, None
        else:
            return [], f"Error fetching issue types: {response.status_code}"
    except Exception as e:
        return [], f"Exception occurred: {str(e)}"

def create_jira_issue(base_url, username, api_key, project_key, feature_title, feature_description, module, complexity, issue_type="Task"):
    """Create a new JIRA issue"""
    url = f"{base_url}/rest/api/3/issue"
    auth = HTTPBasicAuth(username, api_key)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Create the issue payload using Atlassian Document Format (ADF)
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": feature_title,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"Feature Description: {feature_description}"}]
                    },
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"Module: {module}"}]
                    },
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"Complexity: {complexity}"}]
                    }
                ]
            },
            "issuetype": {"name": issue_type},
            "labels": ["feature", "authentication"] if "auth" in feature_title.lower() or "login" in feature_title.lower() else ["feature"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
        if response.status_code == 201:
            data = response.json()
            issue_key = data["key"]
            return issue_key, payload, None
        else:
            error_msg = f"Error creating issue: {response.status_code} - {response.text}"
            return None, None, error_msg
    except Exception as e:
        return None, None, f"Exception occurred: {str(e)}"

def fetch_jira_issue(base_url, username, api_key, issue_id):
    """Fetch JIRA issue details using the API"""
    url = f"{base_url}/rest/api/3/issue/{issue_id}"
    auth = HTTPBasicAuth(username, api_key)
    headers = {"Accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            data = response.json()
            summary = data["fields"]["summary"]
            
            # Handle description safely (it might be None or have different structure)
            description = ""
            if data["fields"].get("description"):
                if isinstance(data["fields"]["description"], dict):
                    # New Atlassian Document Format (ADF)
                    content = data["fields"]["description"].get("content", [])
                    description_parts = []
                    for content_block in content:
                        if content_block.get("content"):
                            for text_block in content_block["content"]:
                                if text_block.get("text"):
                                    description_parts.append(text_block["text"])
                    description = " ".join(description_parts) if description_parts else "No description available"
                else:
                    # Plain text description
                    description = data["fields"]["description"]
            else:
                description = "No description available"
            
            return summary, description, None
        else:
            error_msg = f"Error fetching issue: {response.status_code} - {response.text}"
            return None, None, error_msg
    except Exception as e:
        return None, None, f"Exception occurred: {str(e)}"

def generate_test_case(issue_id, summary, description, test_data=None):
    """Generate a manual test case based on the JIRA issue with test data"""
    
    # Generate test data section if available
    test_data_section = ""
    if test_data and test_data.get('data'):
        data_source = test_data.get('source', 'unknown')
        test_data_section = f"""
Test Data (Source: {data_source.upper()}):
"""
        data = test_data['data']
        for key, value in data.items():
            if isinstance(value, (str, int, float)):
                test_data_section += f"  - {key}: {value}\n"
            elif isinstance(value, list):
                test_data_section += f"  - {key}: {', '.join(map(str, value))}\n"
    
    # Generate more specific test steps based on feature type
    feature_type = test_data.get('feature_type', 'generic') if test_data else 'generic'
    specific_steps = generate_feature_specific_steps(feature_type, summary, test_data)
    
    return f"""=== Manual Test Case ===
Test Case ID: TC_{issue_id}
Title: {summary}
Objective: Verify that the system meets the requirement "{summary}".
Preconditions: User should have access to the application.
{test_data_section}
Test Steps:
{specific_steps}

Expected Result:
  The system should behave as described in: {description[:300]}{'...' if len(description) > 300 else ''}

Priority: Medium
Test Type: Manual
Feature Type: {feature_type}
Status: Draft

Notes:
- This test case was auto-generated from JIRA issue {issue_id}
- Test data is {'included' if test_data else 'not provided'} for automation
- Review and modify as needed before execution
"""

def generate_feature_specific_steps(feature_type, summary, test_data=None):
    """Generate feature-specific test steps based on the feature type"""
    
    if feature_type == 'login':
        return """  1. Navigate to the login page
  2. Enter valid email/username from test data
  3. Enter valid password from test data
  4. Click the login button
  5. Verify successful login and redirection
  6. Test with invalid credentials (negative testing)
  7. Verify appropriate error messages are displayed"""
    
    elif feature_type == 'registration':
        return """  1. Navigate to the registration page
  2. Fill in first name from test data
  3. Fill in last name from test data
  4. Enter email address from test data
  5. Enter username from test data
  6. Set password and confirm password
  7. Fill additional required fields
  8. Submit the registration form
  9. Verify successful registration confirmation
  10. Test with invalid data (negative testing)"""
    
    elif feature_type == 'product':
        return """  1. Navigate to the product catalog/search page
  2. Search for products using test data
  3. Filter by category from test data
  4. Select a product to view details
  5. Verify product information matches expected data
  6. Add product to cart with specified quantity
  7. Verify cart updates correctly
  8. Test product sorting and filtering options"""
    
    elif feature_type == 'search':
        return """  1. Navigate to the search functionality
  2. Enter search query from test data
  3. Execute the search
  4. Verify search results are displayed
  5. Test different search terms from test data
  6. Apply filters if available
  7. Test search with empty/invalid queries
  8. Verify search result accuracy and relevance"""
    
    elif feature_type == 'contact':
        return """  1. Navigate to the contact/feedback form
  2. Fill in name from test data
  3. Enter email address from test data
  4. Fill in phone number from test data
  5. Enter subject from test data
  6. Fill in message from test data
  7. Submit the form
  8. Verify submission confirmation
  9. Test form validation with invalid data"""
    
    elif feature_type == 'payment':
        return """  1. Navigate to the payment/checkout page
  2. Enter billing information from test data
  3. Fill in credit card details from test data
  4. Enter cardholder name from test data
  5. Set expiry date and CVV from test data
  6. Enter billing address from test data
  7. Submit payment information
  8. Verify payment processing
  9. Test with invalid payment data"""
    
    elif feature_type == 'profile':
        return """  1. Navigate to the user profile page
  2. Update profile information using test data
  3. Fill in bio/description from test data
  4. Update contact information
  5. Set preferences and settings
  6. Save profile changes
  7. Verify changes are persisted
  8. Test profile picture upload if applicable"""
    
    else:  # generic
        return """  1. Navigate to the relevant page/section
  2. Identify the main functionality to test
  3. Use test data to fill any required forms/fields
  4. Perform the primary action (submit, save, etc.)
  5. Verify the expected behavior occurs
  6. Test edge cases and error conditions
  7. Validate data persistence and display"""

def save_test_case(test_case, issue_id):
    """Save test case to file"""
    filename = f"TestCase_{issue_id}.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(test_case)
        return filename, None
    except Exception as e:
        return None, f"Error saving file: {str(e)}"

class BrowserTestRunner:
    """Browser automation runner for executing test steps"""
    
    def __init__(self):
        self.result_queue = queue.Queue()
        self.status_queue = queue.Queue()
        self.running = False
        self.thread = None
        self.current_report_dir = None
        
    def extract_test_steps(self, test_case_content):
        """Extract actionable test steps from test case content"""
        # Look for test steps section
        steps_pattern = r"Test Steps:\s*(.*?)(?=Expected Result:|Priority:|Test Type:|$)"
        match = re.search(steps_pattern, test_case_content, re.DOTALL | re.IGNORECASE)
        
        if not match:
            return []
            
        steps_text = match.group(1).strip()
        
        # Extract numbered steps
        step_lines = []
        for line in steps_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('- ') or line.startswith('• ')):
                # Clean up the step
                cleaned_step = re.sub(r'^\d+\.?\s*', '', line)  # Remove numbering
                cleaned_step = re.sub(r'^[-•]\s*', '', cleaned_step)  # Remove bullet points
                if cleaned_step:
                    step_lines.append(cleaned_step)
        
        return step_lines
    
    def convert_test_steps_to_automation_task(self, test_steps, feature_title, url="https://example.com", test_data=None):
        """Convert test steps into browser automation instructions with test data"""
        
        # Prepare test data section
        test_data_section = ""
        if test_data and test_data.get('data'):
            test_data_section = f"""
AVAILABLE TEST DATA ({test_data.get('source', 'unknown').upper()} SOURCE):
{json.dumps(test_data['data'], indent=2)}

"""
        
        if not test_steps:
            return f"""
Navigate to {url} and test the feature: {feature_title}

{test_data_section}General testing approach:
1. Navigate to the main page
2. Look for elements related to '{feature_title}'
3. Use test data provided above to fill forms and inputs
4. Interact with any forms, buttons, or input fields
5. Take screenshots of the process
6. Verify the functionality works as expected
"""
        
        automation_task = f"""
Navigate to {url} and execute the following test steps for feature: {feature_title}

{test_data_section}DETAILED TEST STEPS:
"""
        
        for i, step in enumerate(test_steps, 1):
            automation_task += f"\n{i}. {step}"
            
        automation_task += f"""

AUTOMATION INSTRUCTIONS:
- Use the test data provided above for filling forms, login, registration, etc.
- For email fields: Use 'email' from test data
- For username fields: Use 'username' or 'login_username' from test data
- For password fields: Use 'password' from test data
- For name fields: Use 'first_name' and 'last_name' from test data
- For phone fields: Use 'phone' from test data
- For search fields: Use 'search_query' or 'search_terms' from test data
- For product fields: Use 'product_name', 'quantity', 'price' from test data
- For contact forms: Use 'subject', 'message', 'inquiry_type' from test data
- Take screenshots before and after each major action
- If authentication is required, try the provided credentials first
- Document any fields that couldn't be filled and why
- Handle error messages and validation responses
- Capture the final state and any success/error messages

IMPORTANT:
- Always use the test data provided above rather than random values
- If a field type is not covered in test data, document this in results
- Take extra screenshots when forms are filled or submitted
- Test both valid and invalid scenarios when possible
"""
        
        return automation_task.strip()
    
    def run_browser_automation(self, url, automation_task, api_key, headless=True, test_data=None):
        """Run browser automation in a separate thread"""
        def run_in_thread():
            try:
                self.status_queue.put("🔧 Initializing browser automation...")
                
                # Create report directory
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_name = f"test_automation_{timestamp}"
                self.current_report_dir = Path("automation_reports") / report_name
                self.current_report_dir.mkdir(parents=True, exist_ok=True)
                
                self.status_queue.put(f"📁 Created report directory: {report_name}")
                
                # Save test data to report directory
                if test_data:
                    test_data_file = self.current_report_dir / "test_data.json"
                    test_data_file.write_text(json.dumps(test_data, indent=2), encoding='utf-8')
                    self.status_queue.put(f"💾 Test data saved: {len(test_data.get('data', {}))} data fields")
                
                try:
                    # Try to import browser-use
                    from browser_use import Agent
                    from browser_use.llm.deepseek.chat import ChatDeepSeek
                    browser_available = True
                    self.status_queue.put("✅ Browser automation library loaded")
                except ImportError as e:
                    browser_available = False
                    self.status_queue.put("⚠️ Browser automation not available, running in demo mode")
                
                if browser_available:
                    self.status_queue.put("🤖 Setting up AI agent...")
                    llm = ChatDeepSeek(
                        model='deepseek-chat',
                        api_key=api_key
                    )
                    
                    if headless:
                        self.status_queue.put("🌐 Starting browser (headless mode)...")
                    else:
                        self.status_queue.put("🌐 Starting visible browser - watch your screen! 👁️")
                    
                    agent = Agent(
                        task=automation_task,
                        llm=llm,
                        headless=headless
                    )
                    
                    if headless:
                        self.status_queue.put("⚡ Executing test automation in background...")
                    else:
                        self.status_queue.put("⚡ Executing test automation - you can watch the browser! 🔍")
                    
                    # Run the automation
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(agent.run())
                    
                    self.status_queue.put("✅ Test automation completed!")
                    
                else:
                    # Demo mode
                    self.status_queue.put("🔧 Running in demo mode with test data...")
                    result = self.run_demo_automation(url, automation_task, test_data)
                
                # Generate report
                self.status_queue.put("📄 Generating test report...")
                report_path = self.generate_test_report(url, automation_task, result, report_name, browser_available)
                
                self.result_queue.put({
                    "success": True,
                    "result": result,
                    "report_path": str(report_path) if report_path else None,
                    "report_dir": str(self.current_report_dir),
                    "mode": "real" if browser_available else "demo",
                    "test_data": test_data
                })
                
            except Exception as e:
                self.status_queue.put(f"❌ Error: {str(e)}")
                self.result_queue.put({
                    "success": False,
                    "error": str(e)
                })
            finally:
                self.running = False
        
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=run_in_thread)
            self.thread.start()
            return True
        return False
    
    def run_demo_automation(self, url, automation_task, test_data=None):
        """Run demo automation with simulated steps and test data"""
        demo_steps = [
            "🌐 Navigating to target URL...",
            "🔍 Analyzing page structure...",
            "� Loading test data context...",
            "�📝 Identifying form fields and inputs...",
            "🔐 Attempting authentication with test credentials...",
            "📋 Filling forms with generated test data...",
            "🔄 Testing form validations and submissions...",
            "📸 Capturing screenshots at each step...",
            "✅ Test execution completed with data validation!"
        ]
        
        for step in demo_steps:
            self.status_queue.put(step)
            time.sleep(2)
        
        test_data_summary = ""
        if test_data:
            data_source = test_data.get('source', 'unknown')
            data_count = len(test_data.get('data', {}))
            test_data_summary = f"""
Test Data Summary ({data_source.upper()} source):
- Data fields available: {data_count}
- Test data used for form filling and validation
- Data source: {data_source}
"""
        
        return f"""Enhanced Demo Test Automation Results:

Target URL: {url}
Automation Task: {automation_task[:200]}...
{test_data_summary}
Simulated Test Execution with Data:
1. Successfully navigated to the target website
2. Loaded and prepared test data for automation
3. Identified interactive elements and form fields
4. Applied test data contextually based on field types
5. Executed validation testing with both valid and invalid data
6. Captured screenshots and documented all interactions
7. Generated comprehensive test results

Test Data Applied:
{json.dumps(test_data.get('data', {}), indent=2) if test_data else "No test data provided"}

Status: Completed (Enhanced Demo Mode)
Note: This is a demonstration with test data integration. Install browser-use and configure DeepSeek API for real automation."""
    
    def generate_test_report(self, url, automation_task, result, report_name, real_mode=True):
        """Generate HTML test report"""
        try:
            mode_badge = "REAL AUTOMATION" if real_mode else "DEMO MODE"
            mode_color = "#28a745" if real_mode else "#ffc107"
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Automation Report - {report_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .mode-badge {{
            background: {mode_color};
            color: {'white' if real_mode else '#212529'};
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
            display: inline-block;
        }}
        .section {{
            padding: 30px;
            border-bottom: 1px solid #eee;
        }}
        .section:last-child {{
            border-bottom: none;
        }}
        .task-content {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
        }}
        .result-content {{
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #28a745;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Test Automation Report</h1>
            <h2>{report_name}</h2>
            <div class="mode-badge">{mode_badge}</div>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="section">
            <h3>🎯 Test Target</h3>
            <p><strong>URL:</strong> <a href="{url}" target="_blank">{url}</a></p>
            <p><strong>Executed:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h3>📋 Automation Task</h3>
            <div class="task-content">{automation_task}</div>
        </div>
        
        <div class="section">
            <h3>📊 Results</h3>
            <div class="result-content">{str(result)}</div>
        </div>
        
        <div class="section">
            <h3>📁 Report Files</h3>
            <ul>
                <li>📄 <strong>{report_name}.html</strong> - This test report</li>
                <li>📁 <strong>Location:</strong> {self.current_report_dir}</li>
            </ul>
        </div>
    </div>
</body>
</html>"""
            
            report_path = self.current_report_dir / f"{report_name}.html"
            report_path.write_text(html_content, encoding='utf-8')
            return report_path
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return None
    
    def get_status(self):
        """Get current status update"""
        try:
            return self.status_queue.get_nowait()
        except queue.Empty:
            return None
    
    def get_result(self):
        """Get automation result"""
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

def main():
    st.title("🤖 JIRA Test Case Generator & Automation")
    st.markdown("Create JIRA issues, generate test cases, and execute them automatically with BrowserClark")
    
    # Initialize session state
    if 'test_runner' not in st.session_state:
        st.session_state.test_runner = BrowserTestRunner()
    if 'test_data_manager' not in st.session_state:
        st.session_state.test_data_manager = TestDataManager()
    if 'automation_status' not in st.session_state:
        st.session_state.automation_status = "Ready"
    if 'automation_result' not in st.session_state:
        st.session_state.automation_result = None
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Get default values from environment
    default_base_url = os.getenv("jira_base_url", "")
    default_username = os.getenv("jira_email", "")
    default_api_key = os.getenv("jira_api_token", os.getenv("jira_key", ""))
    
    with st.sidebar:
        base_url = st.text_input(
            "JIRA Base URL", 
            value=default_base_url,
            placeholder="https://yourcompany.atlassian.net",
            help="Your JIRA instance URL without trailing slash"
        )
        
        username = st.text_input(
            "Email/Username", 
            value=default_username,
            placeholder="your.email@company.com",
            help="Your JIRA email address or username"
        )
        
        api_key = st.text_input(
            "API Key", 
            value=default_api_key,
            type="password",
            help="Your JIRA API token"
        )
        
        project_key = st.text_input(
            "Project Key",
            placeholder="PROJ",
            help="Your JIRA project key (e.g., PROJ, DEV, TEST)"
        )
        
        st.markdown("---")
        st.subheader("🤖 Automation Settings")
        
        deepseek_api_key = st.text_input(
            "DeepSeek API Key",
            type="password",
            value=os.getenv("DEEPSEEK_API_KEY", ""),
            help="API key for browser automation AI"
        )
        
        test_url = st.text_input(
            "Test URL",
            value="https://example.com",
            placeholder="https://your-app.com",
            help="URL where the test automation will run"
        )
        
        st.markdown("**🖥️ Browser Display Mode:**")
        browser_mode = st.radio(
            "Choose how to run the browser:",
            options=["🔍 **Show Browser** (Visible)", "⚡ **Headless** (Hidden)"],
            index=0,  # Default to showing browser
            help="Choose whether to show the browser window during automation"
        )
        headless_mode = "Headless" in browser_mode
        
        if not headless_mode:
            st.success("✅ Browser will be **visible** during test execution")
            st.info("💡 You'll be able to watch the automation in real-time!")
        else:
            st.info("⚡ Browser will run **hidden** (faster execution)")
        
        st.markdown("---")
        st.subheader("🎲 Test Data Configuration")
        
        # Test data mode selection
        data_mode = st.radio(
            "Choose test data source:",
            options=["🎲 **Faker** (Generated)", "📋 **CSV File** (Custom)"],
            index=0,
            help="Choose between auto-generated test data or your own CSV file"
        )
        
        use_faker = "Faker" in data_mode
        
        if use_faker:
            st.success("✅ Using **Faker** for realistic test data generation")
            if not FAKER_AVAILABLE:
                st.warning("⚠️ Faker not installed! Run: `pip install faker`")
        else:
            st.info("📋 Using **Custom CSV** data for testing")
            
            # CSV file upload
            uploaded_file = st.file_uploader(
                "Upload Test Data CSV",
                type=['csv'],
                help="Upload a CSV file with your test data. Column names will be used as field names."
            )
            
            if uploaded_file is not None:
                success, message = st.session_state.test_data_manager.load_csv_data(uploaded_file)
                if success:
                    st.success(message)
                    # Show CSV data preview
                    if st.session_state.test_data_manager.csv_data is not None:
                        st.write("**Data Preview:**")
                        st.dataframe(st.session_state.test_data_manager.csv_data.head(3))
                else:
                    st.error(message)
            else:
                # Show sample CSV template
                if st.button("📥 Download Sample CSV Template"):
                    sample_df = st.session_state.test_data_manager.create_sample_csv_template()
                    csv_string = sample_df.to_csv(index=False)
                    st.download_button(
                        label="Download sample_test_data.csv",
                        data=csv_string,
                        file_name="sample_test_data.csv",
                        mime="text/csv"
                    )
        
        st.markdown("---")
        st.markdown("**API Keys Required:**")
        st.markdown("• **JIRA**: [Get API Token](https://id.atlassian.com/manage-profile/security/api-tokens)")
        st.markdown("• **DeepSeek**: [Get API Key](https://platform.deepseek.com/api_keys)")
    
    # Main tabs
    tab1, tab2 = st.tabs(["🆕 Create New Issue", "📋 Fetch Existing Issue"])
    
    with tab1:
        st.header("Create New JIRA Issue")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            feature_title = st.text_input(
                "Feature Title",
                placeholder="Implement user login feature with OTP verification",
                help="Brief title describing the feature"
            )
            
            feature_description = st.text_area(
                "Feature Description",
                placeholder="Allow users to log in securely using email and password with an OTP sent to their phone.",
                help="Detailed description of the feature"
            )
            
            module = st.text_input(
                "Module",
                placeholder="Authentication & Security",
                help="Which module/component this feature belongs to"
            )
            
            complexity = st.selectbox(
                "Complexity",
                ["Low", "Medium", "High"],
                index=1,
                help="Complexity level of the feature"
            )
            
            # Issue type selection
            issue_type = st.selectbox(
                "Issue Type",
                ["Task", "Bug", "Story", "Epic", "Improvement"],
                index=0,
                help="Type of JIRA issue to create"
            )
            
            # Get available issue types button
            if st.button("� Check Available Issue Types"):
                if all([base_url, username, api_key, project_key]):
                    with st.spinner("Fetching available issue types..."):
                        available_types, error = get_issue_types(base_url, username, api_key, project_key)
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.success("✅ Available issue types:")
                            st.write(", ".join(available_types))
                            st.session_state.available_issue_types = available_types
                else:
                    st.error("Please fill in JIRA credentials and project key first")
            
            if st.button("�🚀 Create JIRA Issue", type="primary"):
                if not all([base_url, username, api_key, project_key, feature_title, feature_description, module]):
                    st.error("Please fill in all required fields including project key in the sidebar")
                else:
                    with st.spinner("Creating JIRA issue..."):
                        issue_key, payload, error = create_jira_issue(
                            base_url, username, api_key, project_key,
                            feature_title, feature_description, module, complexity, issue_type
                        )
                        
                        if error:
                            st.error(f"❌ {error}")
                            if "issuetype" in error.lower():
                                st.info("💡 Try clicking 'Check Available Issue Types' to see what issue types are available for your project")
                        else:
                            st.success(f"✅ Issue created successfully: {issue_key}")
                            st.session_state.created_issue_key = issue_key
                            st.session_state.created_payload = payload
                            st.session_state.created_summary = feature_title
                            st.session_state.created_description = f"Feature Description: {feature_description}\nModule: {module}\nComplexity: {complexity}"
        
        with col2:
            if hasattr(st.session_state, 'created_issue_key'):
                st.subheader(f"📋 Created Issue: {st.session_state.created_issue_key}")
                
                st.subheader("📤 JSON Payload Sent")
                st.json(st.session_state.created_payload)
                
                st.subheader("🧪 Generated Test Case")
                
                # Generate test data based on feature type
                feature_type = st.session_state.test_data_manager.detect_feature_type(
                    st.session_state.created_summary, 
                    st.session_state.created_description
                )
                
                test_data_mode = 'faker' if use_faker else 'csv'
                test_data = st.session_state.test_data_manager.get_test_data(
                    feature_type, 
                    test_data_mode
                )
                
                test_case = generate_test_case(
                    st.session_state.created_issue_key,
                    st.session_state.created_summary,
                    st.session_state.created_description,
                    test_data
                )
                
                st.text_area("Test Case Preview", test_case, height=300, key="created_test_case")
                
                # Action buttons for created issue
                col_save_created, col_download_created, col_run_created = st.columns(3)
                
                with col_save_created:
                    if st.button("💾 Save Test Case", key="save_created"):
                        filename, error = save_test_case(test_case, st.session_state.created_issue_key)
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.success(f"✅ Test case saved as {filename}")
                
                with col_download_created:
                    st.download_button(
                        label="📥 Download Test Case",
                        data=test_case,
                        file_name=f"TestCase_{st.session_state.created_issue_key}.txt",
                        mime="text/plain",
                        key="download_created"
                    )
                
                with col_run_created:
                    run_disabled = not deepseek_api_key or st.session_state.test_runner.running
                    if st.button("🚀 Run Test Steps", disabled=run_disabled, key="run_created"):
                        if not deepseek_api_key:
                            st.error("Please provide DeepSeek API key in sidebar")
                        else:
                            # Show browser mode info
                            if not headless_mode:
                                st.info("🔍 **Browser will be visible** - You can watch the automation!")
                            else:
                                st.info("⚡ **Browser running in background** - Check status below")
                            
                            # Extract test steps and run automation with test data
                            test_steps = st.session_state.test_runner.extract_test_steps(test_case)
                            automation_task = st.session_state.test_runner.convert_test_steps_to_automation_task(
                                test_steps, st.session_state.created_summary, test_url, test_data
                            )
                            
                            st.info(f"🎲 Using {test_data.get('source', 'unknown')} test data with {len(test_data.get('data', {}))} fields")
                            
                            if st.session_state.test_runner.run_browser_automation(
                                test_url, automation_task, deepseek_api_key, headless_mode, test_data
                            ):
                                st.session_state.automation_result = None
                                st.info("🚀 Starting test automation...")
                                st.rerun()
                            else:
                                st.error("Another automation is already running!")
                
                # Show automation status for created issue
                if hasattr(st.session_state, 'created_issue_key'):
                    status_update = st.session_state.test_runner.get_status()
                    if status_update:
                        st.session_state.automation_status = status_update
                    
                    if st.session_state.test_runner.running:
                        if not headless_mode:
                            st.info(f"🔄 {st.session_state.automation_status} | 👁️ **Browser is visible - check your screen!**")
                        else:
                            st.info(f"🔄 {st.session_state.automation_status}")
                    
                    # Check for automation results
                    result = st.session_state.test_runner.get_result()
                    if result:
                        if result["success"]:
                            st.success("🎉 Test automation completed successfully!")
                            if result.get("report_path"):
                                st.success(f"📄 Report generated: {result['report_path']}")
                            st.session_state.automation_result = result
                        else:
                            st.error(f"❌ Test automation failed: {result['error']}")
                        st.rerun()
            else:
                st.info("👈 Fill in the form and click 'Create JIRA Issue' to see the results")
    
    with tab2:
        st.header("Fetch Existing JIRA Issue")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            issue_id = st.text_input(
                "JIRA Issue ID", 
                placeholder="PROJ-123",
                help="Enter the JIRA issue key (e.g., PROJ-123)"
            )
            
            if st.button("🔍 Fetch Issue", type="primary"):
                if not all([base_url, username, api_key, issue_id]):
                    st.error("Please fill in all required fields")
                else:
                    with st.spinner("Fetching JIRA issue..."):
                        summary, description, error = fetch_jira_issue(base_url, username, api_key, issue_id)
                        
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.session_state.summary = summary
                            st.session_state.description = description
                            st.session_state.issue_id = issue_id
                            st.success("✅ Issue fetched successfully!")
        
        with col2:
            # Display fetched issue information
            if hasattr(st.session_state, 'summary') and st.session_state.summary:
                st.subheader("📋 Summary")
                st.write(st.session_state.summary)
                
                st.subheader("📄 Description")
                st.write(st.session_state.description)
                
                # Generate and display test case with test data
                st.subheader("🧪 Generated Test Case")
                
                # Generate test data based on feature type
                feature_type = st.session_state.test_data_manager.detect_feature_type(
                    st.session_state.summary, 
                    st.session_state.description
                )
                
                test_data_mode = 'faker' if use_faker else 'csv'
                test_data = st.session_state.test_data_manager.get_test_data(
                    feature_type, 
                    test_data_mode
                )
                
                test_case = generate_test_case(
                    st.session_state.issue_id, 
                    st.session_state.summary, 
                    st.session_state.description,
                    test_data
                )
                
                st.text_area("Test Case Preview", test_case, height=400, key="fetched_test_case")
                
                # Action buttons for fetched issue
                col_save, col_download, col_run = st.columns(3)
                
                with col_save:
                    if st.button("💾 Save Test Case", key="save_fetched"):
                        filename, error = save_test_case(test_case, st.session_state.issue_id)
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            st.success(f"✅ Test case saved as {filename}")
                
                with col_download:
                    st.download_button(
                        label="📥 Download Test Case",
                        data=test_case,
                        file_name=f"TestCase_{st.session_state.issue_id}.txt",
                        mime="text/plain",
                        key="download_fetched"
                    )
                
                with col_run:
                    run_disabled = not deepseek_api_key or st.session_state.test_runner.running
                    if st.button("🚀 Run Test Steps", disabled=run_disabled, key="run_fetched"):
                        if not deepseek_api_key:
                            st.error("Please provide DeepSeek API key in sidebar")
                        else:
                            # Show browser mode info
                            if not headless_mode:
                                st.info("🔍 **Browser will be visible** - You can watch the automation!")
                            else:
                                st.info("⚡ **Browser running in background** - Check status below")
                            
                            # Extract test steps and run automation with test data
                            test_steps = st.session_state.test_runner.extract_test_steps(test_case)
                            automation_task = st.session_state.test_runner.convert_test_steps_to_automation_task(
                                test_steps, st.session_state.summary, test_url, test_data
                            )
                            
                            st.info(f"🎲 Using {test_data.get('source', 'unknown')} test data with {len(test_data.get('data', {}))} fields")
                            
                            if st.session_state.test_runner.run_browser_automation(
                                test_url, automation_task, deepseek_api_key, headless_mode, test_data
                            ):
                                st.session_state.automation_result = None
                                st.info("🚀 Starting test automation...")
                                st.rerun()
                            else:
                                st.error("Another automation is already running!")
                
                # Show automation status for fetched issue
                if hasattr(st.session_state, 'issue_id'):
                    status_update = st.session_state.test_runner.get_status()
                    if status_update:
                        st.session_state.automation_status = status_update
                    
                    if st.session_state.test_runner.running:
                        if not headless_mode:
                            st.info(f"🔄 {st.session_state.automation_status} | 👁️ **Browser is visible - check your screen!**")
                        else:
                            st.info(f"🔄 {st.session_state.automation_status}")
                    
                    # Check for automation results
                    result = st.session_state.test_runner.get_result()
                    if result:
                        if result["success"]:
                            st.success("🎉 Test automation completed successfully!")
                            if result.get("report_path"):
                                st.success(f"📄 Report generated: {result['report_path']}")
                            st.session_state.automation_result = result
                        else:
                            st.error(f"❌ Test automation failed: {result['error']}")
                        st.rerun()
            else:
                st.info("👆 Enter issue details and click 'Fetch Issue' to generate test case")
    
    # Live status updates
    if st.session_state.test_runner.running:
        time.sleep(1)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 🤖 **Features:**
    - ✅ **Create JIRA Issues** - Generate issues from feature descriptions
    - ✅ **Auto-Generate Test Cases** - Create structured manual test cases
    - ✅ **Browser Automation** - Execute test steps automatically with BrowserClark
    - ✅ **🔍 Visual Browser Mode** - Watch the browser in real-time during testing
    - ✅ **Real-time Status** - Live updates during automation
    - ✅ **Detailed Reports** - Comprehensive HTML reports with screenshots
    
    ### 🔧 **Requirements:**
    - **JIRA API Token** - For issue creation and fetching
    - **DeepSeek API Key** - For AI-powered browser automation
    - **Target URL** - Website where tests will be executed
    
    ### 👁️ **Browser Visibility:**
    - **🔍 Show Browser**: Watch the automation happen in real-time (great for debugging)
    - **⚡ Headless Mode**: Faster execution with browser running in background
    
    💡 **Tip**: Use "Show Browser" mode to see exactly what the AI is doing on your website!
    
    *Built with Streamlit & BrowserClark* 🚀
    """)

if __name__ == "__main__":
    main()