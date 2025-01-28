import os
import subprocess
import sys

def run_command(command, description):
    """Run a system command with error handling."""
    try:
        subprocess.run(command, check=True)
        print(f"{description} succeeded.")
    except subprocess.CalledProcessError as e:
        print(f"{description} failed with error: {e}")
        sys.exit(1)

def install_python():
    """Install Python 3 and required tools if not already installed."""
    print("Checking for Python 3...")
    if subprocess.run(["python3", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        print("Python 3 is already installed.")
    else:
        print("Python 3 not found, installing...")
        run_command(["sudo", "apt-get", "install", "-y", "python3", "python3-pip"], "Installing Python 3 and pip")

    print("Checking for python3-venv...")
    if subprocess.run(["dpkg", "-s", "python3-venv"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        print("python3-venv is already installed.")
    else:
        print("python3-venv not found, installing...")
        run_command(["sudo", "apt-get", "install", "-y", "python3-venv"], "Installing python3-venv")

def install_git():
    """Install Git if not already installed."""
    print("Checking for Git...")
    if subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
        print("Git is already installed.")
    else:
        print("Git not found, installing...")
        run_command(["sudo", "apt-get", "install", "-y", "git"], "Installing Git")

def update_and_upgrade_os():
    """Update and upgrade the OS."""
    print("Updating and upgrading the OS...")
    run_command(["sudo", "apt-get", "update"], "Updating package lists")
    run_command(["sudo", "apt-get", "upgrade", "-y"], "Upgrading packages")

def create_virtualenv(venv_name="rudrarakshak"):
    """Create a virtual environment."""
    print(f"Creating virtual environment: {venv_name}...")
    run_command([sys.executable, "-m", "venv", venv_name], f"Creating virtual environment '{venv_name}'")

def activate_virtualenv(venv_name="rudrarakshak"):
    """Provide instructions to activate the virtual environment."""
    if os.name == "nt":  # For Windows
        activate_script = os.path.join(venv_name, "Scripts", "activate")
    else:  # For Unix-based systems
        activate_script = os.path.join(venv_name, "bin", "activate")
    
    if os.path.exists(activate_script):
        print(f"To activate the virtual environment, run: \nsource {activate_script}")
    else:
        print(f"Could not find the activation script. Ensure the environment was created successfully.")

def main():
    """Main function to orchestrate the setup process."""
    # Perform OS update and upgrade
    update_and_upgrade_os()

    # Install Python and Git if not present
    install_python()
    install_git()

    # Create and guide virtual environment activation
    venv_name = "rudrarakshak"
    create_virtualenv(venv_name)
    activate_virtualenv(venv_name)

if __name__ == "__main__":
    main()
