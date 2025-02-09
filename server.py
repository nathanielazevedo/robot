from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store the latest command
servo_command = {"angle": None, "dance": False}

@app.route('/command', methods=['GET'])
def get_command():
    return jsonify(servo_command)

@app.route('/set_command', methods=['POST'])
def set_command():
    global servo_command
    data = request.json

    # Ensure the request contains either 'angle' or 'dance'
    if "angle" in data:
        servo_command["angle"] = data["angle"]
        return jsonify({"status": "OK", "message": f"Set angle to {data['angle']}"})
    
    if "dance" in data:
        servo_command["dance"] = data["dance"]
        return jsonify({"status": "OK", "message": f"Set dance to {data['dance']}"})

    return jsonify({"status": "ERROR", "message": "Invalid command, must include 'angle' or 'dance'"}), 400

@app.route('/make_it_dance', methods=['POST'])
def make_it_dance():
    servo_command["dance"] = True
    return jsonify({"status": "OK", "message": "Servo will now dance for 10 seconds!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


