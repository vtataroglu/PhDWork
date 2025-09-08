import pandas as pd
import sqlite3

# Path to the CSV file
csv_file_path = 'BTC-2021min.csv'  # Change this to the path of your CSV file

# Connect to SQLite database (creates the database if it doesn't exist)
conn = sqlite3.connect('bitcoin_price.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bitcoin_prices (
    unix INTEGER,
    date TEXT,
    symbol TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume_btc REAL,
    volume_usd REAL
)
''')

# Load data from CSV into a DataFrame
df = pd.read_csv(csv_file_path)

# Rename DataFrame columns to match SQL table column names
df.columns = df.columns.str.replace(' ', '_').str.lower()

# Convert 'date' column to string to ensure compatibility with SQLite TEXT type
df['date'] = df['date'].astype(str)

# Import data into SQLite database
df.to_sql('bitcoin_prices', conn, if_exists='append', index=False)

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data imported successfully into SQLite database.")
