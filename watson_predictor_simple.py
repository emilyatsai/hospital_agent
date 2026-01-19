#!/usr/bin/env python3
"""
Simple Watson ML Predictor (No pandas required)

This module handles IBM Watson Machine Learning predictions using direct API calls.
"""

import requests
import json
import logging
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class SimpleWatsonPredictor:
    """
    A simple Watson ML predictor that uses direct API calls instead of the SDK.
    """

    def __init__(self, api_key: str, deployment_url: str):
        """
        Initialize the predictor.

        Args:
            api_key (str): IBM Cloud API key
            deployment_url (str): Watson ML deployment URL
        """
        self.api_key = api_key
        self.deployment_url = deployment_url
        self.access_token = None
        self.token_expires = None

    def _get_access_token(self) -> str:
        """
        Get or refresh IBM Cloud access token.

        Returns:
            str: Access token
        """
        if self.access_token is None:
            try:
                token_response = requests.post(
                    'https://iam.cloud.ibm.com/identity/token',
                    data={
                        "apikey": self.api_key,
                        "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
                    }
                )
                token_response.raise_for_status()
                self.access_token = token_response.json()["access_token"]
                logger.info("Successfully obtained Watson ML access token")
            except Exception as e:
                logger.error(f"Failed to get access token: {str(e)}")
                raise

        return self.access_token

    def predict(self, features: Dict[str, float]) -> Dict:
        """
        Make a prediction using the Watson ML model.

        Args:
            features (Dict[str, float]): Input features for prediction

        Returns:
            Dict: Prediction results
        """
        try:
            # Get access token
            token = self._get_access_token()

            # Prepare payload
            payload_scoring = {
                "input_data": [{
                    "fields": list(features.keys()),
                    "values": [list(features.values())]
                }]
            }

            # Set headers
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            # Make prediction request
            response = requests.post(
                self.deployment_url,
                json=payload_scoring,
                headers=headers
            )

            response.raise_for_status()
            result = response.json()

            logger.info("Prediction completed successfully")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise Exception(f"Prediction API call failed: {str(e)}")
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise Exception(f"Prediction failed: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test the connection to Watson ML service.

        Returns:
            bool: True if connection is successful
        """
        try:
            token = self._get_access_token()
            return token is not None
        except Exception:
            return False


def load_config(config_file: str = 'config.json') -> Dict:
    """
    Load configuration from JSON file.

    Args:
        config_file (str): Path to configuration file

    Returns:
        Dict: Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_file}")


def create_predictor_from_config(config_file: str = 'config.json') -> SimpleWatsonPredictor:
    """
    Create a predictor instance from configuration file.

    Args:
        config_file (str): Path to configuration file

    Returns:
        SimpleWatsonPredictor: Configured predictor instance
    """
    config = load_config(config_file)

    required_keys = ['api_key', 'deployment_url']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: {key}")

    return SimpleWatsonPredictor(
        api_key=config['api_key'],
        deployment_url=config['deployment_url']
    )


# Example usage
if __name__ == "__main__":
    # Test the predictor
    try:
        predictor = create_predictor_from_config()

        # Test connection
        if predictor.test_connection():
            print("✓ Connection to Watson ML successful")

            # Test prediction with sample data
            sample_features = {
                'gravity': 1.021,
                'ph': 4.91,
                'osmo': 725,
                'cond': 14.0,
                'urea': 443,
                'calc': 2.45
            }

            result = predictor.predict(sample_features)
            print("✓ Prediction successful:")
            print(json.dumps(result, indent=2))
        else:
            print("✗ Failed to connect to Watson ML")

    except Exception as e:
        print(f"Error: {e}")