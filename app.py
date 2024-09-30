# app.py
from flask import Flask, request, jsonify
import requests
from flask_caching import Cache
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app) 

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300}) 
logging.basicConfig(level=logging.DEBUG)

# ------------- Logging ------------------ 

@app.before_request
def log_request_info():
    app.logger.debug('--- Incoming Request ---')
    app.logger.debug('Request Method: %s', request.method)
    app.logger.debug('Request URL: %s', request.url)
    app.logger.debug('Request Headers: %s', request.headers)
    app.logger.debug('Request Body: %s', request.get_data())

@app.after_request
def log_response_info(response):
    app.logger.debug('--- Outgoing Response ---')
    app.logger.debug('Response Status: %s', response.status)
    app.logger.debug('Response Headers: %s', response.headers)
    app.logger.debug('Response Body: %s', response.get_data(as_text=True))
    return response


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

    app.logger.debug('Requesting Alpha Vantage API: %s', url)
    app.logger.debug('Parameters: %s', params)

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    app.logger.debug('Alpha Vantage Response Status: %s', response.status_code)
    app.logger.debug('Alpha Vantage Response Body: %s', response.text)

    # Top gainers, Top losers, and Top traders
    if 'top_gainers' in data and 'top_losers' in data and 'most_actively_traded' in data:
        top_gainers = data['top_gainers'][:10]
        top_losers = data['top_losers'][:10]
        most_active = data['most_actively_traded'][:10]
        return jsonify({
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'most_active': most_active
        })
    else:
        return jsonify({'error': 'No data found for top gainers, losers, or most active.'}), 400



if __name__ == '__main__':
    app.run(debug=True)