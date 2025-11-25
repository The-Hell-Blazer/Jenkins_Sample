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
    total_replacement_occurrences = 0
    changed_addresses = set()

    with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
        for line in infile:
            original_line = line
            for old_addr, new_addr in address_map.items():
                pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)

                if re.search(pattern, line):
                    line = re.sub(pattern, new_addr, line)
                    total_replacement_occurrences += 1
                    changed_addresses.add(old_addr)

            updated_lines.append(line)

    with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
        outfile.writelines(updated_lines)

    changed_count = len(changed_addresses)
    unchanged_count = len(address_map) - changed_count

    with open("bar_metrics.csv", "w", encoding="utf-8") as bar_csv:
        bar_csv.write("Category,Count\n")
        bar_csv.write(f"Changed,{changed_count}\n")
        bar_csv.write(f"Unchanged,{unchanged_count}\n")

    html_content = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
    <h3>A2L Address Update Summary</h3>

    <canvas id="barChart" width="400" height="200"></canvas>

    <script>
    var ctx = document.getElementById('barChart').getContext('2d');

    new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: ['Changed', 'Unchanged'],
            datasets: [{{
                label: 'Address Count',
                data: [{changed_count}, {unchanged_count}],
                backgroundColor: ['#4CAF50', '#FF5733']
            }}]
        }},
        options: {{
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
    </script>

    </body>
    </html>
    """

    with open("bar_chart.html", "w", encoding="utf-8") as htmlfile:
        htmlfile.write(html_content)
    with open("update_log.txt", "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
        log.write(f"Unique addresses changed: {changed_count}\n")
        log.write(f"Unchanged addresses: {unchanged_count}\n")
        log.write(f"Total replacement occurrences (all lines): {total_replacement_occurrences}\n")

    print(f" Updated {a2l_file} successfully!")
    print(f" Unique addresses changed: {changed_count}")
    print(f" Unchanged addresses: {unchanged_count}")
    print(f" Total occurrences replaced: {total_replacement_occurrences}")


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






# Plot
# import os
# import shutil
# import datetime
# import configparser
# import re
# import time
# import csv

# def load_address_map(ini_file):
#     config = configparser.ConfigParser()
#     config.optionxform = str  
#     config.read(ini_file, encoding="utf-8")

#     address_map = {}
#     for section in config.sections():
#         for key in config[section]:
#             address_map[key.strip()] = config[section][key].strip()
#     return address_map


# def update_a2l_file(a2l_file, address_map):
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     backup_file = f"{os.path.splitext(a2l_file)[0]}_backup.a2l"

#     file_size_before = os.path.getsize(a2l_file)
#     start_time = time.time()

#     if not os.path.exists(backup_file):
#         shutil.copy(a2l_file, backup_file)
#         print(f" Backup created: {backup_file}")
#     else:
#         print(f" Using existing backup: {backup_file}")

#     updated_lines = []
#     changes = 0

#     with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
#         for line in infile:
#             for old_addr, new_addr in address_map.items():
#                 pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)
#                 if re.search(pattern, line):
#                     line = re.sub(pattern, new_addr, line)
#                     changes += 1
#             updated_lines.append(line)

#     with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
#         outfile.writelines(updated_lines)

#     file_size_after = os.path.getsize(a2l_file)
#     runtime = round(time.time() - start_time, 3)

#     # Write update details to update_log.txt
#     with open("update_log.txt", "a", encoding="utf-8", errors="replace") as log:
#         log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
#         for old_addr, new_addr in address_map.items():
#             log.write(f"{old_addr} → {new_addr}\n")
#         log.write(f"Total replacements: {changes}\n")

#     metrics_file = "metrics.csv"
#     create_header = not os.path.exists(metrics_file)

#     with open(metrics_file, "a", newline='') as csvfile:
#         writer = csv.writer(csvfile)

#         if create_header:
#             writer.writerow(["timestamp", "changes", "file_size_before", "file_size_after", "runtime_sec"])

#         writer.writerow([timestamp, changes, file_size_before, file_size_after, runtime])

#     print(f" Updated {a2l_file} successfully! Total replacements: {changes}")
#     print(f" Metrics logged to metrics.csv")


# def main():
#     ini_file = "address.ini"
#     a2l_file = next((f for f in os.listdir(".") if f.endswith(".a2l") and not f.startswith("a2l_updater")), None)

#     if not a2l_file:
#         print(" No .a2l file found in the current directory.")
#         return

#     if not os.path.exists(ini_file):
#         print(" address.ini file not found.")
#         return

#     address_map = load_address_map(ini_file)
#     print(f"Loaded {len(address_map)} address mappings from {ini_file}")
#     update_a2l_file(a2l_file, address_map)


# if __name__ == "__main__":
#     main()

# OG
# import os
# import shutil
# import datetime
# import configparser
# import re

# def load_address_map(ini_file):
#     config = configparser.ConfigParser()
#     config.optionxform = str  
#     config.read(ini_file, encoding="utf-8")

#     address_map = {}
#     for section in config.sections():
#         for key in config[section]:
#             address_map[key.strip()] = config[section][key].strip()
#     return address_map


# def update_a2l_file(a2l_file, address_map):
#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     backup_file = f"{os.path.splitext(a2l_file)[0]}_backup.a2l"

#     if not os.path.exists(backup_file):
#         shutil.copy(a2l_file, backup_file)
#         print(f" Backup created: {backup_file}")
#     else:
#         print(f" Using existing backup: {backup_file}")

#     updated_lines = []
#     changes = 0

#     with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
#         for line in infile:
#             original_line = line
#             for old_addr, new_addr in address_map.items():
#                 pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)
#                 if re.search(pattern, line):
#                     line = re.sub(pattern, new_addr, line)
#                     changes += 1
#             updated_lines.append(line)

#     with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
#         outfile.writelines(updated_lines)

#     with open("update_log.txt", "a", encoding="utf-8", errors="replace") as log:
#         log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
#         for old_addr, new_addr in address_map.items():
#             log.write(f"{old_addr} → {new_addr}\n")
#         log.write(f"Total replacements: {changes}\n")

#     print(f" Updated {a2l_file} successfully! Total replacements: {changes}")


# def main():
#     ini_file = "address.ini"
#     a2l_file = next((f for f in os.listdir(".") if f.endswith(".a2l") and not f.startswith("a2l_updater")), None)

#     if not a2l_file:
#         print(" No .a2l file found in the current directory.")
#         return

#     if not os.path.exists(ini_file):
#         print(" address.ini file not found.")
#         return

#     address_map = load_address_map(ini_file)
#     print(f"Loaded {len(address_map)} address mappings from {ini_file}")
#     update_a2l_file(a2l_file, address_map)


# if __name__ == "__main__":
#     main()
