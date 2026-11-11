from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import heapq
import joblib  # Import joblib for loading the scaler

AI = Flask(__name__)

# Load your trained model
model = load_model('hazard_detection_model.keras')

# Load the saved scaler
scaler = joblib.load('scaler.pkl')

# Example plant map represented as a graph (nodes and edges)
plant_map = {
    'A': {'B': 2, 'C': 5},
    'B': {'A': 2, 'C': 3, 'D': 4},
    'C': {'A': 5, 'B': 3, 'D': 2},
    'D': {'B': 4, 'C': 2, 'Exit': 6},
    'Exit': {}
}

# Dijkstra's algorithm for finding the shortest path in the plant
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

# Define home route (handles both GET and POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Get data from the form submission
            temperature = float(request.form['Temperature'])
            humidity = float(request.form['Humidity'])
            gas_level = float(request.form['Gas_Level'])
            motion = float(request.form['Motion'])
            location = request.form['Location']  # User's current location
            
            # Preprocess the input data
            input_data = np.array([[temperature, humidity, gas_level, motion]])
            input_data_scaled = scaler.transform(input_data)  # Scale the data
            
            # Make prediction using the trained model
            prediction = model.predict(input_data_scaled)

            # Define how to interpret the model's output
            if prediction[0][0] > 0.5:  # Adjust the threshold according to your model
                status = "unsafe"
                # Find shortest route using Dijkstra's algorithm
                distances = dijkstra(plant_map, location)
                escape_route = f"Nearest exit is at {min(distances, key=distances.get)}"
            else:
                status = "safe"
                escape_route = "Stay in place"

            # Return the result on the webpage
            return render_template('index.html', escape_route=escape_route, status=status)

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('index.html', escape_route=None, status=None)

# Define predict route (optional for testing POST requests through Postman or API)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Get JSON data from the request

        # Ensure the input data contains the necessary fields
        if not all(key in data for key in ['Temperature', 'Humidity', 'Gas_Level', 'Motion', 'Location']):
            return jsonify({"error": "Missing data fields"}), 400

        # Extract features from the input data
        temperature = data['Temperature']
        humidity = data['Humidity']
        gas_level = data['Gas_Level']
        motion = data['Motion']
        location = data['Location']

        # Preprocess the input data
        input_data = np.array([[temperature, humidity, gas_level, motion]])
        input_data_scaled = scaler.transform(input_data)  # Scale the data
        
        # Make prediction using the trained model
        prediction = model.predict(input_data_scaled)

        # Define how to interpret the model's output
        if prediction[0][0] > 0.5:  # Adjust the threshold according to your model
            status = "unsafe"
            # Find shortest route using Dijkstra's algorithm
            distances = dijkstra(plant_map, location)
            escape_route = f"Nearest exit is at {min(distances, key=distances.get)}"
        else:
            status = "safe"
            escape_route = "Stay in place"

        # Return the result as a JSON response
        return jsonify({
            "escape_route": escape_route,
            "status": status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
