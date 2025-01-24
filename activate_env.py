import os
import subprocess
import sys

def install_python():
    """Install Python 3 if not already installed."""
    try:
        # Check if Python 3 is installed
        subprocess.check_call(["python3", "--version"])
        print("Python 3 is already installed.")
    except subprocess.CalledProcessError:
        print("Python 3 not found, installing...")
        # Install Python 3
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3", "python3-pip"])
        print("Python 3 installed successfully.")

def install_git():
    """Install Git if not already installed."""
    try:
        # Check if Git is installed
        subprocess.check_call(["git", "--version"])
        print("Git is already installed.")
    except subprocess.CalledProcessError:
        print("Git not found, installing...")
        # Install Git
        subprocess.check_call(["sudo", "apt", "install", "-y", "git"])
        print("Git installed successfully.")

def update_and_upgrade_os():
    """Update and upgrade the OS."""
    try:
        print("Updating and upgrading the OS...")
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "upgrade", "-y"])
        print("OS updated and upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating/upgrading OS: {e}")
        sys.exit(1)

def create_virtualenv(venv_name="rudrarakshak"):
    """Create a virtual environment."""
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])
        print(f"Virtual environment '{venv_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        sys.exit(1)

def activate_virtualenv(venv_name="rudrarakshak"):
    """Activate the virtual environment."""
    if os.name == "nt":  # For Windows
        activate_script = os.path.join(venv_name, "Scripts", "activate")
    else:  # For Unix-based systems
        activate_script = os.path.join(venv_name, "bin", "activate")
    
    if os.path.exists(activate_script):
        print(f"To activate the virtual environment, run: \nsource {activate_script}")
    else:
        print(f"Could not find the activation script. Make sure the environment was created successfully.")

def main():
    # Perform OS update and upgrade
    update_and_upgrade_os()

    # Install Python and Git if not present
    install_python()
    install_git()

    # Create and activate the virtual environment
    venv_name = "rudrarakshak"  # Default virtual environment name
    create_virtualenv(venv_name)
    activate_virtualenv(venv_name)

if __name__ == "__main__":
    main()
