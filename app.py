from flask import Flask, request, jsonify
from keras.models import load_model
import numpy as np

app = Flask(__name__)

# Load the pretrained Keras model
model = load_model('hazard_detection_model.keras')

# Route to accept sensor data and predict hazard
@app.route('/')
def home():
    return "Welcome to the AI Safety Prediction System!"
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    temperature = data['Temperature']
    heart_rate = data['Heart_Rate']
    gas_level = data['Gas_Level']
    motion = data['Motion']
    
    # Prepare data for prediction (ensure same scaling as during training)
    input_data = np.array([[temperature, heart_rate, gas_level, motion]])
    input_data_scaled = scaler.transform(input_data)
    
    # Make a prediction (0=safe, 1=hazardous)
    prediction = model.predict(input_data_scaled)
    result = 'Hazard detected!' if prediction[0] > 0.5 else 'Site is safe.'
    
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
