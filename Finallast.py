from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load your trained model
model = load_model('hazard_detection_model.keras')

# Define home route (handles both GET and POST)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            # Get data from the form submission
            temperature = float(request.form['Temperature'])
            heart_rate = float(request.form['Heart_Rate'])
            gas_level = float(request.form['Gas_Level'])
            motion = float(request.form['Motion'])
            
            # Preprocess the input data (you may need to adjust this step based on your model)
            input_data = np.array([[temperature, heart_rate, gas_level, motion]])
            scaler = StandardScaler()  # Example scaler, adjust if needed
            input_data_scaled = scaler.fit_transform(input_data)  # Scale the data
            
            # Make prediction using the trained model
            prediction = model.predict(input_data_scaled)

            # Define how to interpret the model's output
            if prediction[0][0] > 0.5:  # Adjust the threshold according to your model
                status = "unsafe"
                escape_route = "Evacuate immediately"
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
        if not all(key in data for key in ['Temperature', 'Heart_Rate', 'Gas_Level', 'Motion']):
            return jsonify({"error": "Missing data fields"}), 400

        # Extract features from the input data
        temperature = data['Temperature']
        heart_rate = data['Heart_Rate']
        gas_level = data['Gas_Level']
        motion = data['Motion']

        # Preprocess the input data (you may need to adjust this step based on your model)
        input_data = np.array([[temperature, heart_rate, gas_level, motion]])
        scaler = StandardScaler()  # Example scaler, adjust if needed
        input_data_scaled = scaler.fit_transform(input_data)  # Scale the data
        
        # Make prediction using the trained model
        prediction = model.predict(input_data_scaled)

        # Define how to interpret the model's output
        if prediction[0][0] > 0.5:  # Adjust the threshold according to your model
            status = "unsafe"
            escape_route = "Evacuate immediately"
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
