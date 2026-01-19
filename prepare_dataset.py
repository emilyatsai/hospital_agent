#!/usr/bin/env python3
"""
Prepare Kidney Stone Dataset

This script helps prepare the kidney stone dataset for training.
"""

import os
import pandas as pd
import shutil

def prepare_dataset():
    """Prepare the kidney stone dataset from the provided file."""

    source_file = "/Users/macbookpro/Downloads/kidney-stone-dataset.csv"
    target_file = "kidney_stone_raw_data.csv"

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        print("Please ensure the kidney-stone-dataset.csv file is in your Downloads folder.")
        return False

    try:
        # Read the dataset
        print("Reading kidney stone dataset...")
        df = pd.read_csv(source_file)

        # Clean the dataset (remove the index column if present)
        if df.columns[0].startswith('Unnamed') or df.columns[0] == '':
            df = df.iloc[:, 1:]  # Remove first column if it's an unnamed index

        # Ensure column names are clean
        df.columns = df.columns.str.strip()

        # Basic data validation
        required_columns = ['gravity', 'ph', 'osmo', 'cond', 'urea', 'calc', 'target']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Warning: Missing columns: {missing_columns}")

        # Show basic statistics
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Target distribution:\n{df['target'].value_counts()}")

        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print(f"Missing values:\n{missing_values[missing_values > 0]}")
        else:
            print("No missing values found.")

        # Save cleaned dataset
        df.to_csv(target_file, index=False)
        print(f"Dataset saved to: {target_file}")

        print("\nDataset preparation completed!")
        print(f"You can now run: python run_experiment.py --data {target_file}")

        return True

    except Exception as e:
        print(f"Error preparing dataset: {e}")
        return False

if __name__ == "__main__":
    print("KIDNEY STONE DATASET PREPARATION")
    print("=" * 40)

    success = prepare_dataset()

    if not success:
        print("\nFailed to prepare dataset. Please check the file path and format.")
    else:
        print("\nNext steps:")
        print("1. Configure your Watson credentials: python setup.py")
        print("2. Run the experiment: python run_experiment.py --data kidney_stone_raw_data.csv")
        print("3. Start the web app: python run_webapp.py")