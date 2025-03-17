import pickle
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the trained model
try:
    with open('malware_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: 'malware_model.pkl' file not found.")
    model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Define the selected features (update based on your model training)
selected_features = [
    "ImageBase", "VersionInformationSize", "SectionsMaxEntropy",
    "MajorOperatingSystemVersion", "ResourcesMinSize", "SizeOfStackReserve",
    "Characteristics", "SizeOfInitializedData", "MajorSubsystemVersion",
    "ResourcesNb", "Subsystem", "ResourcesMinEntropy", "BaseOfData",
    "SizeOfImage"
]

# Preprocessing function
def preprocess_input(data):
    """
    Preprocess the input data for the model.
    Ensures that the input data contains only the selected features.
    """
    try:
        # Keep only the selected features
        data = data[selected_features]
        return data
    except KeyError as e:
        raise ValueError(f"Missing required features: {e}")

# Define the prediction route
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict malware or legitimate file based on input data.
    Expects a JSON payload with feature values.
    """
    if model is None:
        return jsonify({'error': 'Model is not loaded. Please check the server logs.'}), 500

    try:
        # Parse the JSON request
        input_data = request.get_json()  # This expects JSON input, not file data

        if not input_data:
            return jsonify({'error': 'No input data provided'}), 400

        # Convert JSON to DataFrame
        input_df = pd.DataFrame([input_data])

        # Preprocess the input data
        processed_data = preprocess_input(input_df)

        # Debugging: Log processed data
        print(f"Processed Data:\n{processed_data}")

        # Make predictions
        predictions = model.predict(processed_data)
        probabilities = model.predict_proba(processed_data)[:, 1]  # Probability of being malware

        # Prepare the response
        response = {
            'prediction': int(predictions[0]),  # 0 for legitimate, 1 for malware
            'probability': float(probabilities[0])
        }
        return jsonify(response)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({'error': f"Server error: {str(e)}"}), 500

# Define the root route
@app.route('/')
def home():
    """
    Root endpoint to check if the API is running.
    """
    return "Malware Prediction API is running!"

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
