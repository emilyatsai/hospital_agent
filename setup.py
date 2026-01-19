#!/usr/bin/env python3
"""
Setup script for Kidney Stone Predictor project.

This script helps users set up their environment and configuration.
"""

import os
import json
import shutil
from pathlib import Path


def setup_config():
    """Set up the configuration file from template."""
    if os.path.exists('config.json'):
        print("Config file already exists. Skipping setup.")
        return

    if not os.path.exists('config_template.json'):
        print("Error: config_template.json not found!")
        return

    print("\n" + "="*60)
    print("IBM WATSON STUDIO CONFIGURATION SETUP")
    print("="*60)

    # Copy template to config
    shutil.copy('config_template.json', 'config.json')
    print("✓ Created config.json from template")

    print("\nPlease edit config.json and fill in your credentials:")
    print("1. IBM Cloud API Key")
    print("2. Watson ML Deployment URL (with your deployment ID)")
    print("\nSee README.md for detailed instructions on obtaining these credentials.")
    print("\nExample deployment URL format:")
    print("https://private.au-syd.ml.cloud.ibm.com/ml/v4/deployments/YOUR_DEPLOYMENT_ID/predictions?version=2021-05-01")

    input("\nPress Enter when you have configured config.json...")


def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)

    try:
        import ibm_watson_machine_learning
        print("✓ ibm-watson-machine-learning installed")
    except ImportError:
        print("✗ ibm-watson-machine-learning not found")
        print("Run: pip install -r requirements.txt")
        return False

    try:
        import pandas
        print("✓ pandas installed")
    except ImportError:
        print("✗ pandas not found")
        return False

    try:
        import numpy
        print("✓ numpy installed")
    except ImportError:
        print("✗ numpy not found")
        return False

    try:
        import sklearn
        print("✓ scikit-learn installed")
    except ImportError:
        print("✗ scikit-learn not found")
        return False

    print("✓ All required dependencies are installed")
    return True


def create_sample_data():
    """Create a sample data file for testing."""
    print("\n" + "="*60)
    print("CREATING SAMPLE DATA")
    print("="*60)

    if os.path.exists('kidney_stone_raw_data.csv'):
        print("Sample data file already exists.")
        return

    # Create sample kidney stone data
    sample_data = """age,sex,blood_pressure,cholesterol,sugar,albumin,blood_urea,serum_creatinine,hemoglobin,packed_cell_volume,white_blood_cell_count,red_blood_cell_count,target
45,1,80,1.020,0,1,0,121,36,1.2,15.4,44,7800,5.2,1
65,0,90,1.025,1,3,1,150,32,1.1,12.8,38,8400,4.8,0
50,1,70,1.010,0,0,0,98,40,1.3,18.2,48,10200,6.1,1
70,0,85,1.015,1,2,1,142,28,0.9,11.6,35,9200,4.2,0
55,1,75,1.018,0,1,1,115,34,1.1,14.8,42,7600,5.0,1
48,0,82,1.022,0,2,0,135,38,1.2,16.5,46,8200,5.4,1
60,1,88,1.024,1,3,1,165,30,1.0,13.2,40,8900,4.5,0
42,1,78,1.016,0,1,0,108,39,1.25,17.1,47,8000,5.6,1
67,0,92,1.026,1,4,1,180,25,0.8,10.9,32,9500,3.8,0
52,1,72,1.012,0,0,0,95,41,1.35,19.0,49,7800,5.8,1"""

    with open('kidney_stone_raw_data.csv', 'w') as f:
        f.write(sample_data)

    print("✓ Created sample data file: kidney_stone_raw_data.csv")
    print("Note: This is synthetic data for testing purposes only.")


def main():
    """Main setup function."""
    print("KIDNEY STONE PREDICTOR - SETUP SCRIPT")
    print("This script will help you set up the project environment.")

    # Check if we're in the right directory
    if not os.path.exists('watson_automl_kidney_predictor.py'):
        print("Error: Please run this script from the project root directory.")
        return

    # Install dependencies
    print("\nInstalling dependencies...")
    os.system('pip install -r requirements.txt')

    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and run setup again.")
        return

    # Setup configuration
    setup_config()

    # Create sample data
    create_sample_data()

    print("\n" + "="*60)
    print("SETUP COMPLETED!")
    print("="*60)
    print("Next steps:")
    print("1. Edit config.json with your IBM Watson credentials")
    print("2. Run the experiment: python run_experiment.py --data kidney_stone_raw_data.csv")
    print("\nFor detailed instructions, see README.md")


if __name__ == "__main__":
    main()