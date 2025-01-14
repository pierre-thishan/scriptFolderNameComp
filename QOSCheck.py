import os

def read_golden_list(file_path):
    """Reads the golden list from the given file."""
    with open(file_path, 'r') as f:
        return {line.strip() for line in f}

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
    # User input for directory and golden list file
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

    # Read golden list
    golden_list = read_golden_list(golden_list_file)

    # Find mismatches
    mismatches = find_mismatches(directory, golden_list)

    # Generate report
    if mismatches:
        write_report(mismatches, report_file)
    else:
        print("No mismatches found. All file names match the golden list.")

if __name__ == "__main__":
    main()
