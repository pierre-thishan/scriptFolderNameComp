import os

DEFAULT_MODES = {"FUNC", "ATPG_SHIFT", "ATPG_STUCKAT", "ATPG_ATSPEED"}

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
            if '<' in line and '>' in line:
                # Replace `<...>` with SOC block name
                updated_line = line.replace(line[line.find('<'):line.find('>') + 1], soc_block_name)
                
                # Handle `<mode>` expansion
                if "<mode>" in updated_line:
                    for mode in mode_list:
                        updated_list.add(updated_line.replace("<mode>", mode))
                else:
                    updated_list.add(updated_line)
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

    # Additional logic (if required, e.g., comparisons, reports) can be plugged in here.


if __name__ == "__main__":
    main()
