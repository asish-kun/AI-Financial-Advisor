# app.py
from flask import Flask, request, jsonify
import requests
from flask_caching import Cache
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})  # Cache timeout in seconds

API_KEY = 'PM36VUI92EF4GOPD'  

@cache.cached()
@app.route('/stocks/quote', methods=['GET'])
def get_stock_quote():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'GLOBAL_QUOTE',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/daily', methods=['GET'])
def get_stock_daily():
    symbol = request.args.get('symbol')
    outputsize = request.args.get('outputsize', 'compact')
    datatype = request.args.get('datatype', 'json')

    # Validate required parameters
    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    # Prepare the API request to Alpha Vantage
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol.upper(),
        'outputsize': outputsize,
        'datatype': datatype,
        'apikey': API_KEY
    }

    # Make the API request
    response = requests.get(url, params=params)

    # Check for request errors
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Check for API errors in the response
    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    # Return the fetched data as JSON
    return jsonify(data)

@cache.cached()
@app.route('/stocks/top_movers', methods=['GET'])
def get_top_movers():
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TOP_GAINERS_LOSERS',
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Extract top gainers and top losers
    if 'top_gainers' in data and 'top_losers' in data:
        top_gainers = data['top_gainers'][:10]
        top_losers = data['top_losers'][:10]
        return jsonify({'top_gainers': top_gainers, 'top_losers': top_losers})
    else:
        return jsonify({'error': 'No data found for top gainers or losers.'}), 400


if __name__ == '__main__':
    app.run(debug=True)