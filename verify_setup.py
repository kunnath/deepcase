#!/usr/bin/env python3
"""
Installation verification script for JIRA Test Case Generator & Automation
Run this script to verify all dependencies are properly installed.
"""

import sys
import importlib.util

def check_module(module_name, install_name=None):
    """Check if a module is installed and importable"""
    install_name = install_name or module_name
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False, f"❌ {module_name} not found. Install with: pip install {install_name}"
        
        # Try to actually import it
        module = importlib.import_module(module_name)
        version = getattr(module, '__version__', 'unknown')
        return True, f"✅ {module_name} {version}"
    except Exception as e:
        return False, f"❌ {module_name} error: {str(e)}"

def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # Try to get browser path to verify installation
            try:
                browser_path = p.chromium.executable_path
                return True, f"✅ Playwright browsers installed at {browser_path}"
            except Exception:
                return False, "❌ Playwright browsers not installed. Run: playwright install"
    except Exception as e:
        return False, f"❌ Playwright check failed: {str(e)}"

def main():
    print("🔍 JIRA Test Case Generator - Installation Verification")
    print("=" * 60)
    
    # Required modules
    modules = [
        ("streamlit", "streamlit>=1.28.0"),
        ("requests", "requests>=2.31.0"),
        ("dotenv", "python-dotenv>=1.0.0"),
        ("browser_use", "browser-use>=0.9.5"),
        ("playwright", "playwright>=1.55.0"),
        ("anthropic", "anthropic>=0.68.1"),
        ("openai", "openai>=1.99.2"),
        ("aiohttp", "aiohttp>=3.12.0"),
        ("bs4", "beautifulsoup4>=4.9.0"),
        ("PIL", "pillow>=11.2.0"),
    ]
    
    print("\n📦 Checking Python packages:")
    all_good = True
    for module, install_name in modules:
        success, message = check_module(module, install_name)
        print(f"  {message}")
        if not success:
            all_good = False
    
    print("\n🌐 Checking Playwright browsers:")
    success, message = check_playwright_browsers()
    print(f"  {message}")
    if not success:
        all_good = False
    
    print("\n📁 Checking configuration files:")
    import os
    if os.path.exists('.env'):
        print("  ✅ .env file found")
        # Check if it has required keys
        with open('.env', 'r') as f:
            content = f.read()
            if 'DEEPSEEK_API_KEY' in content:
                print("  ✅ DEEPSEEK_API_KEY found in .env")
            else:
                print("  ⚠️  DEEPSEEK_API_KEY not found in .env (required for automation)")
                all_good = False
            
            if 'jira_api_token' in content:
                print("  ✅ jira_api_token found in .env")
            else:
                print("  ⚠️  jira_api_token not found in .env (required for JIRA)")
                all_good = False
    else:
        print("  ❌ .env file not found. Copy .env.example to .env and configure")
        all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 All dependencies installed correctly!")
        print("🚀 You can now run: streamlit run jira_test_generator.py")
    else:
        print("❌ Some dependencies are missing. Please install them and try again.")
        print("📖 See README.md for detailed installation instructions.")
    
    print("\n💡 Quick start:")
    print("   1. Configure your .env file with API keys")
    print("   2. Run: streamlit run jira_test_generator.py")
    print("   3. Open browser to http://localhost:8501")

if __name__ == "__main__":
    main()