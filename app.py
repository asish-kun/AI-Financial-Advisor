# app.py
from flask import Flask, request, jsonify
import requests
from flask_caching import Cache
from flask_cors import CORS
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json

app = Flask(__name__)
CORS(app) 

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300}) 
logging.basicConfig(level=logging.DEBUG)
# Initializing Embeddings model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the ChromaDB client with updated settings
settings = Settings(persist_directory="chroma_data")

client = chromadb.Client(settings)

collection = client.get_or_create_collection("stock_data")

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


def generate_embedding(text):
    return embedding_model.encode([text])[0]


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

    # Generate embedding
    data_text = json.dumps(data)  # Convert data to string
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol}],
        ids=[symbol]  # Use the stock symbol as the ID
    )

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/overview', methods=['GET'])
def get_stock_overview():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Generate embedding
    data_text = json.dumps(data)  # Convert data to string
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol}],
        ids=[f"{symbol}_overview"]
    )

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/income_statement', methods=['GET'])
def get_income_statement():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'INCOME_STATEMENT',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Generate embedding
    data_text = json.dumps(data)  # Convert data to string
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol}],
        ids=[f"{symbol}_income_statement"]
    )

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/news', methods=['GET'])
def get_stock_news():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': symbol.upper(),
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Generate embedding
    data_text = json.dumps(data)  # Convert data to string
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol}],
        ids=[f"{symbol}_news"]
    )

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/insider_transactions', methods=['GET'])
def get_insider_transactions():
    symbol = request.args.get('symbol')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'INSIDER_TRANSACTIONS',
        'symbol': symbol.upper(),
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Generate embedding
    data_text = json.dumps(data)  # Convert data to string
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol}],
        ids=[f"{symbol}_insider_transactions"]
    )

    if 'Error Message' in data or 'Note' in data:
        return jsonify({'error': data.get('Error Message') or data.get('Note', 'API call limit reached.')}), 400

    return jsonify(data)

@cache.cached()
@app.route('/stocks/time_series', methods=['GET'])
def get_stock_time_series():
    symbol = request.args.get('symbol')
    time_series_function = request.args.get('function', 'TIME_SERIES_DAILY')
    outputsize = request.args.get('outputsize', 'compact')
    datatype = request.args.get('datatype', 'json')

    if not symbol:
        return jsonify({'error': 'Please provide the stock symbol as a parameter.'}), 400

    if time_series_function not in ['TIME_SERIES_DAILY', 'TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY']:
        return jsonify({'error': 'Invalid time series function.'}), 400

    url = 'https://www.alphavantage.co/query'
    params = {
        'function': time_series_function,
        'symbol': symbol.upper(),
        'outputsize': outputsize,
        'datatype': datatype,
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from Alpha Vantage API.'}), 500

    data = response.json()

    # Generate embedding
    data_text = json.dumps(data)
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol, 'function': time_series_function, 'outputsize': outputsize}],
        ids=[f"{symbol}_{time_series_function}_{outputsize}"]
    )

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

    # Generate embedding
    data_text = json.dumps(data)
    embedding = generate_embedding(data_text)

    # Store in Chroma
    collection.add(
        embeddings=[embedding],
        documents=[data_text],
        metadatas=[{'symbol': symbol, 'outputsize': outputsize}],
        ids=[f"{symbol}_daily_{outputsize}"]
    )

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

        combined_data = {
        'top_gainers': top_gainers,
        'top_losers': top_losers,
        'most_active': most_active
        }

        # Generate embedding
        data_text = json.dumps(combined_data)
        embedding = generate_embedding(data_text)

        # Store in Chroma
        collection.add(
            embeddings=[embedding],
            documents=[data_text],
            metadatas=[{'type': 'top_movers'}],
            ids=['top_movers']
        )

        return jsonify({
            'top_gainers': top_gainers,
            'top_losers': top_losers,
            'most_active': most_active
        })
    else:
        return jsonify({'error': 'No data found for top gainers, losers, or most active.'}), 400

@app.route('/query', methods=['POST'])
def query_data():
    data = request.get_json()
    query_text = data.get('query')

    if not query_text:
        return jsonify({'error': 'Please provide a query in the request body.'}), 400

    # Generate embedding for the query
    query_embedding = generate_embedding(query_text)

    # Query the vector database
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,  # Number of results to return
        include=['documents', 'metadatas']  # Include documents and metadata in the response
    )

    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)