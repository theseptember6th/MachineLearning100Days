from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the model and scaler
def load_model():
    try:
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the data from the form
        iq = float(request.form['iq'])
        cgpa = float(request.form['cgpa'])
        
        # Load the model
        model = load_model()
        if model is None:
            return jsonify({'error': 'Model not loaded properly'})
        
        # Create a scaler (will be fit on prediction data)
        scaler = StandardScaler()
        
        # Get the mean and std from the model's scaler
        # These values should match what was used during training
        # You might need to adjust these values based on your training data
        cgpa_mean = 6.0  # Approximate mean from your dataset
        cgpa_std = 1.0   # Approximate std from your dataset
        iq_mean = 125.0  # Approximate mean from your dataset
        iq_std = 40.0    # Approximate std from your dataset
        
        # Manually standardize input
        cgpa_scaled = (cgpa - cgpa_mean) / cgpa_std
        iq_scaled = (iq - iq_mean) / iq_std
        
        # Make prediction with standardized input
        input_data = np.array([[cgpa_scaled, iq_scaled]])
        prediction = model.predict(input_data)[0]
        
        # Get prediction probability
        prob = model.predict_proba(input_data)[0][1]
        
        # Return the prediction and probability
        result = {
            'prediction': int(prediction),
            'probability': round(float(prob) * 100, 2),
            'message': 'Placement Likely' if prediction == 1 else 'Placement Unlikely'
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)