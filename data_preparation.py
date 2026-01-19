#!/usr/bin/env python3
"""
Data Preparation Script for Kidney Stone Prediction

This script helps prepare and validate training data for the Watson AutoML
kidney stone prediction experiment.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KidneyStoneDataPreparator:
    """
    A class to prepare and validate kidney stone prediction data.
    """

    def __init__(self):
        self.required_columns = [
            'age', 'sex', 'blood_pressure', 'cholesterol', 'sugar', 'albumin',
            'blood_urea', 'serum_creatinine', 'hemoglobin', 'packed_cell_volume',
            'white_blood_cell_count', 'red_blood_cell_count', 'target'
        ]

        self.numeric_columns = [
            'age', 'blood_pressure', 'cholesterol', 'sugar', 'albumin',
            'blood_urea', 'serum_creatinine', 'hemoglobin', 'packed_cell_volume',
            'white_blood_cell_count', 'red_blood_cell_count'
        ]

        self.categorical_columns = ['sex']

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            file_path (str): Path to CSV file

        Returns:
            pd.DataFrame: Loaded dataframe
        """
        try:
            logger.info(f"Loading data from: {file_path}")
            df = pd.read_csv(file_path)

            # Remove any unnamed columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            return df

        except Exception as e:
            logger.error(f"Failed to load data: {str(e)}")
            raise

    def validate_columns(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that all required columns are present.

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            Tuple[bool, List[str]]: (is_valid, missing_columns)
        """
        missing_columns = []
        for col in self.required_columns:
            if col not in df.columns:
                missing_columns.append(col)

        is_valid = len(missing_columns) == 0
        return is_valid, missing_columns

    def validate_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Validate and suggest data type corrections.

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            Dict[str, str]: Dictionary of columns with type issues
        """
        type_issues = {}

        # Check numeric columns
        for col in self.numeric_columns:
            if col in df.columns:
                try:
                    pd.to_numeric(df[col], errors='coerce')
                except:
                    type_issues[col] = f"Should be numeric, found: {df[col].dtype}"

        # Check categorical columns
        for col in self.categorical_columns:
            if col in df.columns:
                unique_values = df[col].unique()
                if len(unique_values) > 10:  # Arbitrary threshold
                    type_issues[col] = f"Too many unique values for categorical: {len(unique_values)}"

        # Check target column
        if 'target' in df.columns:
            unique_targets = df['target'].unique()
            if not set(unique_targets).issubset({0, 1}):
                type_issues['target'] = f"Target should be 0 or 1, found: {unique_targets}"

        return type_issues

    def handle_missing_values(self, df: pd.DataFrame,
                            strategy: str = 'median') -> pd.DataFrame:
        """
        Handle missing values in the dataset.

        Args:
            df (pd.DataFrame): Input dataframe
            strategy (str): Strategy for handling missing values ('median', 'mean', 'mode')

        Returns:
            pd.DataFrame: Dataframe with handled missing values
        """
        logger.info(f"Handling missing values using strategy: {strategy}")

        df_clean = df.copy()

        # Handle numeric columns
        for col in self.numeric_columns:
            if col in df_clean.columns:
                missing_count = df_clean[col].isnull().sum()
                if missing_count > 0:
                    if strategy == 'median':
                        fill_value = df_clean[col].median()
                    elif strategy == 'mean':
                        fill_value = df_clean[col].mean()
                    else:
                        fill_value = 0

                    df_clean[col].fillna(fill_value, inplace=True)
                    logger.info(f"Filled {missing_count} missing values in {col} with {fill_value}")

        # Handle categorical columns
        for col in self.categorical_columns:
            if col in df_clean.columns:
                missing_count = df_clean[col].isnull().sum()
                if missing_count > 0:
                    mode_value = df_clean[col].mode().iloc[0]
                    df_clean[col].fillna(mode_value, inplace=True)
                    logger.info(f"Filled {missing_count} missing values in {col} with {mode_value}")

        return df_clean

    def remove_outliers(self, df: pd.DataFrame,
                       method: str = 'iqr',
                       threshold: float = 1.5) -> pd.DataFrame:
        """
        Remove outliers from numeric columns.

        Args:
            df (pd.DataFrame): Input dataframe
            method (str): Outlier detection method ('iqr', 'zscore')
            threshold (float): Threshold for outlier detection

        Returns:
            pd.DataFrame: Dataframe with outliers removed
        """
        logger.info(f"Removing outliers using method: {method}")

        df_clean = df.copy()

        for col in self.numeric_columns:
            if col in df_clean.columns:
                if method == 'iqr':
                    Q1 = df_clean[col].quantile(0.25)
                    Q3 = df_clean[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR

                    outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound))
                    outlier_count = outliers.sum()

                    if outlier_count > 0:
                        df_clean = df_clean[~outliers]
                        logger.info(f"Removed {outlier_count} outliers from {col}")

                elif method == 'zscore':
                    z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
                    outliers = z_scores > threshold
                    outlier_count = outliers.sum()

                    if outlier_count > 0:
                        df_clean = df_clean[~outliers]
                        logger.info(f"Removed {outlier_count} outliers from {col}")

        return df_clean

    def encode_categorical_variables(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Encode categorical variables.

        Args:
            df (pd.DataFrame): Input dataframe

        Returns:
            pd.DataFrame: Dataframe with encoded categorical variables
        """
        logger.info("Encoding categorical variables")

        df_encoded = df.copy()

        for col in self.categorical_columns:
            if col in df_encoded.columns:
                # Simple label encoding for binary categories
                unique_values = df_encoded[col].unique()
                if len(unique_values) <= 2:
                    le = LabelEncoder()
                    df_encoded[col] = le.fit_transform(df_encoded[col])
                    logger.info(f"Label encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
                else:
                    # One-hot encoding for multi-class categories
                    dummies = pd.get_dummies(df_encoded[col], prefix=col)
                    df_encoded = pd.concat([df_encoded.drop(col, axis=1), dummies], axis=1)
                    logger.info(f"One-hot encoded {col} into {len(dummies.columns)} columns")

        return df_encoded

    def scale_numeric_features(self, df: pd.DataFrame,
                              columns: Optional[List[str]] = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Scale numeric features using StandardScaler.

        Args:
            df (pd.DataFrame): Input dataframe
            columns (List[str]): Columns to scale (default: all numeric columns)

        Returns:
            Tuple[pd.DataFrame, Dict]: (scaled_dataframe, scaler_info)
        """
        if columns is None:
            columns = self.numeric_columns

        logger.info(f"Scaling numeric features: {columns}")

        df_scaled = df.copy()
        scaler_info = {}

        scaler = StandardScaler()

        # Fit and transform the data
        scaled_data = scaler.fit_transform(df_scaled[columns])
        df_scaled[columns] = scaled_data

        # Store scaler parameters for later use
        scaler_info['mean'] = scaler.mean_.tolist()
        scaler_info['scale'] = scaler.scale_.tolist()
        scaler_info['columns'] = columns

        logger.info("Feature scaling completed")
        return df_scaled, scaler_info

    def generate_data_report(self, df: pd.DataFrame,
                           output_file: str = 'data_report.txt') -> None:
        """
        Generate a comprehensive data report.

        Args:
            df (pd.DataFrame): Input dataframe
            output_file (str): Output file path for the report
        """
        logger.info(f"Generating data report: {output_file}")

        with open(output_file, 'w') as f:
            f.write("KIDNEY STONE PREDICTION DATA REPORT\n")
            f.write("=" * 50 + "\n\n")

            # Basic information
            f.write(f"Dataset Shape: {df.shape}\n")
            f.write(f"Number of Features: {df.shape[1]}\n")
            f.write(f"Number of Samples: {df.shape[0]}\n\n")

            # Data types
            f.write("DATA TYPES:\n")
            f.write("-" * 20 + "\n")
            for col, dtype in df.dtypes.items():
                f.write(f"{col}: {dtype}\n")
            f.write("\n")

            # Missing values
            f.write("MISSING VALUES:\n")
            f.write("-" * 20 + "\n")
            missing_info = df.isnull().sum()
            for col, count in missing_info.items():
                if count > 0:
                    percentage = (count / len(df)) * 100
                    f.write(f"{col}: {count} ({percentage:.2f}%)\n")
            if missing_info.sum() == 0:
                f.write("No missing values found.\n")
            f.write("\n")

            # Target distribution
            if 'target' in df.columns:
                f.write("TARGET DISTRIBUTION:\n")
                f.write("-" * 25 + "\n")
                target_counts = df['target'].value_counts()
                for value, count in target_counts.items():
                    percentage = (count / len(df)) * 100
                    f.write(f"Class {value}: {count} ({percentage:.2f}%)\n")
                f.write("\n")

            # Statistical summary
            f.write("STATISTICAL SUMMARY:\n")
            f.write("-" * 25 + "\n")
            f.write(str(df.describe()))
            f.write("\n\n")

            # Correlation with target
            if 'target' in df.columns:
                f.write("CORRELATION WITH TARGET:\n")
                f.write("-" * 30 + "\n")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                correlations = df[numeric_cols].corr()['target'].sort_values(ascending=False)
                for col, corr in correlations.items():
                    if col != 'target':
                        f.write(f"{col}: {corr:.4f}\n")
                f.write("\n")

        logger.info(f"Data report saved to: {output_file}")

    def create_visualizations(self, df: pd.DataFrame,
                            output_dir: str = 'visualizations') -> None:
        """
        Create visualizations for data analysis.

        Args:
            df (pd.DataFrame): Input dataframe
            output_dir (str): Output directory for visualizations
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        logger.info(f"Creating visualizations in: {output_dir}")

        # Set style
        plt.style.use('default')
        sns.set_palette("husl")

        # Target distribution
        plt.figure(figsize=(8, 6))
        target_counts = df['target'].value_counts()
        plt.pie(target_counts, labels=['No Kidney Stone', 'Kidney Stone'],
                autopct='%1.1f%%', startangle=90)
        plt.title('Target Distribution')
        plt.savefig(f'{output_dir}/target_distribution.png')
        plt.close()

        # Correlation heatmap
        plt.figure(figsize=(12, 10))
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title('Feature Correlation Heatmap')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/correlation_heatmap.png')
        plt.close()

        # Distribution plots for key features
        key_features = ['age', 'blood_pressure', 'hemoglobin', 'serum_creatinine']
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.ravel()

        for i, feature in enumerate(key_features):
            if feature in df.columns:
                sns.histplot(data=df, x=feature, hue='target', ax=axes[i], alpha=0.7)
                axes[i].set_title(f'{feature.title()} Distribution by Target')

        plt.tight_layout()
        plt.savefig(f'{output_dir}/feature_distributions.png')
        plt.close()

        logger.info("Visualizations created successfully")

    def prepare_data_pipeline(self, input_file: str,
                            output_file: str = 'prepared_kidney_data.csv',
                            handle_missing: bool = True,
                            remove_outliers_flag: bool = True,
                            scale_features: bool = True,
                            generate_report: bool = True,
                            create_visuals: bool = True) -> pd.DataFrame:
        """
        Complete data preparation pipeline.

        Args:
            input_file (str): Input CSV file path
            output_file (str): Output CSV file path
            handle_missing (bool): Whether to handle missing values
            remove_outliers_flag (bool): Whether to remove outliers
            scale_features (bool): Whether to scale numeric features
            generate_report (bool): Whether to generate data report
            create_visuals (bool): Whether to create visualizations

        Returns:
            pd.DataFrame: Prepared dataframe
        """
        logger.info("Starting data preparation pipeline")

        # Load data
        df = self.load_data(input_file)

        # Validate columns
        is_valid, missing_cols = self.validate_columns(df)
        if not is_valid:
            raise ValueError(f"Missing required columns: {missing_cols}")

        # Validate data types
        type_issues = self.validate_data_types(df)
        if type_issues:
            logger.warning(f"Data type issues found: {type_issues}")

        # Handle missing values
        if handle_missing:
            df = self.handle_missing_values(df)

        # Remove outliers
        if remove_outliers_flag:
            df = self.remove_outliers(df)

        # Encode categorical variables
        df = self.encode_categorical_variables(df)

        # Scale features
        if scale_features:
            df, scaler_info = self.scale_numeric_features(df)
            # Save scaler info for later use
            import json
            with open('scaler_info.json', 'w') as f:
                json.dump(scaler_info, f)

        # Generate report
        if generate_report:
            self.generate_data_report(df)

        # Create visualizations
        if create_visuals:
            self.create_visualizations(df)

        # Save prepared data
        df.to_csv(output_file, index=False)
        logger.info(f"Prepared data saved to: {output_file}")

        logger.info("Data preparation pipeline completed")
        return df


def main():
    """
    Main function for data preparation.
    """
    # Example usage
    preparator = KidneyStoneDataPreparator()

    # Replace 'your_data.csv' with your actual data file
    input_file = 'kidney_stone_raw_data.csv'

    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        logger.info("Please place your kidney stone data CSV file in the project directory")
        return

    try:
        # Run complete preparation pipeline
        prepared_df = preparator.prepare_data_pipeline(
            input_file=input_file,
            output_file='kidney_stone_data.csv',
            handle_missing=True,
            remove_outliers_flag=True,
            scale_features=False,  # Watson AutoML handles scaling
            generate_report=True,
            create_visuals=True
        )

        logger.info("Data preparation completed successfully!")
        logger.info(f"Final dataset shape: {prepared_df.shape}")

    except Exception as e:
        logger.error(f"Data preparation failed: {str(e)}")
        raise


if __name__ == "__main__":
    import os
    main()