#!/usr/bin/env python3
"""
Flask Web Application for Kidney Stone Prediction

This application provides a web interface for predicting kidney stone presence
using IBM Watson AutoML deployed model.
"""

import os
import json
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from typing import Dict, Optional
import requests

# Import our simple Watson predictor (no pandas required)
from watson_predictor_simple import SimpleWatsonPredictor, create_predictor_from_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize Watson predictor (lazy loading)
watson_predictor = None

def get_watson_predictor():
    """Get or initialize Watson predictor."""
    global watson_predictor
    if watson_predictor is None:
        try:
            config_file = 'config.json'
            if not os.path.exists(config_file):
                logger.error("Configuration file not found. Please run setup first.")
                return None

            watson_predictor = create_predictor_from_config(config_file)

            # Test connection
            if watson_predictor.test_connection():
                logger.info("Watson predictor initialized and tested successfully")
            else:
                logger.error("Failed to connect to Watson ML service")
                return None

        except Exception as e:
            logger.error(f"Failed to initialize Watson predictor: {str(e)}")
            return None
    return watson_predictor

@app.route('/')
def index():
    """Home page with prediction form."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Get form data
        form_data = request.form

        # Validate required fields
        required_fields = ['gravity', 'ph', 'osmo', 'cond', 'urea', 'calc']
        missing_fields = []

        for field in required_fields:
            if field not in form_data or not form_data[field].strip():
                missing_fields.append(field)

        if missing_fields:
            flash(f"Missing required fields: {', '.join(missing_fields)}", 'error')
            return redirect(url_for('index'))

        # Convert form data to proper types
        try:
            input_data = {
                'gravity': float(form_data['gravity']),
                'ph': float(form_data['ph']),
                'osmo': float(form_data['osmo']),
                'cond': float(form_data['cond']),
                'urea': float(form_data['urea']),
                'calc': float(form_data['calc'])
            }
        except ValueError as e:
            flash(f"Invalid numeric input: {str(e)}", 'error')
            return redirect(url_for('index'))

        # Dummy prediction for testing (always returns 1 = kidney stone present)
        logger.info("Using dummy prediction mode")
        # Simulate prediction result
        prediction_result = {
            'predictions': [{
                'values': [[1, 0.85]]  # Always predict 1 with 85% confidence
            }]
        }

        # Process prediction result
        # The Watson ML API response structure
        if 'predictions' in prediction_result:
            predictions = prediction_result['predictions']
            if predictions and len(predictions) > 0:
                prediction_values = predictions[0].get('values', [])
                if prediction_values and len(prediction_values) > 0:
                    predicted_class = prediction_values[0][0]  # First prediction value
                    probability = prediction_values[0][1] if len(prediction_values[0]) > 1 else None

                    # Interpret result
                    kidney_stone_present = predicted_class == 1
                    confidence = probability if probability is not None else 0.5

                    result = {
                        'prediction': kidney_stone_present,
                        'confidence': round(confidence * 100, 2),
                        'input_data': input_data
                    }

                    return render_template('result.html', result=result)

        # Try alternative response format (direct API might be different)
        elif 'values' in prediction_result:
            prediction_values = prediction_result['values']
            if prediction_values and len(prediction_values) > 0:
                predicted_class = prediction_values[0][0]
                probability = prediction_values[0][1] if len(prediction_values[0]) > 1 else None

                kidney_stone_present = predicted_class == 1
                confidence = probability if probability is not None else 0.5

                result = {
                    'prediction': kidney_stone_present,
                    'confidence': round(confidence * 100, 2),
                    'input_data': input_data
                }

                return render_template('result.html', result=result)

        # If we get here, something went wrong with the prediction
        flash("Prediction failed. Please try again.", 'error')
        return redirect(url_for('index'))

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        flash(f"An error occurred during prediction: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions."""
    try:
        data = request.get_json()

        if not data or 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400

        features = data['features']

        # Validate features
        required_features = ['gravity', 'ph', 'osmo', 'cond', 'urea', 'calc']
        for feature in required_features:
            if feature not in features:
                return jsonify({'error': f'Missing feature: {feature}'}), 400

        # Dummy prediction for testing (always returns 1 = kidney stone present)
        logger.info("API: Using dummy prediction mode")
        # Simulate prediction result
        prediction_result = {
            'predictions': [{
                'values': [[1, 0.85]]  # Always predict 1 with 85% confidence
            }]
        }

        if 'predictions' in prediction_result:
            predictions = prediction_result['predictions']
            if predictions and len(predictions) > 0:
                prediction_values = predictions[0].get('values', [])
                if prediction_values and len(prediction_values) > 0:
                    predicted_class = prediction_values[0][0]
                    probability = prediction_values[0][1] if len(prediction_values[0]) > 1 else None

                    return jsonify({
                        'prediction': int(predicted_class),
                        'kidney_stone_present': predicted_class == 1,
                        'confidence': round((probability or 0.5) * 100, 2),
                        'features': features
                    })

        return jsonify({'error': 'Prediction failed'}), 500

    except Exception as e:
        logger.error(f"API prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'mode': 'dummy_predictions',
        'note': 'Using dummy predictions (always returns 1) for testing interface'
    })

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/data')
def data_info():
    """Data information page."""
    return render_template('data.html')

if __name__ == '__main__':
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))

    # Run the app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )