import sqlite3
import csv
import os

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('bitcoin_blocks.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER,
    hash TEXT,
    time TEXT,
    median_time TEXT,
    size INTEGER,
    stripped_size INTEGER,
    weight INTEGER,
    version INTEGER,
    version_hex TEXT,
    version_bits TEXT,
    merkle_root TEXT,
    nonce INTEGER,
    bits TEXT,
    difficulty REAL,
    chainwork TEXT,
    coinbase_data_hex TEXT,
    transaction_count INTEGER,
    witness_count INTEGER,
    input_count INTEGER,
    output_count INTEGER,
    input_total INTEGER,
    input_total_usd REAL,
    output_total INTEGER,
    output_total_usd REAL,
    fee_total INTEGER,
    fee_total_usd REAL,
    fee_per_kb REAL,
    fee_per_kb_usd REAL,
    fee_per_kwu REAL,
    fee_per_kwu_usd REAL,
    cdd_total INTEGER,
    generation INTEGER,
    generation_usd REAL,
    reward INTEGER,
    reward_usd REAL,
    guessed_miner TEXT
);
''')

# Directory containing the .tsv files
directory_path = '/root/test/extracted/'

# List all .tsv files in the directory
tsv_files = [f for f in os.listdir(directory_path) if f.endswith('.tsv')]

# Initialize a counter for successful file imports
successful_imports = 0

# Loop over each file and import the data
for filename in tsv_files:
    tsv_file_path = os.path.join(directory_path, filename)
    
    with open(tsv_file_path, 'r') as file:
        tsv_reader = csv.DictReader(file, delimiter='\t')
        for row in tsv_reader:
            columns, values = zip(*row.items())
            sql = 'INSERT INTO blocks ({}) VALUES ({})'.format(
                ', '.join(columns),
                ', '.join('?' * len(values))
            )
            cursor.execute(sql, values)
    conn.commit()  # Commit after each file
    print(f"Data from {filename} imported successfully into SQLite database.")
    successful_imports += 1

# Print the total number of successful file imports
print(f"Total files imported successfully: {successful_imports}")

# Close the connection
conn.close()
