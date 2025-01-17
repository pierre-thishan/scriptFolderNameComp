import os

def generate_directory_file_report(directory, output_file="directory_file_list.txt"):
    """
    Generates a report of all file names in the target directory and subdirectories,
    ignoring files that start with a dot (e.g., `.SYNC`, `.swp`).
    """
    file_list = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if not file_name.startswith("."):  # Ignore dot files
                absolute_path = os.path.abspath(os.path.join(root, file_name))
                file_list.append(absolute_path)

    # Save the directory file list to a report
    with open(output_file, 'w') as f:
        f.write("Directory File List Report\n")
        f.write("=" * 30 + "\n")
        for file_path in sorted(file_list):
            f.write(file_path + "\n")

    print(f"Directory file list report saved to: {os.path.abspath(output_file)}")
    return file_list

def update_golden_list_with_soc(golden_list_path, soc_block_name, debug_file="updated_golden_list.txt"):
    """
    Updates the golden list by replacing placeholders `<...>` with the SOC block name.
    Saves the updated list to a debug file for testing.
    Returns the updated golden list as a set.
    """
    updated_list = set()
    with open(golden_list_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Replace only the placeholders (<...>) with the SOC block name
            if '<' in line and '>' in line:
                updated_line = line.replace(line[line.find('<'):line.find('>') + 1], soc_block_name)
            else:
                updated_line = line  # Keep lines without placeholders unchanged
            updated_list.add(updated_line)

    # Save the updated list to a debug file
    with open(debug_file, 'w') as debug_f:
        debug_f.write("Updated Golden List\n")
        debug_f.write("=" * 30 + "\n")
        for item in sorted(updated_list):
            debug_f.write(item + "\n")

    print(f"Updated golden list saved to: {os.path.abspath(debug_file)}")
    return updated_list

def find_matches_and_mismatches(directory, golden_list):
    """
    Finds both successful matches and mismatches in the directory.
    Returns two lists: matches and mismatches.
    """
    matches = []
    mismatches = []

    for root, _, files in os.walk(directory):
        for file_name in files:
            if not file_name.startswith("."):  # Ignore dot files
                absolute_path = os.path.abspath(os.path.join(root, file_name))
                if file_name in golden_list:
                    matches.append(absolute_path)
                else:
                    mismatches.append(absolute_path)

    return matches, mismatches

def find_directory_only_files(directory_file_list, updated_golden_list):
    """
    Finds files that are in the directory but not present in the reference list (updated golden list).
    """
    directory_files = {os.path.basename(file_path) for file_path in directory_file_list}
    return directory_files - updated_golden_list

def write_report(matches, mismatches, directory_only_files, report_file_1, report_file_2):
    """
    Writes two reports:
    - Report 1: Matches and mismatches.
    - Report 2: Directory-only files (not in the updated golden list).
    """
    # Write matches and mismatches report
    with open(report_file_1, 'w') as f:
        f.write("File Scan Report\n")
        f.write("=" * 30 + "\n\n")

        # Write successful matches
        f.write("Successful Matches:\n")
        f.write("-" * 30 + "\n")
        if matches:
            for match in matches:
                f.write(match + "\n")
        else:
            f.write("No successful matches found.\n")

        f.write("\n")

        # Write mismatches
        f.write("Mismatched Files:\n")
        f.write("-" * 30 + "\n")
        if mismatches:
            for mismatch in mismatches:
                f.write(mismatch + "\n")
        else:
            f.write("No mismatches found.\n")

    print(f"Comparison report saved to: {os.path.abspath(report_file_1)}")

    # Write directory-only files report
    with open(report_file_2, 'w') as f:
        f.write("Directory-Only Files Report\n")
        f.write("=" * 30 + "\n")
        if directory_only_files:
            for file_name in sorted(directory_only_files):
                f.write(file_name + "\n")
        else:
            f.write("No files found in the directory that are not in the reference list.\n")

    print(f"Directory-only files report saved to: {os.path.abspath(report_file_2)}")

def main():
    # User input for SOC block name, directory, and golden list file
    soc_block_name = input("Enter the SOC block name: ").strip()
    directory = input("Enter the directory to scan: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()

    # Report file names
    directory_report_file = "directory_file_list.txt"
    comparison_report_file_1 = "file_scan_report.txt"
    comparison_report_file_2 = "directory_only_files_report.txt"

    # Validate inputs
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return

    # Generate file name report for the directory
    directory_file_list = generate_directory_file_report(directory, directory_report_file)

    # Update golden list with SOC block name and save debug file
    updated_golden_list = update_golden_list_with_soc(golden_list_file, soc_block_name)

    # Find matches and mismatches
    matches, mismatches = find_matches_and_mismatches(directory, updated_golden_list)

    # Find files only in the directory but not in the updated golden list
    directory_only_files = find_directory_only_files(directory_file_list, updated_golden_list)

    # Generate reports
    write_report(matches, mismatches, directory_only_files, comparison_report_file_1, comparison_report_file_2)

if __name__ == "__main__":
    main()
