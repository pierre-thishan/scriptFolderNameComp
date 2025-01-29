import os
from datetime import datetime
from itertools import product

# Default modes that only replace <mode> in the golden list
DEFAULT_MODES = {"FUNC", "ATPG_SHIFT", "ATPG_STUCKAT", "ATPG_ATSPEED"}

# PVTE-specific modes that replace <MODE> in the golden list
PVTE_MODES = {"Matpg_stuckat", "Matpg_atspeed", "Matpg_shift", "Mfunc"}

default_p = {"Ptt", "Pssgnp", "Pffgnp"}
default_v = ["V0675", "V0720", "V0750", "V0770", "V0825", "V1050", "V1160"]  # Sorted manually
default_t = {"T125", "Tm40", "T025"}
default_e = {"Ecworst_CCworst_T", "Ecworst_CCworst", "Ercworst_CCworst", "Ercworst_CCworst_T", "Etypical", "Ecbest_CCbest", "Ercbest_CCbest"}

def get_pvte_combinations():
    """
    Generates all possible PVTE and Mode combinations while maintaining the fixed order.
    """
    return ["{}_{}_{}_{}_{}".format(p, v, t, e, mode)
            for p, v, t, e, mode in product(default_p, default_v, default_t, default_e, PVTE_MODES)]

def save_pvte_combinations(output_file="pvte_combinations.txt"):
    """
    Saves the generated PVTE combinations to a file for debugging purposes.
    """
    pvte_combinations = get_pvte_combinations()
    with open(output_file, 'w') as f:
        f.write("Generated PVTE Combinations\n")
        f.write("=" * 50 + "\n")
        for combo in pvte_combinations:
            f.write(combo + "\n")
    print(f"PVTE combinations saved to: {os.path.abspath(output_file)}")

def update_golden_list_with_modes(golden_list_path, soc_block_name, user_modes, debug_file):
    """
    Updates the golden list by replacing `<anamix>` with SOC block name
    and `<mode>` with default or user-provided modes, and `<MODE>` with PVTE modes.
    """
    mode_list = DEFAULT_MODES.union(user_modes) if user_modes else DEFAULT_MODES
    pvte_combinations = get_pvte_combinations()
    updated_list = set()
    
    with open(golden_list_path, 'r') as f:
        for line in f:
            line = line.strip()
            if "<anamix>" in line:
                updated_line = line.replace("<anamix>", soc_block_name)
                if "<mode>" in updated_line:
                    for mode in mode_list:
                        updated_list.add(updated_line.replace("<mode>", mode))
                elif "<MODE>" in updated_line:
                    for pvte in pvte_combinations:
                        updated_list.add(updated_line.replace("<MODE>", pvte))
                else:
                    updated_list.add(updated_line)
            else:
                if "<mode>" in line:
                    for mode in mode_list:
                        updated_list.add(line.replace("<mode>", mode))
                elif "<MODE>" in line:
                    for pvte in pvte_combinations:
                        updated_list.add(line.replace("<MODE>", pvte))
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
    save_pvte_combinations()  # Save PVTE combinations for debugging
    directory_file_list = generate_directory_file_report(directory, f"directory_file_list_{timestamp}.txt")
    updated_golden_list = update_golden_list_with_modes(golden_list_file, soc_block_name, user_modes, f"updated_golden_list_{timestamp}.txt")
    matches, missing_in_target, extra_in_target = find_matches_and_mismatches(directory_file_list, updated_golden_list)
    write_report(matches, missing_in_target, extra_in_target, directory_file_list, include_mismatch_locations, f"file_comparison_report_{timestamp}.txt")

if __name__ == "__main__":
    main()