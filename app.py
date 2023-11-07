from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# API key should be kept secure. Consider loading from environment for production.
api_key = 'S4U9D9FVFLIA63BF'


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
    alpha_vantage_url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'

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
        # HTTP errors are caught and sent back with a 500 status code.
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        # Any other exceptions are caught and a generic error message is returned.
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
    if stock_category == 'top':
        alpha_vantage_function = 'TOP_GAINERS_LOSERS'
        key_in_response = 'top_gainers'
    elif stock_category == 'bottom':
        alpha_vantage_function = 'TOP_GAINERS_LOSERS'
        key_in_response = 'top_losers'
    else:
        # If an invalid stock_category is specified, return an error.
        return jsonify({'error': 'Invalid stock_category specified'}), 400

    alpha_vantage_url = f'https://www.alphavantage.co/query?function={alpha_vantage_function}&apikey={api_key}'

    try:
        # Performs the API request and handles potential HTTP errors.
        response = requests.get(alpha_vantage_url)
        response.raise_for_status()
        data = response.json()

        # Checks if the API returned an error message.
        if 'Error Message' in data:
            return jsonify({'error': data['Error Message']}), 400

        # Extracts the relevant data from the API response.
        relevant_data = data.get(key_in_response)

        # If the expected data is not present, return an error.
        if relevant_data is None:
            return jsonify({'error': 'No data available'}), 404

        # Returns the relevant data as a JSON response.
        return jsonify(relevant_data)
    except requests.HTTPError as http_err:
        # Returns a JSON error message for HTTP errors.
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        # Catches any other exceptions and returns a generic error message.
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500


# Runs the application in debug mode when the script is executed directly.
if __name__ == '__main__':
    app.run(debug=True)
