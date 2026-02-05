# app.py - Flask API for NightSky Helper

from flask import Flask, request, jsonify
from sky_calculator import SkyCalculator

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"service": "NightSky Helper API", "status": "running"})


@app.route("/api/observations")
def get_observation():
    """
    Accepts a date parameter, calculates the sky observation for that date,
    and returns it as JSON.
    Example: /api/observations?date=2026-02-05
    """
    obs_date = request.args.get("date")
    if not obs_date:
        return jsonify({"error": "No date provided"}), 400

    try:
        calculator = SkyCalculator()
        observation = calculator.calculate(obs_date)  # Returns Observation object

        # Convert Observation object to dict
        obs_dict = {
            "date": observation.date,
            "sunset": observation.sunset,
            "dark_sky": observation.dark_sky,
            "sunrise": observation.sunrise,
            "planets": observation.planets,
            "stars": observation.stars,
            "moon_illum": getattr(observation, "moon_illum", "N/A")
        }

        # Optional: save observation to file if you want persistence
        # from output import save_observations
        # save_observations([observation])

        return jsonify(obs_dict)

    except Exception as e:
        return jsonify({"error": f"Failed to calculate observation: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
