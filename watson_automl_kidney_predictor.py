#!/usr/bin/env python3
"""
IBM Watson Studio AutoML Kidney Stone Predictor

This program uses IBM Watson Studio's AutoML service to create and run
machine learning experiments for predicting kidney stones in patients.

Requirements:
- IBM Watson Studio account
- API key with AutoML permissions
- Training data in CSV format
"""

import os
import json
import time
import logging
from datetime import datetime
from typing import Dict, Optional, List

# IBM Watson SDK imports
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.experiment import AutoAI
from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('watson_automl.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WatsonKidneyStonePredictor:
    """
    A class to handle AutoML experiments for kidney stone prediction using IBM Watson Studio.
    """

    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize the Watson AutoML predictor.

        Args:
            config_path (str): Path to configuration file containing API keys and settings
        """
        self.config = self._load_config(config_path)
        self.client = None
        self.experiment = None
        self.pipeline = None

    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from JSON file.

        Args:
            config_path (str): Path to configuration file

        Returns:
            Dict: Configuration dictionary
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as f:
            config = json.load(f)

        # Validate required configuration
        required_keys = ['api_key', 'url', 'project_id']
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")

        return config

    def authenticate(self) -> None:
        """
        Authenticate with IBM Watson Studio using API key.
        """
        try:
            logger.info("Authenticating with IBM Watson Studio...")

            # Create authenticator
            authenticator = IAMAuthenticator(self.config['api_key'])

            # Initialize Watson ML client
            self.client = APIClient({
                'authenticator': authenticator,
                'version': '2021-06-01'
            })

            # Set the service URL
            self.client.set_service_url(self.config['url'])

            # Verify connection by getting account details
            account_details = self.client.service_instance.get_details()
            logger.info(f"Successfully authenticated. Account: {account_details.get('entity', {}).get('name', 'Unknown')}")

        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise

    def setup_experiment(self, experiment_name: Optional[str] = None,
                        max_runtime: int = 3600) -> None:
        """
        Set up AutoML experiment configuration.

        Args:
            experiment_name (str): Name for the experiment (optional)
            max_runtime (int): Maximum runtime in seconds (default: 1 hour)
        """
        if experiment_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            experiment_name = f"kidney_stone_prediction_{timestamp}"

        try:
            logger.info(f"Setting up AutoML experiment: {experiment_name}")

            # Create AutoAI experiment
            self.experiment = AutoAI(
                wml_credentials={
                    'apikey': self.config['api_key'],
                    'url': self.config['url']
                },
                project_id=self.config['project_id']
            )

            # Configure experiment settings
            self.experiment.metadata.name = experiment_name
            self.experiment.metadata.description = "AutoML experiment for kidney stone prediction"

            logger.info("Experiment setup completed")

        except Exception as e:
            logger.error(f"Failed to setup experiment: {str(e)}")
            raise

    def upload_training_data(self, data_path: str, target_column: str = 'target') -> str:
        """
        Upload training data to Watson Studio.

        Args:
            data_path (str): Path to training data CSV file
            target_column (str): Name of the target column for prediction

        Returns:
            str: Asset ID of uploaded data
        """
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Training data file not found: {data_path}")

        try:
            logger.info(f"Uploading training data from: {data_path}")

            # Upload data asset
            asset_details = self.client.data_assets.store({
                'name': 'kidney_stone_training_data',
                'description': 'Training data for kidney stone prediction',
                'file_path': data_path
            })

            asset_id = self.client.data_assets.get_uid(asset_details)
            logger.info(f"Training data uploaded successfully. Asset ID: {asset_id}")

            return asset_id

        except Exception as e:
            logger.error(f"Failed to upload training data: {str(e)}")
            raise

    def configure_automl_settings(self, prediction_type: str = 'binary',
                                 max_number_of_estimators: int = 4,
                                 training_data_references: Optional[List] = None) -> Dict:
        """
        Configure AutoML experiment settings.

        Args:
            prediction_type (str): Type of prediction ('binary', 'multiclass', 'regression')
            max_number_of_estimators (int): Maximum number of estimators to try
            training_data_references (List): List of training data references

        Returns:
            Dict: AutoML configuration
        """
        automl_config = {
            'prediction_type': prediction_type,
            'prediction_column': 'target',  # Assuming 'target' column contains kidney stone presence
            'max_number_of_estimators': max_number_of_estimators,
            'train_sample_rows_test_size': 0.2,  # 20% for testing
            'include_only_estimators': ['RandomForestClassifier', 'LogisticRegression',
                                      'XGBClassifier', 'LGBMClassifier'],
            'include_batched_ensemble_estimators': [],
            'cognito_transform_names': ['flatten', 'pca', 'isolation_forest'],
            'text_processing': [],
            'word2vec_feature_number': 0,
            'daub_ensemble_mode': 'random',
            'feature_selector_mode': 'auto',
            'imputation_strategy': 'auto',
            'text_processing_options': {}
        }

        if training_data_references:
            automl_config['training_data_references'] = training_data_references

        logger.info(f"AutoML configuration: {json.dumps(automl_config, indent=2)}")
        return automl_config

    def run_experiment(self, data_asset_id: str,
                      prediction_type: str = 'binary',
                      max_runtime: int = 3600) -> Dict:
        """
        Run the AutoML experiment.

        Args:
            data_asset_id (str): ID of uploaded training data
            prediction_type (str): Type of prediction
            max_runtime (int): Maximum runtime in seconds

        Returns:
            Dict: Experiment results
        """
        try:
            logger.info("Starting AutoML experiment...")

            # Configure training data reference
            training_data_references = [{
                'id': data_asset_id,
                'type': 'data_asset',
                'connection': {},
                'location': {}
            }]

            # Get AutoML configuration
            automl_config = self.configure_automl_settings(
                prediction_type=prediction_type,
                training_data_references=training_data_references
            )

            # Initialize optimizer
            optimizer = self.experiment.optimizer(
                name='kidney_stone_optimizer',
                desc='AutoML optimizer for kidney stone prediction',
                prediction_type=prediction_type,
                prediction_column='target',
                scoring='accuracy',
                max_number_of_estimators=4,
                train_sample_rows_test_size=0.2
            )

            # Run the experiment
            pipeline_details = optimizer.fit(
                training_data_references=training_data_references,
                background_mode=False
            )

            logger.info("AutoML experiment completed successfully")
            return pipeline_details

        except Exception as e:
            logger.error(f"AutoML experiment failed: {str(e)}")
            raise

    def get_experiment_results(self, pipeline_details: Dict) -> Dict:
        """
        Get detailed results from the completed experiment.

        Args:
            pipeline_details (Dict): Pipeline details from experiment run

        Returns:
            Dict: Experiment results including metrics and model details
        """
        try:
            logger.info("Retrieving experiment results...")

            # Get pipeline details
            pipeline_id = pipeline_details.get('metadata', {}).get('id')
            if not pipeline_id:
                raise ValueError("Pipeline ID not found in experiment results")

            # Get pipeline details
            pipeline = self.experiment.pipelines.get(pipeline_id=pipeline_id)

            # Get metrics
            metrics = pipeline.get_metrics()

            # Get model details
            model_details = {
                'pipeline_id': pipeline_id,
                'metrics': metrics,
                'status': pipeline_details.get('entity', {}).get('status', {}),
                'created_at': pipeline_details.get('metadata', {}).get('created_at')
            }

            logger.info(f"Experiment results retrieved. Best accuracy: {metrics.get('accuracy', 'N/A')}")
            return model_details

        except Exception as e:
            logger.error(f"Failed to retrieve experiment results: {str(e)}")
            raise

    def deploy_model(self, pipeline_id: str, model_name: str = None) -> Dict:
        """
        Deploy the trained model for predictions.

        Args:
            pipeline_id (str): ID of the pipeline to deploy
            model_name (str): Name for the deployed model

        Returns:
            Dict: Deployment details
        """
        if model_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name = f"kidney_stone_model_{timestamp}"

        try:
            logger.info(f"Deploying model: {model_name}")

            # Create deployment
            deployment_details = self.client.deployments.create(
                artifact_uid=pipeline_id,
                meta_props={
                    self.client.deployments.ConfigurationMetaNames.NAME: model_name,
                    self.client.deployments.ConfigurationMetaNames.ONLINE: {}
                }
            )

            deployment_id = self.client.deployments.get_uid(deployment_details)
            logger.info(f"Model deployed successfully. Deployment ID: {deployment_id}")

            return deployment_details

        except Exception as e:
            logger.error(f"Model deployment failed: {str(e)}")
            raise

    def predict(self, deployment_id: str, input_data: Dict) -> Dict:
        """
        Make predictions using the deployed model.

        Args:
            deployment_id (str): ID of the deployed model
            input_data (Dict): Input data for prediction

        Returns:
            Dict: Prediction results
        """
        try:
            logger.info("Making prediction...")

            # Get scoring endpoint
            scoring_url = self.client.deployments.get_scoring_href(deployment_id)

            # Make prediction
            predictions = self.client.deployments.score(deployment_id, input_data)

            logger.info("Prediction completed successfully")
            return predictions

        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise


def main():
    """
    Main function to run the kidney stone prediction AutoML experiment.
    """
    try:
        # Initialize predictor
        predictor = WatsonKidneyStonePredictor()

        # Authenticate
        predictor.authenticate()

        # Setup experiment
        predictor.setup_experiment()

        # Note: You'll need to provide your own training data
        # For demo purposes, this assumes you have a CSV file with kidney stone data
        data_path = 'kidney_stone_data.csv'  # Replace with your data file

        if os.path.exists(data_path):
            # Upload training data
            asset_id = predictor.upload_training_data(data_path)

            # Run AutoML experiment
            pipeline_details = predictor.run_experiment(asset_id)

            # Get results
            results = predictor.get_experiment_results(pipeline_details)

            # Deploy model
            deployment_details = predictor.deploy_model(
                pipeline_details['metadata']['id'],
                'kidney_stone_predictor'
            )

            logger.info("AutoML experiment completed successfully!")
            logger.info(f"Results: {json.dumps(results, indent=2)}")

        else:
            logger.warning(f"Training data file not found: {data_path}")
            logger.info("Please ensure your training data is available and run the program again.")

    except Exception as e:
        logger.error(f"Program execution failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()