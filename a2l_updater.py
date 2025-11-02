import os
import re
import configparser
import subprocess
from datetime import datetime

def find_a2l_file():
    """Find the first .a2l file in the current directory."""
    for file in os.listdir('.'):
        if file.endswith('.a2l'):
            return file
    raise FileNotFoundError("No .a2l file found in the current directory.")

def load_address_mappings(ini_file):
    """Read the address mappings from address.ini"""
    config = configparser.ConfigParser()
    config.read(ini_file)
    address_map = {}
    for section in config.sections():
        for key, value in config.items(section):
            address_map[key] = value
    return address_map

def update_a2l_file(a2l_file, address_map):
    """Replace addresses in the .a2l file and create a new one."""
    # Create backup
    backup_file = a2l_file.replace('.a2l', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.a2l')
    os.rename(a2l_file, backup_file)
    print(f"Backup created: {backup_file}")

    # Read backup content
    with open(backup_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Replace addresses
    for old_addr, new_addr in address_map.items():
        pattern = re.compile(rf'\b{old_addr}\b', re.IGNORECASE)
        content = pattern.sub(new_addr, content)

    # Write updated file
    new_file = a2l_file  # same name as original
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated .a2l file generated: {new_file}")
    return new_file, backup_file

def git_commit_and_push(files, message="Updated A2L addresses via Jenkins"):
    """Commit and push changes back to the repo."""
    try:
        subprocess.run(["git", "config", "--global", "user.email", "jenkins@automation.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Jenkins Automation"], check=True)
        subprocess.run(["git", "add"] + files, check=True)
        subprocess.run(["git", "commit", "-m", message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed to remote repository successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

def main():
    ini_file = "address.ini"

    if not os.path.exists(ini_file):
        raise FileNotFoundError("address.ini file not found in the repository.")

    a2l_file = find_a2l_file()
    print(f"Found A2L file: {a2l_file}")

    address_map = load_address_mappings(ini_file)
    print(f"Loaded {len(address_map)} address mappings from {ini_file}")

    new_a2l, backup_a2l = update_a2l_file(a2l_file, address_map)

    # Commit both backup and updated file
    git_commit_and_push([new_a2l, backup_a2l], "A2L address update automated via Jenkins")

if __name__ == "__main__":
    main()
