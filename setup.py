#!/usr/bin/env python3
"""
Setup script for Your Palette Flask Application
This script will help set up the virtual environment and dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print the result"""
    print(f"\n{'='*50}")
    print(f"Step: {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🎨 Your Palette Flask Application Setup")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    # Create virtual environment
    if not run_command("python3 -m venv venv", "Creating virtual environment"):
        print("Trying with 'python' instead of 'python3'...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            print("❌ Failed to create virtual environment. Please install Python 3.7+")
            sys.exit(1)
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Initialize database
    init_script = '''
import app
with app.app.app_context():
    app.init_db()
    print("Database initialized with sample products!")
    print(f"Total products: {app.Product.query.count()}")
'''
    
    with open('temp_init.py', 'w') as f:
        f.write(init_script)
    
    if run_command(f"{python_cmd} temp_init.py", "Initializing database"):
        os.remove('temp_init.py')
    
    print("\n" + "="*50)
    print("🎉 Setup Complete!")
    print("="*50)
    print("\nTo run the application:")
    print("1. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the Flask app:")
    print("   python app.py")
    print("3. Open your browser to: http://127.0.0.1:5000")
    print("\nOr run directly with:")
    print(f"   {python_cmd} app.py")

if __name__ == "__main__":
    main()