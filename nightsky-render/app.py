# app.py - Flask API for NightSky Helper
from flask import Flask, request, jsonify
from flask_cors import CORS
from sky_calculator import SkyCalculator
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"service": "NightSky Helper API", "status": "running"})


@app.route("/api/observations")
def get_observation():
    """
    Accepts a 'date' query parameter in YYYY-MM-DD format,
    calculates the sky observation for that date,
    and returns it as JSON.
    Example: /api/observations?date=2026-02-05
    """
    obs_date_str = request.args.get("date")
    if not obs_date_str:
        return jsonify({"error": "No date provided"}), 400

    try:
        # Convert string to datetime.date
        obs_date = datetime.strptime(obs_date_str, "%Y-%m-%d").date()

        # Calculate observation
        calculator = SkyCalculator()
        observation = calculator.calculate(obs_date)  # Returns Observation object

        # Convert Observation object to dict for JSON
        obs_dict = {
            "date": observation.date,
            "sunset": observation.sunset,
            "dark_sky": observation.dark_sky,
            "sunrise": observation.sunrise,
            "planets": observation.planets,
            "stars": observation.stars,
            "moon_illum": getattr(observation, "moon_illum", "N/A")
        }

        return jsonify(obs_dict)

    except Exception as e:
        return jsonify({"error": f"Failed to calculate observation: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
