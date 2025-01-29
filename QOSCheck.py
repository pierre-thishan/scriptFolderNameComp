import os
from datetime import datetime

DEFAULT_MODES = {"FUNC", "ATPG_SHIFT", "ATPG_STUCKAT", "ATPG_ATSPEED"}  # Users can input more modes.

def generate_directory_file_report(directory, output_file):
    """
    Generates a report of all file names in the target directory and subdirectories,
    ignoring files that start with a dot (e.g., `.SYNC`, `.swp`).
    """
    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"tool_data", "STUB"}]
        for file_name in files:
            if not file_name.startswith("."):  # Ignore dot files
                absolute_path = os.path.abspath(os.path.join(root, file_name))
                file_list.append(absolute_path)
    
    with open(output_file, 'w') as f:
        f.write(f"Directory File List Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        f.write("=" * 50 + "\n")
        for file_path in sorted(file_list):
            f.write(file_path + "\n")
    
    print(f"Directory file list report saved to: {os.path.abspath(output_file)}")
    return file_list

def update_golden_list_with_modes(golden_list_path, soc_block_name, user_modes, debug_file):
    """
    Updates the golden list by replacing `<...>` with SOC block name
    and `<mode>` with default or user-provided modes.
    """
    mode_list = DEFAULT_MODES.union(user_modes) if user_modes else DEFAULT_MODES
    updated_list = set()
    
    with open(golden_list_path, 'r') as f:
        for line in f:
            line = line.strip()
            if "<anamix>" in line:
                updated_line = line.replace(line[line.find('<'):line.find('>') + 1], soc_block_name)
                if "<mode>" in updated_line:
                    for mode in mode_list:
                        updated_list.add(updated_line.replace("<mode>", mode))
                else:
                    updated_list.add(updated_line)
            else:
                if "<mode>" in line:
                    for mode in mode_list:
                        updated_list.add(line.replace("<mode>", mode))
                else:
                    updated_list.add(line)
    
    with open(debug_file, 'w') as debug_f:
        debug_f.write(f"Updated Golden List with Modes ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        debug_f.write("=" * 50 + "\n")
        for item in sorted(updated_list):
            debug_f.write(item + "\n")
    
    print(f"Updated golden list saved to: {os.path.abspath(debug_file)}")
    return updated_list

def find_matches_and_mismatches(directory_file_list, updated_golden_list):
    """
    Finds both successful matches and mismatches between the directory files and the updated golden list.
    """
    directory_file_names = {os.path.basename(file_path) for file_path in directory_file_list}
    golden_file_names = {os.path.basename(file) for file in updated_golden_list}
    
    matches = directory_file_names & golden_file_names
    missing_in_target = golden_file_names - directory_file_names
    extra_in_target = directory_file_names - golden_file_names
    
    return sorted(matches), sorted(missing_in_target), sorted(extra_in_target)

def write_report(matches, missing_in_target, extra_in_target, directory_file_list, include_mismatch_locations, report_file):
    """
    Writes a report including the success rate, matched files, and mismatched files with optional paths.
    """
    total_files = len(matches) + len(missing_in_target) + len(extra_in_target)
    success_rate = (len(matches) / total_files) * 100 if total_files > 0 else 0
    file_paths = {os.path.basename(fp): fp for fp in directory_file_list}  # Map names to paths
    
    with open(report_file, 'w') as f:
        f.write(f"File Comparison Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total Files Compared: {total_files}\n")
        f.write(f"Successful Matches: {len(matches)}\n")
        f.write(f"Missing in Target Directory: {len(missing_in_target)}\n")
        f.write(f"Extra in Target Directory: {len(extra_in_target)}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n\n")
        
        f.write("Matched Files:\n" + "-" * 50 + "\n")
        for match in matches:
            f.write(match + "\n")
        
        f.write("\nMissing in Target Directory:\n" + "-" * 50 + "\n")
        for missing in missing_in_target:
            f.write(f"{missing} {'(' + file_paths.get(missing, 'Path not found') + ')' if include_mismatch_locations else ''}\n")
        
        f.write("\nExtra in Target Directory:\n" + "-" * 50 + "\n")
        for extra in extra_in_target:
            f.write(f"{extra} {'(' + file_paths.get(extra, 'Path not found') + ')' if include_mismatch_locations else ''}\n")
    
    print(f"File comparison report saved to: {os.path.abspath(report_file)}")

def main():
    soc_block_name = input("Enter the SOC block name: ").strip()
    directory = input("Enter the directory to scan: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()
    additional_modes = input("Enter additional modes (comma-separated) or press Enter to skip: ").strip()
    include_mismatch_locations = input("Include file paths for mismatches? (yes/no): ").strip().lower() == 'yes'
    
    user_modes = {mode.strip() for mode in additional_modes.split(',') if mode.strip()} if additional_modes else None
    
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    directory_file_list = generate_directory_file_report(directory, f"directory_file_list_{timestamp}.txt")
    updated_golden_list = update_golden_list_with_modes(golden_list_file, soc_block_name, user_modes, f"updated_golden_list_{timestamp}.txt")
    matches, missing_in_target, extra_in_target = find_matches_and_mismatches(directory_file_list, updated_golden_list)
    write_report(matches, missing_in_target, extra_in_target, directory_file_list, include_mismatch_locations, f"file_comparison_report_{timestamp}.txt")

if __name__ == "__main__":
    main()
