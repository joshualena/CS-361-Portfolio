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

    # Fetch the 'query' parameter from the request; default to 'veternarians in Corvallis'
    query = request.args.get('query', 'veternarians in Corvallis')

    # Check if the query parameter is provided, return an error if not
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Construct the URL for the Google Places API Text Search request
    google_places_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={google_places_api_key}'

    try:
        # Make the API request
        response = requests.get(google_places_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Parse the response JSON
        return jsonify(data)  # Return the parsed JSON as a response
    except requests.HTTPError as http_err:
        # Handle HTTP errors
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        # Handle any other exceptions
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500


@app.route('/search_places', methods=['GET'])
def search_places():
    """Endpoint to search for places using Google Places API."""
    query = request.args.get('query', 'veternarians in Corvallis')

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    google_places_url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={google_places_api_key}'

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

    # Fetch parameters from the request
    lat = request.args.get('lat')  # Latitude
    lng = request.args.get('lng')  # Longitude
    radius = request.args.get('radius', '5000')  # Radius in meters, default is 5000 meters (5 km)
    type = request.args.get('type', 'veterinary_care')  # Default type is set to veterinary care

    # Validate that both latitude and longitude are provided
    if not lat or not lng:
        return jsonify({'error': 'Latitude and longitude are required parameters'}), 400

    # Construct the URL for the Google Places API Nearby Search request
    google_places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={type}&key={google_places_api_key}'

    try:
        # Make the API request
        response = requests.get(google_places_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()  # Parse the response JSON
        return jsonify(data)  # Return the parsed JSON as a response
    except requests.HTTPError as http_err:
        # Handle HTTP errors
        return jsonify({'error': f'HTTP error occurred: {http_err}'}), 500
    except Exception as err:
        # Handle any other exceptions
        return jsonify({'error': f'An unexpected error occurred: {err}'}), 500
