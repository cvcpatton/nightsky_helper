from flask import Flask, request, jsonify
from flask_cors import CORS

from output import db, Observation
from sky_calculator import SkyCalculator

app = Flask(__name__)
CORS(app)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nightsky.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return {
        "service": "NightSky Helper API",
        "status": "running"
    }
    
@app.route("/api/observations", methods=["GET"])
def get_observations():
    observations = Observation.query.all()
    return jsonify([obs.to_dict() for obs in observations])


@app.route("/api/observations", methods=["POST"])
def create_observation():
    data = request.get_json()

    if "date" not in data:
        return jsonify({"error": "Date is required"}), 400

    calculator = SkyCalculator()
    observation_data = calculator.calculate(data["date"])

    observation = Observation.from_calculation(observation_data)
    db.session.add(observation)
    db.session.commit()

    return jsonify(observation.to_dict()), 201


@app.route("/api/observations/<int:obs_id>", methods=["DELETE"])
def delete_observation(obs_id):
    observation = Observation.query.get_or_404(obs_id)
    db.session.delete(observation)
    db.session.commit()
    return jsonify({"message": "Observation deleted"})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

