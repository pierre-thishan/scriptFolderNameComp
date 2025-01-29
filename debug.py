import os
from datetime import datetime
from itertools import product

DEFAULT_MODES = {"Matpg_stuckat", "Matpg_atspeed", "Matpg_shift", "Mfunc"}  # Default PVT Modes
default_p = {"Ptt", "Pssgnp", "Pffgnp"}
default_v = {"V0675", "V0720", "V0750", "V0770", "V0825", "V1050", "V1160"}  # Sorted voltages in ascending order
default_t = {"T125", "Tm40", "T025"}
default_e = {"Ecworst_CCworst_T", "Ecworst_CCworst", "Ercworst_CCworst", "Ercworst_CCworst_T", "Etypical", "Ecbest_CCbest", "Ercbest_CCbest"}

def get_pvte_combinations(p_set, v_set, t_set, e_set, mode_set):
    """
    Generates all possible PVTE and Mode combinations while maintaining the fixed order.
    """
    return ["{}_{}_{}_{}_{}".format(p, v, t, e, mode)
            for p, v, t, e, mode in product(p_set, v_set, t_set, e_set, mode_set)]

def save_pvte_combinations_to_file(p_set, v_set, t_set, e_set, mode_set, output_file="pvte_combinations.txt"):
    """
    Saves the generated PVTE combinations to a file for debugging purposes.
    """
    pvte_combinations = get_pvte_combinations(p_set, v_set, t_set, e_set, mode_set)
    with open(output_file, 'w') as f:
        f.write("Generated PVTE Combinations\n")
        f.write("=" * 50 + "\n")
        for combo in pvte_combinations:
            f.write(combo + "\n")
    print(f"PVTE combinations saved to: {os.path.abspath(output_file)}")

def prompt_pvte_options():
    """
    Displays available PVTE options and allows the engineer to customize selections.
    """
    print("Default PVTE Options:")
    print(f"Process (P): {default_p}")
    print(f"Voltage (V): {default_v}")
    print(f"Temperature (T): {default_t}")
    print(f"Environment (E): {default_e}")
    print(f"Modes: {DEFAULT_MODES}")

    custom_choice = input("Would you like to modify these selections? (yes/no): ").strip().lower()
    
    if custom_choice == "yes":
        def modify_set(name, default_set):
            print(f"Modify {name} (current: {default_set})")
            new_values = input("Enter comma-separated values or press Enter to keep default: ").strip()
            return set(new_values.split(',')) if new_values else default_set
        
        return (
            modify_set("Process (P)", default_p),
            modify_set("Voltage (V)", default_v),
            modify_set("Temperature (T)", default_t),
            modify_set("Environment (E)", default_e),
            modify_set("Modes", DEFAULT_MODES),
        )
    return default_p, default_v, default_t, default_e, DEFAULT_MODES

def update_golden_list_with_pvte_modes(golden_list_path, soc_block_name, p_set, v_set, t_set, e_set, mode_set, debug_file):
    """
    Updates the golden list by replacing `<anamix>` with SOC block name
    and `<PVTE><Mode>` with all possible combinations.
    """
    pvte_combinations = get_pvte_combinations(p_set, v_set, t_set, e_set, mode_set)
    updated_list = set()
    
    with open(golden_list_path, 'r') as f:
        for line in f:
            line = line.strip()
            if "<anamix>" in line and "<PVTE><Mode>" in line:
                for pvte in pvte_combinations:
                    updated_list.add(line.replace("<anamix>", soc_block_name).replace("<PVTE><Mode>", pvte))
            else:
                updated_list.add(line)
    
    with open(debug_file, 'w') as debug_f:
        debug_f.write(f"Updated Golden List with PVTE Modes ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
        debug_f.write("=" * 50 + "\n")
        for item in sorted(updated_list):
            debug_f.write(item + "\n")
    
    print(f"Updated golden list saved to: {os.path.abspath(debug_file)}")
    return updated_list

def main():
    soc_block_name = input("Enter the SOC block name: ").strip()
    golden_list_file = input("Enter the path to the golden list file: ").strip()
    p_set, v_set, t_set, e_set, mode_set = prompt_pvte_options()  # Prompt the engineer for PVTE modifications
    
    save_pvte_combinations_to_file(p_set, v_set, t_set, e_set, mode_set)  # Save PVTE combinations for debugging
    
    if not os.path.isfile(golden_list_file):
        print(f"Error: File '{golden_list_file}' does not exist.")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    updated_golden_list = update_golden_list_with_pvte_modes(golden_list_file, soc_block_name, p_set, v_set, t_set, e_set, mode_set, f"updated_golden_list_{timestamp}.txt")

if __name__ == "__main__":
    main()