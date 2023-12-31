
# Microservice for Google Places API Integration

### Overview

This microservice interfaces with the Google Places API, providing two endpoints: `/search_places` for text-based place searches, and `/search_nearby` for nearby place searches. It's implemented in Python using Flask and requires a valid Google Places API key.


### Communication Contract

#### Making Requests

- **Base URL**: By default, the microservice runs on `http://localhost:5000`. If you deploy this application on a different server or change the port, replace `localhost` with your server's IP address and `5000` with the new port number.

- **Endpoints**:
  - `/search_places`: Performs text-based searches for places.
  - `/search_nearby`: Finds nearby places based on geographical coordinates.

- **Request Format**:
  - Send GET requests to the endpoints with the required parameters.
  - Example for `/search_places`: `GET http://localhost:5000/search_places?query=veterinarians+in+Corvallis`
  - Example for `GET http://localhost:5000/search_nearby?lat=44.5646&lng=-123.2620&radius=5000&type=veterinary_care`

### Receiving Responses

- **Response Format**: Responses are returned in JSON format.

- **Success Response**: Includes the data retrieved from the Google Places API.

- **Error Handling**: In case of errors, responses will include an HTTP status code and a descriptive error message.

### UML Sequence Diagram

![UML Sequence Diagram](https://github.com/joshualena/CS-361-Portfolio/blob/main/images/Screenshot%202023-11-22%20at%201.42.23%20PM.png)

## Installation and Setup

1. Clone the repository to your local machine.
2. Install the required Python packages: `pip install flask requests`.
3. Set up an environment variable for the Google Places API key:
  - On Unix/Linux/macOS:  
     `export GOOGLE_PLACES_API_KEY='your_api_key_here'`
  - On Windows Command Prompt:  
     `set GOOGLE_PLACES_API_KEY=your_api_key_here`
  - On Windows PowerShell:  
     `$env:GOOGLE_PLACES_API_KEY='your_api_key_here'`  
   Replace `your_api_key_here` with your actual Google Places API key.
4. Run the application: `python microservice_for_diana.py`.

## Usage

### Endpoints

#### 1. `/search_places`

- **Method**: GET
- **Parameters**:
  - `query` (str): Text string for the search query. Defaults to 'veterinarians in Corvallis'.
- **Example**: `GET /search_places?query=animal+shelters+in+Corvallis+Oregon`

#### 2. `/search_nearby`

- **Method**: GET
- **Parameters**:
- `lat` (str): Latitude of the location.
- `lng` (str): Longitude of the location.
- `radius` (str): Search radius in meters. Default is 5000 meters.
- `type` (str): Type of place. Default is 'veterinary_care'.
- **Example**: `GET /search_nearby?lat=44.5646&lng=-123.2620&radius=1000&type=animal_shelter`
