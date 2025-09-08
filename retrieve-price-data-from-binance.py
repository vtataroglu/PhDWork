import requests
import pandas as pd
from datetime import datetime, timedelta
import json

def get_binance_price(symbol, start_time, end_time):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': '1m',
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000),
        'limit': 1500  # Maximum limit per API call
    }
    response = requests.get(url, params=params)
    data = response.json()
    if response.status_code == 200:
        columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 
                   'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 
                   'Taker buy quote asset volume', 'Ignore']
        df = pd.DataFrame(data, columns=columns)
        df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame on failure

# Read timestamps from file
with open('missing_dates.txt', 'r') as file:
    timestamps = [datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S') for line in file]

# Create DataFrame from timestamps
df = pd.DataFrame(timestamps, columns=['timestamp'])

# Group by date
grouped = df.groupby(df['timestamp'].dt.date)

# Prepare list for JSON output
all_data = []

# Process each group
for date, group in grouped:
    start_time = group['timestamp'].min()
    end_time = group['timestamp'].max()

    # Fetch data
    data = get_binance_price('BTCUSDT', start_time, end_time)

    # Convert data to JSON format and append to list
    for index, row in data.iterrows():
        entry = {
            "date": row['Open time'].strftime('%Y-%m-%d %H:%M:%S'),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": float(row['Close'])
        }
        all_data.append(entry)

# Write to JSON file
with open('data.json', 'w') as f:
    json.dump(all_data, f, indent=2)
