import os
import pickle
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
CORS(app, resources={r"/api/*": {"origins": FRONTEND_URL}})

# Model global holder
MODEL = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "height_weight_model.pk")

def load_ml_model():
    """Load trained machine learning model robustly using joblib or pickle."""
    global MODEL
    if not os.path.exists(MODEL_PATH):
        # Fallback to root model path if backend/model doesn't have it
        root_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "height_weight_model.pk")
        if os.path.exists(root_path):
            model_file = root_path
        else:
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH} or {root_path}")
    else:
        model_file = MODEL_PATH

    print(f"Loading model from: {model_file}")
    
    # Try loading with joblib first
    try:
        MODEL = joblib.load(model_file)
        print("Model loaded successfully using joblib.")
        return
    except Exception as j_err:
        print(f"joblib.load failed ({j_err}), trying pickle.load...")

    # Fallback to pickle
    try:
        with open(model_file, "rb") as f:
            MODEL = pickle.load(f)
        print("Model loaded successfully using pickle.")
    except Exception as p_err:
        raise RuntimeError(f"Failed to load model file with joblib or pickle: {p_err}")

# Load model once on application start
try:
    load_ml_model()
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load machine learning model: {e}")
    MODEL = None


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify API status."""
    return jsonify({
        "status": "success",
        "message": "API is running"
    }), 200


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Prediction endpoint.
    Expects JSON input: {"height": 170}
    Returns JSON output: {"success": true, "height": 170, "predicted_weight": 65.42}
    """
    if MODEL is None:
        return jsonify({
            "success": False,
            "error": "Machine learning model is not available on the server."
        }), 500

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({
            "success": False,
            "error": "Invalid request. Please provide JSON data."
        }), 400

    if "height" not in data or data["height"] is None:
        return jsonify({
            "success": False,
            "error": "Please enter your height."
        }), 400

    raw_height = data["height"]

    # Validate numeric type
    try:
        height = float(raw_height)
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Please enter a valid height."
        }), 400

    # Range & positivity validation
    if height <= 0:
        return jsonify({
            "success": False,
            "error": "Please enter a valid height greater than 0."
        }), 400

    if height < 50 or height > 250:
        return jsonify({
            "success": False,
            "error": "Please enter a height between 50 cm and 250 cm."
        }), 400

    # Perform prediction using model.predict([[height]])
    try:
        input_data = np.array([[height]])
        prediction = MODEL.predict(input_data)

        # Extract scalar value from prediction
        if isinstance(prediction, (list, tuple, np.ndarray)):
            predicted_value = float(prediction[0])
        else:
            predicted_value = float(prediction)

        predicted_weight = round(predicted_value, 2)

        return jsonify({
            "success": True,
            "height": height,
            "predicted_weight": predicted_weight
        }), 200

    except Exception as e:
        print(f"Prediction execution error: {e}")
        return jsonify({
            "success": False,
            "error": "Something went wrong during prediction. Please try again."
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found."
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error."
    }), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV", "development") == "development"
    print(f"Starting Flask API on port {port} (debug={debug_mode})...")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
