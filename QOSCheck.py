import os

DEFAULT_MODES = {"FUNC", "ATPG_SHIFT", "ATPG_STUCKAT", "ATPG_ATSPEED"} # USER can input more modes as comma seperated.


def generate_directory_file_report(directory, output_file="directory_file_list.txt"):
    """
    Generates a report of all file names in the target directory and subdirectories,
    ignoring files that start with a dot (e.g., `.SYNC`, `.swp`).
    """
    file_list = []

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".")] # To ignore hidden directories.
        dirs[:] = [d for d in dirs if d !="tool_data" ] #USER can enter directory names to be dropped if needed . TO DO :) 
        dirs[:] = [d for d in dirs if d !="STUB" ]
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

    print(
        f"Directory file list report saved to: {os.path.abspath(output_file)}")
    return file_list


def update_golden_list_with_modes(golden_list_path, soc_block_name, user_modes=None, debug_file="updated_golden_list.txt"):
    """
    Updates the golden list by replacing placeholders `<...>` with SOC block name
    and `<mode>` with default modes or user-provided modes.
    """
    if user_modes:
        mode_list = DEFAULT_MODES.union(user_modes)
    else:
        mode_list = DEFAULT_MODES

    updated_list = set()
    with open(golden_list_path, 'r') as f:
        for line in f:
            line = line.strip()
            if "<anamix>" in line:
                # Replace `<...>` with SOC block name
                updated_line = line.replace(
                    line[line.find('<'):line.find('>') + 1], soc_block_name)

                # Handle `<mode>` expansion
                if "<mode>" in updated_line:
                    for mode in mode_list:
                        updated_list.add(updated_line.replace("<mode>", mode))
                else:
                    updated_list.add(updated_line)
            else:
                if "<mode>" in updated_line:
                    for mode in mode_list:
                        updated_list.add(line.replace("<mode>", mode))
                else:
                    updated_list.add(line)

    # Save the updated list to a debug file
    with open(debug_file, 'w') as debug_f:
        debug_f.write("Updated Golden List with Modes\n")
        debug_f.write("=" * 30 + "\n")
        for item in sorted(updated_list):
            debug_f.write(item + "\n")

    print(f"Updated golden list saved to: {os.path.abspath(debug_file)}")
    return updated_list


def find_matches_and_mismatches(directory_file_list, updated_golden_list):
    """
    Finds both successful matches and mismatches between the directory files and the updated golden list.
    """
    matches = []
    mismatches = []

    # Extract file names from the directory list
    directory_file_names = {os.path.basename(file_path) for file_path in directory_file_list}

    for file_name in directory_file_names:
        if file_name in updated_golden_list:
            matches.append(file_name)
        else:
            mismatches.append(file_name)

    return matches, mismatches


def write_report(matches, mismatches, report_file="file_comparison_report.txt"):
    """
    Writes a report that includes the success rate, matched files, and mismatched files.
    """
    total_files = len(matches) + len(mismatches)
    success_rate = (len(matches) / total_files) * 100 if total_files > 0 else 0

    with open(report_file, 'w') as f:
        f.write("File Comparison Report\n")
        f.write("=" * 30 + "\n\n")

        f.write(f"Total Files: {total_files}\n")
        f.write(f"Successful Matches: {len(matches)}\n")
        f.write(f"Mismatches: {len(mismatches)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n\n")

        f.write("Matched Files:\n")
        f.write("-" * 30 + "\n")
        for match in sorted(matches):
            f.write(match + "\n")

        f.write("\nMismatched Files:\n")
        f.write("-" * 30 + "\n")
        for mismatch in sorted(mismatches):
            f.write(mismatch + "\n")

    print(f"File comparison report saved to: {os.path.abspath(report_file)}")


def main():
    # User input for SOC block name, directory, golden list file, and additional modes
    soc_block_name = input("Enter the SOC block name: ").strip()
    directory = input("Enter the directory to scan: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()
    additional_modes = input("Enter additional modes (comma-separated) or press Enter to skip: ").strip()

    # Process additional modes
    user_modes = set(additional_modes.split(',')) if additional_modes else None

    # Validate inputs
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return

    # Generate file name report for the directory
    directory_report_file = "directory_file_list.txt"
    directory_file_list = generate_directory_file_report(directory, directory_report_file)

    # Update golden list with SOC block name and modes
    updated_golden_list = update_golden_list_with_modes(
        golden_list_file, soc_block_name, user_modes
    )

    # Find matches and mismatches
    matches, mismatches = find_matches_and_mismatches(directory_file_list, updated_golden_list)

    # Write report
    write_report(matches, mismatches)


if __name__ == "__main__":
    main()