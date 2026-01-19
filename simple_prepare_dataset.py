#!/usr/bin/env python3
"""
Simple Dataset Preparation (No pandas required)

This script prepares the kidney stone dataset without requiring pandas.
"""

import csv
import os

def prepare_dataset_simple():
    """Prepare the kidney stone dataset using only standard library."""

    source_file = "/Users/macbookpro/Downloads/kidney-stone-dataset.csv"
    target_file = "kidney_stone_raw_data.csv"

    if not os.path.exists(source_file):
        print(f"Source file not found: {source_file}")
        print("Please ensure the kidney-stone-dataset.csv file is in your Downloads folder.")
        return False

    try:
        print("Reading kidney stone dataset...")

        # Read the CSV file
        with open(source_file, 'r', newline='') as infile:
            # Skip the first row if it contains unwanted data
            lines = infile.readlines()

            # Check if first line looks like an index column issue
            first_line = lines[0].strip()
            if first_line.startswith('|') or first_line.startswith(',gravity'):
                # Skip the first line if it's an index or header issue
                data_lines = lines[1:]
            else:
                data_lines = lines

        # Parse CSV data
        csv_reader = csv.reader(data_lines)
        rows = list(csv_reader)

        # Clean the data
        cleaned_rows = []
        for row in rows:
            # Skip empty rows
            if not row or all(cell.strip() == '' for cell in row):
                continue

            # Remove the first column if it's an index
            if len(row) > 7 and row[0].strip().isdigit():
                row = row[1:]

            # Ensure we have the right number of columns
            if len(row) >= 7:
                cleaned_rows.append(row[:7])  # gravity, ph, osmo, cond, urea, calc, target

        if not cleaned_rows:
            print("No valid data found in the file.")
            return False

        # Check header
        header = cleaned_rows[0]
        expected_header = ['gravity', 'ph', 'osmo', 'cond', 'urea', 'calc', 'target']

        # Write cleaned data
        with open(target_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(expected_header)
            writer.writerows(cleaned_rows[1:])  # Skip header

        # Basic statistics
        print(f"Dataset processed successfully!")
        print(f"Total rows (including header): {len(cleaned_rows)}")
        print(f"Data rows: {len(cleaned_rows) - 1}")

        # Count classes
        target_counts = {}
        for row in cleaned_rows[1:]:  # Skip header
            if len(row) >= 7:
                target = row[6].strip()
                target_counts[target] = target_counts.get(target, 0) + 1

        print(f"Target distribution: {target_counts}")

        print(f"Dataset saved to: {target_file}")
        return True

    except Exception as e:
        print(f"Error preparing dataset: {e}")
        return False

if __name__ == "__main__":
    print("SIMPLE KIDNEY STONE DATASET PREPARATION")
    print("=" * 45)

    success = prepare_dataset_simple()

    if not success:
        print("\nFailed to prepare dataset. Please check the file format.")
        print("Alternative: You can create kidney_stone_raw_data.csv manually with columns:")
        print("gravity,ph,osmo,cond,urea,calc,target")
    else:
        print("\nNext steps:")
        print("1. Configure your Watson credentials: python setup.py")
        print("2. Run the experiment: python run_experiment.py --data kidney_stone_raw_data.csv")
        print("3. Start the web app: python run_webapp.py")