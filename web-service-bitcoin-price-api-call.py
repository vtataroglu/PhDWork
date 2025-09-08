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

if __name__ == '__main__':
    app.run()
