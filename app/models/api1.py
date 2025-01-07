import json
import requests
from flask import jsonify

# gets data
def get_data(data):
    with open(data, 'r') as f:
        content = json.load(f)
    return content

# gets tokens
def get_access(access):
    with open(access, 'r') as f:
        content = json.load(f)
    return content

import logging
logging.basicConfig(level=logging.DEBUG)

def live_locate(lat, lon):
    logging.debug(f"Requesting location for lat: {lat}, lon: {lon}")
    # ... rest of the function

# take location by coordinates
def live_locate(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)

        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={tokens['weather_key']}"

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return jsonify({"error": f"error code {res.status_code}"}), res.status_code

        data = res.json()
        city = data.get('name', "Unknown City")
        country = data.get('sys', {}).get('country', "Unknown City")
        location = f"{city}, {country}"

        return {"location": location, "{city": city}, 200

    except ValueError as ve:
        return jsonify({"error": f"Invalid latitude or longitude: {str(ve)}"}), 400

    except KeyError as ke:
        return jsonify({"error": "API key is missing or invalid"}), 500

    except Exception as e:
        return jsonify({"error": f"request nerror {str(e)}"}), 500

tokens = get_access("access.txt")
api = get_data("data.txt")
class Api:
    def get_flight(flight_number=None):
        """
        flight api to return flight details
        """
        your_flight = []
        l_flight = None
        try:
            flights = api['data']
            for flight in flights:
                if flight_number == int(flight['flight']['number']):
                    your_flight = {
                            'aircraft_no': flight['aircraft']['registration'],
                            'airline': flight['airline']['name'],
                            'take_off': {
                                'time': flight['departure']['actual'],
                                'from': flight['departure']['airport'],
                                'timezone': flight['departure']['timezone']
                                },
                            'landing': {
                                'time': flight['arrival']['estimated'],
                                'to': flight['arrival']['airport'],
                                'timezone': flight['arrival']['timezone']
                                },
                            'flight_status': flight['flight_status'],
                            'live': {
                                'alt': flight['live']['altitude'],
                                'location': live_locate(flight['live']['latitude'], flight['live']['longitude']),
                                'direction': flight['live']['direction'],
                                'speed': flight['live']['speed_horizontal']
                                }
                            }
                elif flight_number is None:
                    # returns all live flights
                    for flight in flights:
                        if flight['live'] is not None:
                            l_flight = {
                                'flight_number': flight['flight']['number'],
                                'aircraft_no': flight['aircraft']['registration'],
                                'airline': flight['airline']['name'],
                                'live': {
                                    'alt': flight['live']['altitude'],
                                    'location': live_locate(flight['live']['latitude'], flight['live']['longitude']),
                                    'direction': flight['live']['direction'],
                                    'speed': flight['live']['speed_horizontal']
                                    }
                                }
                            your_flight.append(l_flight)

            if your_flight:
                return your_flight
            else:
                return jsonify({'error': f"flight {flight_number} Not Found"}), 404
        except Exception as error:
            return jsonify({'error': f'error {error}'}), 500


    # weather data
    def weather():
        """
        weather api to return weather details on that particular location
        """
        city = "Ruiru"
        if city == None:
            city == "London"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={tokens['weather_key']}&units=metric"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

            weather = {
                    #"location": live_locate(data['coord']['lat'], data['coord']['lon']),
                    "weather" : data['weather'][0]['main'],
                    "icon" : data['weather'][0]['icon'],
                    "humidity" : data['main']['humidity'],
                    "temp" : data['main']['temp'],
                    "visibility" : data['visibility'],
                    "wind_speed" : data['wind']['speed']
                    }
            return weather
        except Exception as e:
            return jsonify({"error": e})
