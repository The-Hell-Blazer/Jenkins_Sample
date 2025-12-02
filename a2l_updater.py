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
            clean_key = key.strip().lower()
            clean_val = config[section][key].strip().lower()
            address_map[clean_key] = clean_val

    print("DEBUG address_map:", address_map)
    return address_map


def update_a2l_file(a2l_file, address_map):
    report_dir = "."

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = "sample_backup.a2l"
    shutil.copy(a2l_file, backup_file)
    print(f" Backup saved: {backup_file}")

    updated_lines = []
    changed_pairs_dict = {}  # old_addr -> new_addr (unique)

    with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
        for line in infile:
            # Only attempt replacement if line contains ECU_ADDRESS
            if "ecu_address" in line.lower():
                for old_addr, new_addr in address_map.items():
                    pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)
                    new_line = re.sub(pattern, new_addr, line)

                    if new_line != line:
                        line = new_line
                        # Record unique changed address
                        if old_addr not in changed_pairs_dict:
                            changed_pairs_dict[old_addr] = new_addr

            updated_lines.append(line)

    with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
        outfile.writelines(updated_lines)

    changed_count = len(changed_pairs_dict)
    unchanged_count = len(address_map) - changed_count

    # Create bar metrics CSV
    metrics_file = os.path.join(report_dir, "bar_metrics.csv")
    with open(metrics_file, "w", encoding="utf-8") as bar_csv:
        bar_csv.write("Category,Count\n")
        bar_csv.write(f"Changed,{changed_count}\n")
        bar_csv.write(f"Unchanged,{unchanged_count}\n")

    # Create HTML report
    html_content = f"""  
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>

    <h3>Address Change Analysis Report</h3>

    <canvas id="barChart" width="750" height="750"></canvas>

    <script>
    var ctx = document.getElementById('barChart').getContext('2d');

    new Chart(ctx, {{
        type: 'bar',
        data: {{
            labels: ['Changed', 'Unchanged'],
            datasets: [{{
                label: 'Address Count',
                data: [{changed_count}, {unchanged_count}],
                backgroundColor: ['#4CAF50', '#FF5733'],
                barPercentage: 0.6,
                categoryPercentage: 0.6
            }}]
        }},
        options: {{
            responsive: false,
            plugins: {{
                legend: {{
                    display: false 
                }}
            }},
            scales: {{
                x: {{
                    grid: {{ display: false }},
                    title: {{
                        display: true,
                        text: "Address"
                    }}
                }},
                y: {{
                    beginAtZero: true,
                    min: 0,
                    max: 10,
                    ticks: {{
                        stepSize: 1
                    }},
                    title: {{
                        display: true,
                        text: "Address Count"
                    }}
                }}
            }}
        }}
    }});
    </script>

    </body>
    </html>
    """

    html_report_path = os.path.join(report_dir, "Address_Change_Analysis_Report.html")
    with open(html_report_path, "w", encoding="utf-8") as htmlfile:
        htmlfile.write(html_content)

    # Write log
    log_file = os.path.join(report_dir, "update_log.txt")
    with open(log_file, "a", encoding="utf-8", errors="replace") as log:
        log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
        log.write(f"Unique addresses changed: {changed_count}\n")
        log.write(f"Unchanged addresses: {unchanged_count}\n\n")  # newline added
        if changed_pairs_dict:
            log.write("Changed Address Pairs:\n")
            for old, new in changed_pairs_dict.items():
                log.write(f"{old} → {new}\n")

    # Console output
    print(f" Updated {a2l_file} successfully!")
    print(f" Unique addresses changed: {changed_count}")
    print(f" Unchanged addresses: {unchanged_count}\n")  # newline for readability

    if changed_pairs_dict:
        print(" Changed Address Pairs:")
        for old, new in changed_pairs_dict.items():
            print(f" {old} -> {new}")

    print(f"HTML report: {html_report_path}")


def main():
    ini_file = "address.ini"
    a2l_file = "sample.a2l"

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
#             clean_key = key.strip().lower()
#             clean_val = config[section][key].strip().lower()
#             address_map[clean_key] = clean_val

#     print("DEBUG address_map:", address_map)
#     return address_map


# def update_a2l_file(a2l_file, address_map):
#     report_dir = "."

#     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     backup_file = "sample_backup.a2l"
#     shutil.copy(a2l_file, backup_file)
#     print(f" Backup saved: {backup_file}")

#     updated_lines = []
#     total_replacement_occurrences = 0
#     changed_addresses = set()

#     with open(a2l_file, "r", encoding="utf-8", errors="replace") as infile:
#         for line in infile:
#             original_line = line
#             for old_addr, new_addr in address_map.items():
#                 if "ecu_address" in original_line.lower():
#                     pattern_exact = re.compile(rf'\bECU_ADDRESS\s+{re.escape(old_addr)}\b', re.IGNORECASE)
#                     if re.search(pattern_exact, original_line):
#                         changed_addresses.add(old_addr)

#                     pattern = re.compile(rf'\b{re.escape(old_addr)}\b', re.IGNORECASE)
#                     new_line = re.sub(pattern, new_addr, line)

#                     if new_line != line:
#                         total_replacement_occurrences += 1
#                         line = new_line

#             updated_lines.append(line)

#     with open(a2l_file, "w", encoding="utf-8", errors="replace") as outfile:
#         outfile.writelines(updated_lines)

#     changed_count = len(changed_addresses)
#     unchanged_count = len(address_map) - changed_count

#     metrics_file = os.path.join(report_dir, "bar_metrics.csv")
#     with open(metrics_file, "w", encoding="utf-8") as bar_csv:
#         bar_csv.write("Category,Count\n")
#         bar_csv.write(f"Changed,{changed_count}\n")
#         bar_csv.write(f"Unchanged,{unchanged_count}\n")

#     html_content = f"""  
#     <html>
#     <head>
#         <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
#     </head>
#     <body>

#     <h3>Address Change Analysis Report</h3>

#     <canvas id="barChart" width="750" height="750"></canvas>

#     <script>
#     var ctx = document.getElementById('barChart').getContext('2d');

#     new Chart(ctx, {{
#         type: 'bar',
#         data: {{
#             labels: ['Changed', 'Unchanged'],
#             datasets: [{{
#                 label: 'Address Count',
#                 data: [{changed_count}, {unchanged_count}],
#                 backgroundColor: ['#4CAF50', '#FF5733'],
#                 barPercentage: 0.6,
#                 categoryPercentage: 0.6
#             }}]
#         }},
#         options: {{
#             responsive: false,
#             plugins: {{
#                 legend: {{
#                     display: false 
#                 }}
#             }},
#             scales: {{
#                 x: {{
#                     grid: {{ display: false }},
#                     title: {{
#                         display: true,
#                         text: "Address"
#                     }}
#                 }},
#                 y: {{
#                     beginAtZero: true,
#                     min: 0,
#                     max: 10,
#                     ticks: {{
#                         stepSize: 1
#                     }},
#                     title: {{
#                         display: true,
#                         text: "Address Count"
#                     }}
#                 }}
#             }}
#         }}
#     }});
#     </script>

#     </body>
#     </html>
#     """

#     html_report_path = os.path.join(report_dir, "Address_Change_Analysis_Report.html")
#     with open(html_report_path, "w", encoding="utf-8") as htmlfile:
#         htmlfile.write(html_content)

#     log_file = os.path.join(report_dir, "update_log.txt")
#     with open(log_file, "a", encoding="utf-8", errors="replace") as log:
#         log.write(f"\nUpdated {a2l_file} at {timestamp}\n")
#         log.write(f"Unique addresses changed: {changed_count}\n")
#         log.write(f"Unchanged addresses: {unchanged_count}\n")
#         log.write(f"Total replacement occurrences: {total_replacement_occurrences}\n")

#     print(f" Updated {a2l_file} successfully!")
#     print(f" Unique addresses changed: {changed_count}")
#     print(f" Unchanged addresses: {unchanged_count}")
#     print(f" Total occurrences replaced: {total_replacement_occurrences}")
#     print(f"HTML report: {html_report_path}")


# def main():
#     ini_file = "address.ini"
#     a2l_file = "sample.a2l"

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
