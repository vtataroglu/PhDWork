import os
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_file(file_path, extract_dir):
    try:
        # Construct the path for the extracted file
        file_name = os.path.basename(file_path)
        extract_path = os.path.join(extract_dir, file_name[:-3])  # Remove .gz to get .tsv

        # Extract the file
        with gzip.open(file_path, 'rb') as f_in:
            with open(extract_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        return file_path, True
    except Exception as e:
        print(f"Failed to extract {file_path}: {e}")
        return file_path, False

def main():
    # Directory containing the downloaded .tsv.gz files
    download_dir = '/root/test'
    # Directory to extract files to
    extract_dir = './extracted'

    # Ensure the extraction directory exists
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # List all .tsv.gz files in the download directory
    files_to_extract = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if f.endswith('.tsv.gz')]

    # Set up the ThreadPoolExecutor for parallel extraction
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Create a future for each extraction task
        futures = [executor.submit(extract_file, file_path, extract_dir) for file_path in files_to_extract]
        # Process results as they become available
        for future in as_completed(futures):
            file_path, success = future.result()
            print(f"{'Successfully' if success else 'Failed to'} extract {file_path}")

if __name__ == "__main__":
    main()
