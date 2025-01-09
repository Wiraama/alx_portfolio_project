"""
main py file to deal wit basic routes
:   home route
:   welcome page
"""
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from app.models.api import Api
import os, json, random
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
import logging

main = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def landing():
    try:
        mapping = []
        flight = Api.get_flight()
        count = 0
        for f in flight:
            if isinstance(f, dict) and 'live' in f and f['live'] is not None:
                from app.models.api import live_locate
                location = live_locate(f['live']['latitude'], f['live']['longitude'])
                res = location.split()
                city = res[0]
                mapping_data = {
                        'lat': f['live']['latitude'],
                        'lon': f['live']['longitude'],
                        'direction': f['live']['direction']
                        }
                mapping.append(mapping_data)
                count += 1
                if count >= 7:
                    break

        map_html = Api.map_view(mapping)
        weather = Api.weather(city)
    except Exception as e:
        return jsonify({"error": f"{e} Occurred"}), 500

    if request.accept_mimetypes.best == 'application/json':
        return jsonify(flight=flight)

    return render_template('landing.html', weather=weather, flight=flight, map_html=map_html)

@main.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    weather = None
    flight = None
    map_html = None
    mapping = []
    try:
        flight_number = request.args.get('s') if request.method == 'GET' else request.form.get('flight_number')

        res = Api.get_flight(flight_number)

        if isinstance(res, tuple):
            flight, status_code = res
            if status_code != 200:
                return redirect(url_for('main.home'))

        else:
            flight = res

        if isinstance(flight, list) and flight:
           flight = flight[0] 

        if isinstance(flight, dict) and 'live' in flight:
            if 'location' in flight['live']:
                location = flight['live']['location']
                res = location.split()
                city = res[0]
                mapp = {
                    'lat': flight['live']['latitude'],
                    'lon': flight['live']['longitude'],
                    'direction': flight['live']['direction']
                    }
                mapping.append(mapp)

                weather = Api.weather(city)
                map_html = Api.map_view(mapping)
            elif 'latitude' and 'longitude' in flight['live']:
                from app.models.api import live_locate
                location = live_locate(flight['live']['latitude'], flight['live']['longitude'])
                res = location.split()
                city = res[0]
                mapp = {
                    'lat': flight['live']['latitude'],
                    'lon': flight['live']['longitude'],
                    'direction': flight['live']['direction']
                    }

                mapping.append(mapp)
                weather = Api.weather(city)
                map_html = Api.map_view(mapping)

        elif not flight['live']:
            flight['live'] = None
        else:
            raise ValueError("Flight data is not in the expected format or missing 'live' key.")

        print(f"flight object: {flight}")

    except Exception as e:
        logging.error("Error: %s", str(e))
        import traceback
        traceback.print_exc()

        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

    if request.accept_mimetypes.best == 'application/json':
        return jsonify(flight=flight)

    with open('facts.txt', 'r') as f:
        facts = json.load(f)
        random_facts = random.choice(facts)

    return render_template('Home.html', flight=flight, weather=weather, facts=random_facts, map_html=map_html)
