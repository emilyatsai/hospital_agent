#!/usr/bin/env python3
"""
Test the Simple Watson Predictor

This script tests the direct API integration with IBM Watson ML.
"""

import json
from watson_predictor_simple import SimpleWatsonPredictor

def test_predictor():
    """Test the predictor with sample data."""

    # Load configuration
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found. Please run setup.py first.")
        return

    # Check if required config exists
    if 'api_key' not in config or 'deployment_url' not in config:
        print("❌ Missing required configuration (api_key or deployment_url)")
        print("Please edit config.json with your credentials.")
        return

    print("🔧 Initializing Watson Predictor...")
    print(f"API Key: {config['api_key'][:10]}...")
    print(f"Deployment URL: {config['deployment_url']}")

    try:
        # Create predictor
        predictor = SimpleWatsonPredictor(
            api_key=config['api_key'],
            deployment_url=config['deployment_url']
        )

        # Test connection
        print("\n🔗 Testing connection...")
        if not predictor.test_connection():
            print("❌ Connection test failed. Check your API key and deployment URL.")
            return

        print("✅ Connection successful!")

        # Test prediction with sample data
        sample_data = {
            'gravity': 1.021,
            'ph': 4.91,
            'osmo': 725,
            'cond': 14.0,
            'urea': 443,
            'calc': 2.45
        }

        print(f"\n🔮 Testing prediction with sample data: {sample_data}")

        result = predictor.predict(sample_data)

        print("✅ Prediction successful!")
        print("📊 Result:", json.dumps(result, indent=2))

        # Check if result has expected structure
        if 'predictions' in result and len(result['predictions']) > 0:
            prediction_values = result['predictions'][0].get('values', [])
            if prediction_values:
                predicted_class = prediction_values[0][0]
                probability = prediction_values[0][1] if len(prediction_values[0]) > 1 else None

                print("\n🎯 Prediction Summary:")
                print(f"   Class: {predicted_class} ({'High Risk' if predicted_class == 1 else 'Low Risk'})")
                if probability:
                    print(f"   Confidence: {probability:.2%}")

        print("\n🎉 All tests passed! Your predictor is ready to use.")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your API key is valid")
        print("2. Verify the deployment URL is correct")
        print("3. Ensure your model is deployed and accessible")
        print("4. Check your network connection")

if __name__ == "__main__":
    print("🧪 WATSON PREDICTOR TEST")
    print("=" * 40)
    test_predictor()