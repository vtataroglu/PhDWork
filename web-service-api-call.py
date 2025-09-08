from flask import Flask, request, jsonify, Response
import sqlite3
import json
import gzip
from datetime import datetime

app = Flask(__name__)

def query_ohlc_data(start_date, end_date):
    try:
        datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None, "Invalid date format"

    with sqlite3.connect('bitcoin_price.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
        SELECT date, open, high, low, close FROM bitcoin_prices
        WHERE date BETWEEN ? AND ?
        ORDER BY date ASC
        """
        cursor.execute(query, (start_date, end_date))
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return json.dumps(data, default=str), None

def fetch_entries(database_path, start_time, end_time):
    with sqlite3.connect(database_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = """
        SELECT time_interval, open_time, open, high, low, close
        FROM min10price
        WHERE open_time BETWEEN ? AND ?
        ORDER BY time_interval ASC;
        """
        cursor.execute(query, (start_time, end_time))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

@app.route('/get_price_ten-interval', methods=['GET'])
def get_data():
    database_path = 'bitcoin_price.db'
    start_time = request.args.get('start', '')
    end_time = request.args.get('end', '')
    
    try:
        datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.'}), 400
    
    entries = fetch_entries(database_path, start_time, end_time)
    return jsonify(entries)

@app.route('/api/get-price-data', methods=['GET'])
def get_ohlc_data():
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if not start_date or not end_date:
        return jsonify({'error': 'Missing required parameters'}), 400
    json_data, error = query_ohlc_data(start_date, end_date)
    if error:
        return jsonify({'error': error}), 400
    return Response(json_data, mimetype='application/json')

def query_data(start_datetime, end_datetime):
    with sqlite3.connect('bitcoin_blocks.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM blocks
            WHERE time BETWEEN ? AND ?
        """, (start_datetime, end_datetime))  
        rows = cursor.fetchall()
        data = [dict(row) for row in rows]
        return json.dumps(data)

@app.route('/api/get_data_by_interval_time', methods=['GET'])
def get_data_by_time():
    start_datetime = request.args.get('start_datetime')
    end_datetime = request.args.get('end_datetime')
    if not start_datetime or not end_datetime:
        return jsonify({'error': 'Missing datetime parameters'}), 400
    json_data = query_data(start_datetime, end_datetime)
    compressed_data = gzip.compress(json_data.encode())
    response = Response(compressed_data, mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Length'] = str(len(compressed_data))
    return response

if __name__ == '__main__':
    app.run(debug=True)
