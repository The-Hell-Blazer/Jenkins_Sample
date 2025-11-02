import os
import re
import configparser
from datetime import datetime

def find_a2l_file():
    for file in os.listdir('.'):
        if file.endswith('.a2l'):
            return file
    raise FileNotFoundError("No .a2l file found in the current directory.")

def load_address_mappings(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    address_map = {}
    for section in config.sections():
        for key, value in config.items(section):
            address_map[key] = value
    return address_map

def update_a2l_file(a2l_file, address_map):
    backup_file = a2l_file.replace('.a2l', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.a2l')
    os.rename(a2l_file, backup_file)
    print(f"Backup created: {backup_file}")

    with open(backup_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    replacements = []
    for old_addr, new_addr in address_map.items():
        pattern = re.compile(rf'\b{old_addr}\b', re.IGNORECASE)
        if pattern.search(content):
            content = pattern.sub(new_addr, content)
            replacements.append(f"{old_addr} → {new_addr}")

    new_file = a2l_file 
    with open(new_file, 'w', encoding='utf-8') as f:
        f.write(content)

    with open("address_update.log", "w") as log:
        log.write("Address Update Log\n")
        log.write("===================\n")
        for line in replacements:
            log.write(line + "\n")

    print(f"Updated .a2l file generated: {new_file}")
    print("Replacements written to address_update.log")
    return new_file, backup_file

def main():
    ini_file = "address.ini"
    if not os.path.exists(ini_file):
        raise FileNotFoundError("address.ini file not found in the repository.")

    a2l_file = find_a2l_file()
    print(f"Found A2L file: {a2l_file}")

    address_map = load_address_mappings(ini_file)
    print(f"Loaded {len(address_map)} address mappings from {ini_file}")

    update_a2l_file(a2l_file, address_map)

if __name__ == "__main__":
    main()
