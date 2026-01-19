#!/usr/bin/env python3
"""
Complete Kidney Stone Prediction Experiment Runner

This script orchestrates the complete workflow:
1. Data preparation and validation
2. AutoML experiment execution
3. Model deployment and testing

Usage:
    python run_experiment.py --data your_data.csv --config config.json
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Import our custom modules
from data_preparation import KidneyStoneDataPreparator
from watson_automl_kidney_predictor import WatsonKidneyStonePredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('experiment_run.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def check_requirements():
    """Check if all required files and configurations are present."""
    required_files = [
        'config.json',
        'requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        logger.error(f"Missing required files: {missing_files}")
        logger.info("Please ensure all required files are present. See README.md for setup instructions.")
        return False

    return True


def prepare_data(data_file: str, skip_preparation: bool = False) -> str:
    """
    Prepare and validate training data.

    Args:
        data_file (str): Path to raw data file
        skip_preparation (bool): Skip data preparation if already done

    Returns:
        str: Path to prepared data file
    """
    if skip_preparation:
        prepared_file = 'kidney_stone_data.csv'
        if os.path.exists(prepared_file):
            logger.info(f"Using existing prepared data: {prepared_file}")
            return prepared_file
        else:
            logger.warning("Prepared data file not found, running preparation anyway")

    logger.info("Starting data preparation...")

    try:
        preparator = KidneyStoneDataPreparator()

        # Run complete preparation pipeline
        prepared_df = preparator.prepare_data_pipeline(
            input_file=data_file,
            output_file='kidney_stone_data.csv',
            handle_missing=True,
            remove_outliers_flag=True,
            scale_features=False,  # Let AutoML handle scaling
            generate_report=True,
            create_visuals=True
        )

        logger.info("Data preparation completed successfully!")
        return 'kidney_stone_data.csv'

    except Exception as e:
        logger.error(f"Data preparation failed: {str(e)}")
        raise


def run_automl_experiment(data_file: str, config_file: str = 'config.json') -> dict:
    """
    Run the AutoML experiment using Watson Studio.

    Args:
        data_file (str): Path to prepared data file
        config_file (str): Path to configuration file

    Returns:
        dict: Experiment results
    """
    logger.info("Starting AutoML experiment...")

    try:
        # Initialize predictor
        predictor = WatsonKidneyStonePredictor(config_file)

        # Authenticate
        predictor.authenticate()

        # Setup experiment
        predictor.setup_experiment()

        # Upload training data
        asset_id = predictor.upload_training_data(data_file)

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

        return {
            'results': results,
            'deployment': deployment_details,
            'pipeline_id': pipeline_details['metadata']['id']
        }

    except Exception as e:
        logger.error(f"AutoML experiment failed: {str(e)}")
        raise


def test_model(deployment_id: str, config_file: str = 'config.json'):
    """
    Test the deployed model with sample data.

    Args:
        deployment_id (str): ID of the deployed model
        config_file (str): Path to configuration file
    """
    logger.info("Testing deployed model...")

    try:
        predictor = WatsonKidneyStonePredictor(config_file)
        predictor.authenticate()

        # Sample patient data (you should replace with real test data)
        sample_data = {
            "input_data": [{
                "fields": ["age", "sex", "blood_pressure", "cholesterol", "sugar", "albumin",
                          "blood_urea", "serum_creatinine", "hemoglobin", "packed_cell_volume",
                          "white_blood_cell_count", "red_blood_cell_count"],
                "values": [
                    # Sample patient 1: Normal patient
                    [45, 1, 80, 1.020, 0, 1, 0, 121, 36, 1.2, 15.4, 44],
                    # Sample patient 2: High risk patient
                    [65, 0, 90, 1.025, 1, 3, 1, 150, 32, 1.1, 12.8, 38]
                ]
            }]
        }

        predictions = predictor.predict(deployment_id, sample_data)

        logger.info("Model testing completed!")
        logger.info(f"Predictions: {predictions}")

        return predictions

    except Exception as e:
        logger.error(f"Model testing failed: {str(e)}")
        raise


def main():
    """Main function to run the complete experiment."""
    parser = argparse.ArgumentParser(description='Run Kidney Stone Prediction AutoML Experiment')
    parser.add_argument('--data', type=str, required=True,
                       help='Path to training data CSV file')
    parser.add_argument('--config', type=str, default='config.json',
                       help='Path to configuration file (default: config.json)')
    parser.add_argument('--skip-prep', action='store_true',
                       help='Skip data preparation step')
    parser.add_argument('--test-only', action='store_true',
                       help='Only run model testing (requires existing deployment)')

    args = parser.parse_args()

    try:
        logger.info("Starting Kidney Stone Prediction Experiment")
        logger.info("=" * 60)

        # Check requirements
        if not check_requirements():
            sys.exit(1)

        if args.test_only:
            # Only run testing
            if not os.path.exists('deployment_info.json'):
                logger.error("Deployment info not found. Run full experiment first.")
                sys.exit(1)

            import json
            with open('deployment_info.json', 'r') as f:
                deployment_info = json.load(f)

            test_model(deployment_info['deployment_id'], args.config)
            return

        # Prepare data
        prepared_data_file = prepare_data(args.data, args.skip_prep)

        # Run AutoML experiment
        experiment_results = run_automl_experiment(prepared_data_file, args.config)

        # Save deployment information
        deployment_info = {
            'deployment_id': experiment_results['deployment']['metadata']['id'],
            'model_name': experiment_results['deployment']['entity']['name'],
            'experiment_results': experiment_results['results']
        }

        with open('deployment_info.json', 'w') as f:
            import json
            json.dump(deployment_info, f, indent=2)

        logger.info("Experiment completed! Deployment info saved to deployment_info.json")

        # Test the model
        logger.info("Testing the deployed model...")
        test_predictions = test_model(deployment_info['deployment_id'], args.config)

        logger.info("=" * 60)
        logger.info("EXPERIMENT COMPLETED SUCCESSFULLY!")
        logger.info(f"Model deployed with ID: {deployment_info['deployment_id']}")
        logger.info("You can now use the model for predictions.")

    except KeyboardInterrupt:
        logger.info("Experiment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Experiment failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()