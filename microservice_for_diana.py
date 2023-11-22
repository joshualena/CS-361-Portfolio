from flask import Flask, jsonify, request
import requests
import os
from urllib.parse import quote_plus

app = Flask(__name__)

# Load the API key for Google Places API from environment variables for security
google_places_api_key = os.getenv('GOOGLE_PLACES_API_KEY')

@app.route('/search_places', methods=['GET'])
def search_places():
    """
    Endpoint to perform a text-based search for places using the Google Places API.

    This endpoint accepts GET requests with a query parameter and performs a text
    search using the Google Places API. The query can be a combination of the name
    of a place, a type of place, and/or a location. It returns the search results
    provided by the API.

    Parameters:
    query (str): A text string on which the search is based. Defaults to 'veternarians in Corvallis' if not provided.
    """
    query = request.args.get('query', 'veterinarians in Corvallis')
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

@app.route('/search_nearby', methods=['GET'])
def search_nearby():
    """
    Endpoint to search for places nearby using Google Places API.

    This endpoint accepts GET requests and expects parameters for latitude (lat),
    longitude (lng), radius (in meters), and optionally the type of place (type).
    It constructs a URL for a Nearby Search request to the Google Places API
    using these parameters and returns the results.

    Parameters:
    lat (str): Latitude of the location around which to retrieve place information.
    lng (str): Longitude of the location around which to retrieve place information.
    radius (str): The radius (in meters) within which to return place results. Default is 5000 meters.
    type (str): The type of place to filter the results. Default is set to 'veterinary_care'.
    """
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius', '5000')
    type = request.args.get('type', 'veterinary_care')

    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required parameters'}), 400

    google_places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={google_places_api_key}'

    try:
        response = requests.get(google_places_url)
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.HTTPError as http_err:
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500

if __name__ == '__main__':
    app.run(debug=True)