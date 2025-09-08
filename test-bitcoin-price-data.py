import sqlite3
import json
from datetime import datetime

def query_ohlc_data(start_date, end_date):
    # Connect to the SQLite database
    conn = sqlite3.connect('bitcoin_price.db')
    conn.row_factory = sqlite3.Row  # Enable accessing columns by names
    cursor = conn.cursor()

    # SQL query to select OHLC data between two datetimes
    query = """
    SELECT date, open, high, low, close FROM bitcoin_prices
    WHERE date BETWEEN ? AND ?
    ORDER BY date ASC
    """
    cursor.execute(query, (start_date, end_date))

    # Fetch all results
    rows = cursor.fetchall()

    # Convert rows to dictionaries to facilitate JSON conversion
    data = [dict(row) for row in rows]

    # Close the database connection
    conn.close()

    # Convert data to JSON format
    return json.dumps(data, default=str)  # default=str to handle datetime serialization if needed

# Example usage
start_date = '2019-12-31 23:55:00'
end_date = '2020-01-01 00:05:00'
json_data = query_ohlc_data(start_date, end_date)
print(json_data)
