# Connect to the SQLite database
import sqlite3
import pandas as pd

with sqlite3.connect('bitcoin_price.db') as conn:
    # Query all data from the bitcoin_prices table ordered by date in ascending order
    df = pd.read_sql_query("SELECT * FROM bitcoin_prices ORDER BY date", conn)

# Convert 'date' to datetime format if it's not already
df['date'] = pd.to_datetime(df['date'])

# Generate a complete datetime range from first to last record, with 1-minute intervals
full_date_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='min')

# Create a DataFrame from this range
df_full_range = pd.DataFrame(full_date_range, columns=['date'])

# Perform a left join with the original data to find missing minutes
df_missing_dates = df_full_range.merge(df, on='date', how='left', indicator=True)

# Filter to show only the missing dates
missing_dates = df_missing_dates[df_missing_dates['_merge'] == 'left_only']

# Print the total number of missing dates
print(f"Total missing dates: {len(missing_dates)}")

# Write the missing dates to a TXT file, one date per line
with open('/root/test/missing_dates.txt', 'w') as file:
    for date in missing_dates['date']:
        file.write(f"{date.strftime('%Y-%m-%d %H:%M:%S')}\n")

print("Missing dates saved to /root/test/missing_dates.txt")
