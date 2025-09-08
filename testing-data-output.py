import os
import glob

def get_latest_tsv_file(directory):
    # Get all .tsv files in the directory
    tsv_files = glob.glob(os.path.join(directory, '*.tsv'))
    # Sort files by file name
    tsv_files.sort(key=str.lower, reverse=True)
    # Return the latest .tsv file
    if tsv_files:
        return tsv_files[0]
    else:
        return None

def print_first_three_lines(file_path):
    try:
        # Open the file and read the first three lines
        with open(file_path, 'r') as file:
            print("```")  # Start Markdown code block
            for _ in range(10):
                line = file.readline()
                if not line:
                    break
                print(line.strip())  # Use strip() to remove newline characters
            print("```")  # End Markdown code block
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")

def main():
    directory = '/root/test/extracted'  # Replace with your directory
    latest_tsv_file = get_latest_tsv_file(directory)
    if latest_tsv_file:
        print(f"### Latest .tsv file: `{latest_tsv_file}`")
        print_first_three_lines(latest_tsv_file)
    else:
        print("No .tsv files found in the directory.")

if __name__ == "__main__":
    main()
