import sqlite3

def aggregate_and_store_all_data(database_path):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        # Create the table if it does not exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS min10price (
            time_interval DATETIME PRIMARY KEY,
            open_time DATETIME,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT
        );
        """)
        # Perform the aggregation and insert data into min10price
        aggregation_query = """
        INSERT INTO min10price (time_interval, open_time, open, high, low, close)
        SELECT 
            datetime((strftime('%s', date) / 600) * 600, 'unixepoch') AS time_interval,
            MIN(date) AS open_time,
            FIRST_VALUE(open) OVER (PARTITION BY datetime((strftime('%s', date) / 600) * 600, 'unixepoch') ORDER BY date ASC) AS open,
            MAX(high) AS high,
            MIN(low) AS low,
            LAST_VALUE(close) OVER (PARTITION BY datetime((strftime('%s', date) / 600) * 600, 'unixepoch') ORDER BY date DESC) AS close
        FROM bitcoin_prices
        GROUP BY time_interval
        ORDER BY time_interval ASC;
        """
        cursor.execute(aggregation_query)
        conn.commit()

# Example usage of the function
database_path = 'bitcoin_price.db'
aggregate_and_store_all_data(database_path)
