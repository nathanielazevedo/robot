from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sock import Sock
import queue
import threading
import time

app = Flask(__name__)
CORS(app)
sock = Sock(app)  # Native WebSocket support

# Queue to manage dance commands
dance_queue = queue.Queue()
queue_list = []  # Track names in queue
current_dancer = None  # Track the dancer currently performing

def process_dance_queue():
    """Continuously process dance requests from the queue."""
    global current_dancer
    while True:
        try:
            name = dance_queue.get(timeout=1)  # ✅ Wait for an item or timeout
            queue_list.pop(0)  # ✅ Remove the first name from queue_list
            current_dancer = name
            print(f"🕺 Processing dance request from {current_dancer}...")  

            # Notify ESP32 via WebSocket
            with app.app_context():
                for ws in clients:
                    ws.send(f"DANCE:{current_dancer}")

            time.sleep(10)  # Simulate dance duration
            print(f"✅ {current_dancer}'s dance completed.")
            current_dancer = None  # Clear current dancer after dancing

            dance_queue.task_done()  # ✅ Only call task_done() if an item was dequeued

        except queue.Empty:  # ✅ Avoid calling task_done() if queue is empty
            continue


# Start background worker thread
worker_thread = threading.Thread(target=process_dance_queue, daemon=True)
worker_thread.start()

clients = set()  # Store active WebSocket connections

@app.route('/make_it_dance', methods=['POST'])
def make_it_dance():
    """Handles dance requests and adds them to the queue."""
    data = request.json
    if "name" not in data:
        return jsonify({"status": "ERROR", "message": "Missing 'name' field"}), 400

    name = data["name"]
    dance_queue.put(name)  # Add request to queue
    queue_list.append(name)  # Track names in queue

    return jsonify({"status": "OK", "message": f"{name} added to the dance queue!"})

@app.route('/queue_status', methods=['GET'])
def queue_status():
    """Returns the current queue list and who's dancing."""
    return jsonify({
        "queue": queue_list,
        "current_dancer": current_dancer
    })

@sock.route('/ws')  # Native WebSocket connection
def websocket_connection(ws):
    """Handles WebSocket connections from ESP32."""
    print("✅ ESP32 WebSocket Connected!")
    clients.add(ws)

    try:
        while True:
            msg = ws.receive()  # Listen for messages from ESP32
            print("📩 Received:", msg)

    except Exception as e:
        print("❌ WebSocket Error:", e)
    finally:
        clients.remove(ws)
        print("❌ ESP32 WebSocket Disconnected!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
