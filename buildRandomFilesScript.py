import os
import random
import string

def create_test_environment(base_dir, golden_list_file, golden_list, num_extra_files=5):
    """Creates a test environment with a mix of matching and mismatching files."""
    # Create base directory
    os.makedirs(base_dir, exist_ok=True)

    # Create some subdirectories
    subdirs = [os.path.join(base_dir, f"subdir_{i}") for i in range(3)]
    for subdir in subdirs:
        os.makedirs(subdir, exist_ok=True)

    # Generate files from the golden list
    for i, name in enumerate(golden_list):
        file_dir = random.choice([base_dir] + subdirs)
        with open(os.path.join(file_dir, name), "w") as f:
            f.write(f"This is file {i} from the golden list.")

    # Generate extra random files not in the golden list
    for i in range(num_extra_files):
        file_dir = random.choice([base_dir] + subdirs)
        random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + ".txt"
        with open(os.path.join(file_dir, random_name), "w") as f:
            f.write(f"This is extra random file {i}.")

    # Write the golden list to a file
    with open(golden_list_file, "w") as f:
        f.writelines(f"{name}\n" for name in golden_list)

    print(f"Test environment created at '{base_dir}'.")
    print(f"Golden list file written to '{golden_list_file}'.")
    print("Golden list contains:")
    print("\n".join(golden_list))

def main():
    base_dir = "test_files"
    golden_list_file = "golden_list.txt"
    golden_list = [
        "file1.txt",
        "file2.txt",
        "file3.txt",
        "golden_file1.txt",
        "golden_file2.txt"
    ]
    create_test_environment(base_dir, golden_list_file, golden_list, num_extra_files=5)

if __name__ == "__main__":
    main()
