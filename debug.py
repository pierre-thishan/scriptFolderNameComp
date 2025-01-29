import os
from datetime import datetime
from itertools import product

DEFAULT_MODES = {"Matpg_stuckat", "Matpg_atspeed", "Matpg_shift", "Mfunc"}  # Default PVT Modes
default_p = {"Ptt", "Pssgnp", "Pffgnp"}
default_v = ["V0675", "V0720", "V0750", "V0770", "V0825", "V1050", "V1160"]  # Sorted manually in ascending order  # Sorted voltages in ascending order
default_t = {"T125", "Tm40", "T025"}
default_e = {"Ecworst_CCworst_T", "Ecworst_CCworst", "Ercworst_CCworst", "Ercworst_CCworst_T", "Etypical", "Ecbest_CCbest", "Ercbest_CCbest"}

def get_pvte_combinations(p_set, v_set, t_set, e_set, mode_set):
    """
    Generates all possible PVTE and Mode combinations while maintaining the fixed order.
    """
    return ["{}_{}_{}_{}_{}".format(p, v, t, e, mode)
            for p, v, t, e, mode in product(p_set, v_set, t_set, e_set, mode_set)]

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
    include_mismatch_locations = input("Include file paths for mismatches? (yes/no): ").strip().lower() == 'yes'
    
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    directory_file_list = generate_directory_file_report(directory, f"directory_file_list_{timestamp}.txt")
    matches, missing_in_target, extra_in_target = find_matches_and_mismatches(directory_file_list, [])
    write_report(matches, missing_in_target, extra_in_target, directory_file_list, include_mismatch_locations, f"file_comparison_report_{timestamp}.txt")

if __name__ == "__main__":
    main()