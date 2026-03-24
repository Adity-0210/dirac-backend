from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

all_users_data = []

@app.route("/")
def home():
    return "DIRAC API is running 🚀"

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    name = data.get("name")
    consent = data.get("consent")
    timestamp = data.get("timestamp")
    answers = data.get("answers", [])

    if not consent:
        return jsonify({"error": "User did not give consent"}), 403

    user_entry = {
        "name": name,
        "consent": consent,
        "timestamp": timestamp,
        "answers": answers,
        "server_time": datetime.now().isoformat()
    }

    all_users_data.append(user_entry)

    score = len([a for a in answers if a in ["Aggressive", "Visionary", "Fast decisions"]])

    if score >= 2:
        result = "Aggressive Visionary 🚀"
    elif score == 1:
        result = "Balanced Strategist ⚖️"
    else:
        result = "Conservative Leader 🧊"

    return jsonify({
        "message": "Data received successfully",
        "result": result
    })

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(all_users_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)