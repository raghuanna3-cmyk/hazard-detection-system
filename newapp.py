from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the pretrained Keras model
model = load_model('hazard_detection_model.keras')

# Initialize and fit the scaler (you can also load a pre-trained scaler if you have one saved)
scaler = StandardScaler()

# Assuming you have training data to fit the scaler, do it before predictions.
# For example, use some mock training data to fit the scaler (replace this with your actual training data)
mock_training_data = np.array([[40, 80, 30, 1], [50, 85, 25, 0]])  # Example data: [Temperature, Heart_Rate, Gas_Level, Motion]
scaler.fit(mock_training_data)  # Fit the scaler on your training data

# Route to accept sensor data and predict hazard
@app.route('/')
def home():
    return "Welcome to the AI Safety Prediction System!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()  # Get the JSON data from the request

        # Extract the input data
        temperature = data.get('Temperature')
        heart_rate = data.get('Heart_Rate')
        gas_level = data.get('Gas_Level')
        motion = data.get('Motion')

        # Ensure all required fields are present
        if None in [temperature, heart_rate, gas_level, motion]:
            return jsonify({"error": "Missing input data"}), 400

        # Prepare the input data for the model
        input_data = np.array([[temperature, heart_rate, gas_level, motion]])

        # Scale the input data using the pre-fitted scaler
        input_data_scaled = scaler.transform(input_data)

        # Example logic for safety prediction (replace with your model's logic)
        if temperature > 50 or gas_level > 70:
            return jsonify({"status": "unsafe", "escape_route": "Exit A"}), 200
        else:
            return jsonify({"status": "safe", "escape_route": "Stay in place"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
