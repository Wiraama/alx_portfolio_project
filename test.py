from app import create_app  # Assuming you have a factory function to create the app
from app.models.api import Api

# Create a Flask app instance and push an app context
app = create_app()

with app.app_context():
    # Now you can safely call the function that requires the Flask app context
    res, status_code = Api.get_flight(flight_number=808)
    
    # If the status code is 200, get the JSON data from the response
    if status_code == 200:
        print("Flight Details:", res)  # If the response is in JSON, it will be printed here
    else:
        print(f"Error: {res}, Status Code: {status_code}")

