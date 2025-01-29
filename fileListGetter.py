import os

def list_files(directory, output_file="file_list.txt"):
    """
    Lists all file names in a directory (including subdirectories) and saves them to a text file.
    Ignores hidden files and directories.
    """
    file_list = []
    
    for root, dirs, files in os.walk(directory):
        # Ignore hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        for file in files:
            if not file.startswith("."):  # Ignore hidden files
                file_path = os.path.abspath(os.path.join(root, file))
                file_list.append(file_path)
    
    # Save file list to the output file
    with open(output_file, 'w') as f:
        for file_path in sorted(file_list):
            f.write(file_path + "\n")
    
    print(f"File list saved to: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    target_directory = input("Enter the directory to scan: ").strip()
    output_filename = input("Enter the output file name (or press Enter for default 'file_list.txt'): ").strip()
    output_filename = output_filename if output_filename else "file_list.txt"
    
    if os.path.isdir(target_directory):
        list_files(target_directory, output_filename)
    else:
        print("Error: Directory does not exist.")