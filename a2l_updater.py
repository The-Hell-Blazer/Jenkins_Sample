import os
import shutil
import datetime
import configparser
import re

def load_address_map(ini_file):
    config = configparser.ConfigParser()
    config.optionxform = str  
    config.read(ini_file, encoding="utf-8")

    address_map = {}
    for section in config.sections():
        for key in config[section]:
            address_map[key.strip()] = config[section][key].strip()
    return address_map


def update_a2l_file(a2l_file, address_map):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{os.path.splitext(a2l_file)[0]}_backup.a2l"

    if not os.path.exists(backup_file):
        shutil.copy(a2l_file, backup_file)
        print(f" Backup created: {backup_file}")
    else:
        print(f" Using existing backup: {backup_file}")

    updated_lines = []
    changes = 0

    with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
        for line in infile:
            original_line = line
            for old_addr, new_addr in address_map.items():
                pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)
                if re.search(pattern, line):
                    line = re.sub(pattern, new_addr, line)
                    changes += 1
            updated_lines.append(line)

    with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
        outfile.writelines(updated_lines)

    with open("update_log.txt", "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
        for old_addr, new_addr in address_map.items():
            log.write(f"{old_addr} → {new_addr}\n")
        log.write(f"Total replacements: {changes}\n")

    print(f" Updated {a2l_file} successfully! Total replacements: {changes}")


def main():
    ini_file = "address.ini"
    a2l_file = next((f for f in os.listdir(".") if f.endswith(".a2l") and not f.startswith("a2l_updater")), None)

    if not a2l_file:
        print(" No .a2l file found in the current directory.")
        return

    if not os.path.exists(ini_file):
        print(" address.ini file not found.")
        return

    address_map = load_address_map(ini_file)
    print(f"Loaded {len(address_map)} address mappings from {ini_file}")
    update_a2l_file(a2l_file, address_map)


if __name__ == "__main__":
    main()
