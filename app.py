from flask import Flask, jsonify, request
import requests
import os
from urllib.parse import quote_plus

app = Flask(__name__)

# Diana - Added the import os above and the WATCHLIST_FILE_PATH below

# Load the API key for Alpha Vantage and Google Places API from environment variables for security
alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
google_places_api_key = os.getenv('GOOGLE_PLACES_API_KEY')

WATCHLIST_FILE_PATH = 'watchlist.txt'

# Diana - Add to Watchlist route
@app.route('/add_to_watchlist', methods=['POST'])
def add_to_watchlist():
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        price = data.get('price')

        if symbol and price:
            current_price = get_current_price(symbol)
            if current_price is None:
                return jsonify({'error': 'Failed to fetch current stock price'}), 500
            # Check if the watchlist file exists
            if not os.path.exists(WATCHLIST_FILE_PATH):
                with open(WATCHLIST_FILE_PATH, 'w') as file:
                    file.write(f"{symbol} {price}\n")
            else:
                with open(WATCHLIST_FILE_PATH, 'a') as file:
                    file.write(f"{symbol} {price}\n")

            return jsonify({'message': 'Stock added to watchlist successfully',
                            'current_price': current_price
            })
        else:
            return jsonify({'error': 'Symbol and price are required parameters'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

# Diana - View Watchlist route
@app.route('/view_watchlist', methods=['GET'])
def view_watchlist():
    try:
        # Check if the watchlist file exists
        if os.path.exists(WATCHLIST_FILE_PATH):
            with open(WATCHLIST_FILE_PATH, 'r') as file:
                watchlist_data = [line.strip().split() for line in file.readlines()]

            watchlist = [{'symbol': item[0], 'price': item[1]} for item in watchlist_data]
            return jsonify({'watchlist': watchlist})
        else:
            return jsonify({'watchlist': []})
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

@app.route('/top_stocks', methods=['GET'])
def get_top_stocks():
    """Endpoint to retrieve top performing stocks.
    The method delegates the request to a common utility function that fetches stock performance.

    Returns:
        A JSON response containing the top performing stock data or an error message.
    """
    print(f"Received request at {request.path}")
    return get_stock_performance('top')

@app.route('/bottom_stocks', methods=['GET'])
def get_bottom_stocks():
    """Endpoint to retrieve bottom performing stocks.

    Returns:
        A JSON response containing the bottom performing stock data or an error message.
    """
    return get_stock_performance('bottom')

@app.route('/daily_open_close', methods=['GET'])
def get_daily_open_close():
    """Endpoint to retrieve the daily open and close prices for a given stock symbol.

    The stock symbol is retrieved from the query parameters, defaulting to 'AAPL' if not provided.

    Returns:
        A JSON response containing the opening and closing prices for the specified stock symbol or an error message.
    """
    symbol = request.args.get('symbol', 'AAPL')
    function = "TIME_SERIES_DAILY"
    alpha_vantage_url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={alpha_vantage_api_key}'

    try:
        response = requests.get(alpha_vantage_url)
        response.raise_for_status()
        data = response.json()

        recent_date = list(data['Time Series (Daily)'].keys())[0]
        recent_data = data['Time Series (Daily)'][recent_date]

        open_price = recent_data['1. open']
        close_price = recent_data['4. close']

        return jsonify({
            'symbol': symbol,
            'date': recent_date,
            'open': open_price,
            'close': close_price
        })
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500

# TODO: News Route
# TODO: Alerts Route

def get_stock_performance(stock_category):
    """
    Fetches the stock performance data from Alpha Vantage API.

    Args:
    stock_category (str): A string to determine which category of stocks to fetch.
                      'top' for top gainers, 'bottom' for top losers.

    Returns:
    A JSON response with the stock performance data or an error message.
    """
    alpha_vantage_function = 'TOP_GAINERS_LOSERS'
    key_in_response = 'top_gainers' if stock_category == 'top' else 'top_losers'

    alpha_vantage_url = f'https://www.alphavantage.co/query?function={alpha_vantage_function}&apikey={alpha_vantage_api_key}'

    try:
        response = requests.get(alpha_vantage_url)
        response.raise_for_status()
        data = response.json()

        if 'Error Message' in data:
            return jsonify({'error': data['Error Message']}), 400

        relevant_data = data.get(key_in_response)
        if relevant_data is None:
            return jsonify({'error': 'No data available'}), 404

        return jsonify(relevant_data)
    except requests.HTTPError as http_err:
        # Returns a JSON error message for HTTP errors.
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        # Catches any other exceptions and returns a generic error message.
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500

def get_current_price(symbol):
    """Fetch the most recent close price for a given symbol."""
    function = "TIME_SERIES_DAILY"
    alpha_vantage_url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={alpha_vantage_api_key}'

    try:
        response = requests.get(alpha_vantage_url)
        response.raise_for_status()
        data = response.json()

        recent_date = list(data['Time Series (Daily)'].keys())[0]
        recent_data = data['Time Series (Daily)'][recent_date]

        return recent_data['4. close']
    except Exception as err:
        print(f'Error fetching current price for {symbol}: {err}')
        return None

@app.route('/search_places', methods=['GET'])
def search_places():
    """Endpoint to search for places using Google Places API."""
    query = request.args.get('query', 'brokerages in Denver')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    encoded_query = quote_plus(query)
    google_places_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={encoded_query}&key={google_places_api_key}'

    try:
        response = requests.get(google_places_url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500


# Runs the application in debug mode when the script is executed directly.
if __name__ == '__main__':
    app.run(debug=True)
