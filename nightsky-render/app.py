# app.py - Flask API for NightSky Helper

from flask import Flask, request, jsonify
from flask_cors import CORS
from sky_calculator import SkyCalculator
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow cross-origin requests from the frontend

@app.get("/api/observations")
def get_observation():
    """
    Expects a query parameter: ?date=YYYY-MM-DD
    Returns JSON with observation details.
    """
    date_str = request.args.get("date")

    if not date_str:
        return jsonify({"error": "Missing 'date' query parameter."}), 400

    try:
        # Convert string to datetime.date
        obs_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    try:
        calculator = SkyCalculator()
        observation = calculator.calculate(obs_date)
        
        # Convert to dict for JSON response
        observation_dict = {
            "date": observation.date,
            "sunset": observation.sunset,
            "dark_sky": observation.dark_sky,
            "sunrise": observation.sunrise,
            "planets": observation.planets,
            "stars": observation.stars,
            "moon_illum": observation.moon_illum,
        }

        return jsonify(observation_dict)

    except Exception as e:
        return jsonify({"error": f"Failed to calculate observation: {str(e)}"}), 500

@app.get("/")
def home():
    return jsonify({"service": "NightSky Helper API", "status": "running"})

if __name__ == "__main__":
    app.run(debug=True)
