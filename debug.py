import os

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
            absolute_path = os.path.abspath(os.path.join(root, file_name))
            if file_name in golden_list:
                matches.append(absolute_path)
            else:
                mismatches.append(absolute_path)

    return matches, mismatches

def write_report(matches, mismatches, report_file):
    """
    Writes the successful matches and mismatches to the report file.
    """
    with open(report_file, 'w') as f:
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

    print(f"Report written to: {os.path.abspath(report_file)}")

def main():
    # User input for SOC block name, directory, and golden list file
    soc_block_name = input("Enter the SOC block name: ").strip()
    directory = input("Enter the directory to scan: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()
    report_file = "file_scan_report.txt"

    # Validate inputs
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return

    # Update golden list with SOC block name and save debug file
    golden_list = update_golden_list_with_soc(golden_list_file, soc_block_name)

    # Find matches and mismatches
    matches, mismatches = find_matches_and_mismatches(directory, golden_list)

    # Generate report
    write_report(matches, mismatches, report_file)

if __name__ == "__main__":
    main()
