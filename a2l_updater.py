import os
import shutil
import datetime
import configparser

def load_address_map(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file, encoding='utf-8')
    address_map = {}
    for section in config.sections():
        for key in config[section]:
            address_map[key.upper()] = config[section][key]
    return address_map

def update_a2l_file(a2l_file, address_map):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{os.path.splitext(a2l_file)[0]}_backup_{timestamp}.a2l"
    shutil.copy(a2l_file, backup_file)
    print(f"Backup created: {backup_file}")

    updated_lines = []
    with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
        for line in infile:
            for var, new_addr in address_map.items():
                if var in line:
                    print(f"Updating {var} → {new_addr}")
                    line = line.replace(var, new_addr)
            updated_lines.append(line)

    with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
        outfile.writelines(updated_lines)

    with open("update_log.txt", "w", encoding="utf-8", errors="replace") as log:
        log.write(f"Updated {a2l_file} at {timestamp}\n")
        for var, new_addr in address_map.items():
            log.write(f"{var} → {new_addr}\n")

    print(f"Updated {a2l_file} successfully!")

def main():
    ini_file = "address.ini"
    a2l_file = next((f for f in os.listdir(".") if f.endswith(".a2l")), None)

    if not a2l_file:
        print("❌ No .a2l file found in the current directory.")
        return

    address_map = load_address_map(ini_file)
    print(f"Loaded {len(address_map)} address mappings from {ini_file}")
    update_a2l_file(a2l_file, address_map)

if __name__ == "__main__":
    main()
