import json, os, folium
import requests
from flask import jsonify, url_for, current_app
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

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
    try:
        # Convert inputs to float
        print("am here wiriama")
        lat = float(lat)
        lon = float(lon)

        # Initialize geolocator
        geolocator = Nominatim(user_agent="location_checker")
        location = geolocator.reverse((lat, lon), language='en')

        # Debug response

        if location:
            raw_address = location.raw.get('address', {})
            town = raw_address.get('town') or raw_address.get('city') or raw_address.get('village', 'Unknown Town')
            country = raw_address.get('country', 'Unknown Country')
            location = f"{town}, {country}"

            return location
        else:
            return "Location not found"
    except (ValueError, TypeError) as e:
        return "Invalid input coordinates"
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return "Geocoding service error"
    except Exception as e:
        return "Unexpected error occurred"

tokens = get_access("access.txt")
api = get_data("data.txt")
class Api:
    def get_flight(flight_number=None):
        your_flight = []
        l_flight = None
        try:
            flights = api['data']
            for flight in flights:
                if flight_number == flight['flight']['number']:
                    your_flight = {
                            'flight_number': flight['flight']['number'],
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
                                'latitude': flight['live']['latitude'],
                                'longitude': flight['live']['longitude'],
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
                                'flight_status': flight['flight_status'],
                                'flight_number': flight['flight']['number'],
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
                                'live': {
                                    'alt': flight['live']['altitude'],
                                    'latitude': flight['live']['latitude'],
                                    'longitude': flight['live']['longitude'],
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

    def map_view(mapping):
        if not mapping:
            return "<p>No flight data available</p>"

        first_location = mapping[0]
        folium_map = folium.Map(location=[float(first_location['lat']), float(first_location['lon'])], zoom_start=5 if len(mapping) == 1 else 3)

        icon = os.path.join(current_app.static_folder, 'images', 'kl.png')
        if not os.path.exists(icon):
            raise FileNotFoundError(f"image not found in path {icon}")

        for mapp in mapping:
            lat = float(mapp['lat'])
            lon = float(mapp['lon'])

            icon_html = f"""
                <div style="transform: rotate({mapp['direction']}deg); width: 30px; height: 30px; background: url('{url_for('static', filename='images/kl.png')}') no-repeat center; background-size: contain;"></div>
                """

            flight_icon = folium.DivIcon(html=icon_html)
            folium.Marker(
                    [lat, lon],
                    popup=f"Flight Location ({mapp['direction']}°)",
                    icon=flight_icon
                    ).add_to(folium_map)

        map_html = folium_map._repr_html_()
        return map_html


    # weather data
    def weather(city=None):
        """
        weather api to return weather details on that particular location
        """
        if city == None:
            city == "London"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={tokens['weather_key']}&units=metric"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

            weather = {
                    "location": live_locate(data['coord']['lat'], data['coord']['lon']),
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
