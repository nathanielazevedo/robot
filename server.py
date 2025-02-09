from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store the latest command
servo_command = {"angle": None}

@app.route('/command', methods=['GET'])
def get_command():
    global servo_command
    return jsonify(servo_command)

@app.route('/set_command', methods=['POST'])
def set_command():
    global servo_command
    data = request.json
    if "angle" in data:
        servo_command["angle"] = data["angle"]
        return jsonify({"status": "OK", "message": f"Set angle to {data['angle']}"})
    return jsonify({"status": "ERROR", "message": "Invalid command"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

