import os

def update_golden_list_with_soc(golden_list_path, soc_block_name):
    """
    Updates the golden list by replacing the placeholder `<...>` with the SOC block name.
    Returns the updated golden list as a set.
    """
    updated_list = set()
    with open(golden_list_path, 'r') as f:
        for line in f:
            updated_line = line.strip().replace('<>', soc_block_name)
            updated_list.add(updated_line)
    return updated_list

def find_mismatches(directory, golden_list):
    """Finds mismatched file names in the directory and subdirectories."""
    mismatches = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name not in golden_list:
                absolute_path = os.path.abspath(os.path.join(root, file_name))
                mismatches.append(absolute_path)

    return mismatches

def write_report(mismatches, report_file):
    """Writes the list of mismatched files to the report file."""
    with open(report_file, 'w') as f:
        f.write("Mismatched Files Report\n")
        f.write("=" * 30 + "\n")
        for mismatch in mismatches:
            f.write(mismatch + "\n")
    print(f"Report written to: {os.path.abspath(report_file)}")

def main():
    # User input for SOC block name, directory, and golden list file
    soc_block_name = input("Enter the SOC block name: ").strip()
    directory = input("Enter the directory to scan: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()
    report_file = "mismatched_files_report.txt"

    # Validate inputs
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return

    # Update golden list with SOC block name
    golden_list = update_golden_list_with_soc(golden_list_file, soc_block_name)

    # Find mismatches
    mismatches = find_mismatches(directory, golden_list)

    # Generate report
    if mismatches:
        write_report(mismatches, report_file)
    else:
        print("No mismatches found. All file names match the updated golden list.")

if __name__ == "__main__":
    main()
