# IBM Watson Studio AutoML Kidney Stone Predictor

This program uses IBM Watson Studio's AutoML service to automatically create and train machine learning models for predicting kidney stones in patients.

## Features

- Automated machine learning experiment setup
- Data upload and preprocessing
- Model training with multiple algorithms
- Model evaluation and deployment
- Prediction API for new patient data

## Prerequisites

1. **IBM Cloud Account**: You need an active IBM Cloud account
2. **Watson Studio Instance**: A Watson Studio service instance in IBM Cloud
3. **Python 3.7+**: Python environment with required packages
4. **Training Data**: CSV file with patient data for kidney stone prediction

## Setup Instructions

### 1. Install Dependencies

For Python 3.13 compatibility, use the basic requirements:

```bash
pip install -r requirements_basic.txt
```

**Note:** If you encounter issues with pandas on Python 3.13, the basic requirements exclude pandas and use only standard library + numpy for data processing.

### Python 3.13 Compatibility

This application has been updated to work with Python 3.13 by:

- **Simplified Watson Integration**: Uses direct API calls instead of the ibm-watson-machine-learning SDK
- **No Pandas Dependency**: Data processing uses standard library CSV module
- **Lightweight Requirements**: Only essential packages required

The simplified approach provides the same functionality with better compatibility across Python versions.

### 2. Get IBM Watson API Credentials

#### Step 2.1: Create Watson Machine Learning Service
1. Go to [IBM Cloud](https://cloud.ibm.com/)
2. Search for "Watson Machine Learning" in the catalog
3. Create a new service instance
4. Note down the service credentials and instance ID

#### Step 2.2: Create Watson Studio Project
1. Go to [Watson Studio](https://watsonstudio.cloud.ibm.com/)
2. Create a new project
3. Note down the Project ID from the project settings

#### Step 2.3: Generate API Key
1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Create a new API key
3. Download and save the API key securely

### 3. Configure API Credentials

1. Copy the configuration template:
```bash
cp config_template.json config.json
```

2. Edit `config.json` and fill in your credentials:
```json
{
  "api_key": "your_ibm_api_key_here",
  "url": "https://us-south.ml.cloud.ibm.com",
  "project_id": "your_watson_studio_project_id_here",
  "region": "us-south",
  "instance_id": "your_watson_ml_instance_id_here"
}
```

### 4. Prepare Training Data

Your training data should be in CSV format with the following structure:

```csv
age,sex,blood_pressure,cholesterol,sugar,albumin,blood_urea,serum_creatinine,hemoglobin,packed_cell_volume,white_blood_cell_count,red_blood_cell_count,target
48,1,80,1.020,0,1,0,121,36,1.2,15.4,44,7800,5.2,1
...
```

**Important**: The target column should contain:
- `1` for patients with kidney stones
- `0` for patients without kidney stones

## Quick Start

### Step 1: Setup Configuration

First, configure your Watson ML credentials:

```bash
# Run setup to create config.json
python setup.py

# Edit config.json with your:
# - IBM Cloud API Key
# - Watson ML Deployment URL (from your deployed model)
```

### Step 2: Prepare Dataset (Optional)

If you want to train a new model, prepare your dataset:

```bash
# Use the simple dataset preparation (no pandas required)
python simple_prepare_dataset.py
```

### Step 3: Test Configuration

Test that your configuration works:

```bash
# Test the predictor connection and make a sample prediction
python test_predictor.py
```

### Step 4: Launch Web Application

Start the Flask web application:

```bash
# Start the Flask web application
python run_webapp.py

# Or with custom options
python run_webapp.py --port 8000 --debug
```

The web application will be available at `http://localhost:5000`

**Note:** The web app uses direct API calls to your deployed Watson ML model, so no additional training step is required if you already have a deployed model.

### Step 5: Use the Web Interface

1. Open your browser and go to `http://localhost:5000`
2. Fill in the urine analysis parameters
3. Click "Predict Kidney Stone Risk"
4. View the prediction results with confidence levels

## Web Application Features

### 🎯 Prediction Interface
- **User-friendly form** for inputting medical parameters
- **Real-time validation** of input data
- **Sample data buttons** for testing
- **Responsive design** that works on all devices

### 📊 Results Display
- **Clear risk assessment** (High Risk / Low Risk)
- **Confidence percentage** for prediction certainty
- **Visual progress bars** for easy interpretation
- **Input parameter summary** for reference

### 🔧 Additional Features
- **About page** with medical information
- **Data information** page explaining the dataset
- **API endpoints** for programmatic access
- **Health check** endpoint for monitoring
- **Error handling** with user-friendly messages

### Option 2: Manual Step-by-Step Process

#### Step 1: Prepare Your Data

```bash
# Option A: Use the data preparation script
python data_preparation.py

# Option B: Prepare data manually and save as kidney_stone_data.csv
```

#### Step 2: Run the AutoML Experiment

```bash
python watson_automl_kidney_predictor.py
```

The program will:
- Authenticate with IBM Watson Studio
- Upload your training data
- Run AutoML experiment to find the best model
- Display results and metrics
- Deploy the best model for predictions

### Using the Prediction API

Once the model is deployed, you can use it to make predictions:

```python
from watson_automl_kidney_predictor import WatsonKidneyStonePredictor

# Initialize predictor
predictor = WatsonKidneyStonePredictor()

# Authenticate
predictor.authenticate()

# Make prediction for new patient data
patient_data = {
    "input_data": [{
        "fields": ["age", "sex", "blood_pressure", "cholesterol", "sugar", "albumin", "blood_urea", "serum_creatinine", "hemoglobin", "packed_cell_volume", "white_blood_cell_count", "red_blood_cell_count"],
        "values": [[48, 1, 80, 1.020, 0, 1, 0, 121, 36, 1.2, 15.4, 44]]
    }]
}

prediction = predictor.predict(deployment_id, patient_data)
print(prediction)
```

## Program Components

### Main Classes

- **`WatsonKidneyStonePredictor`**: Main class handling all AutoML operations
  - `authenticate()`: Connect to IBM Watson Studio
  - `setup_experiment()`: Configure AutoML experiment
  - `upload_training_data()`: Upload CSV data to Watson Studio
  - `run_experiment()`: Execute AutoML training
  - `get_experiment_results()`: Retrieve training metrics
  - `deploy_model()`: Deploy trained model
  - `predict()`: Make predictions with deployed model

### Configuration Options

The `config.json` file supports various settings:

- **API Settings**: IBM Cloud credentials and service URLs
- **Experiment Settings**: Runtime limits, prediction type, train/test split
- **Model Settings**: Number of estimators, algorithms to include

## Expected Data Format

### Required Columns for Kidney Stone Prediction

Your CSV file should include these medical features:

| Column | Description | Type |
|--------|-------------|------|
| age | Patient age in years | numeric |
| sex | Gender (0=female, 1=male) | categorical |
| blood_pressure | Blood pressure measurement | numeric |
| cholesterol | Cholesterol level | numeric |
| sugar | Sugar/glucose level | numeric |
| albumin | Albumin level | numeric |
| blood_urea | Blood urea level | numeric |
| serum_creatinine | Serum creatinine level | numeric |
| hemoglobin | Hemoglobin level | numeric |
| packed_cell_volume | Packed cell volume | numeric |
| white_blood_cell_count | WBC count | numeric |
| red_blood_cell_count | RBC count | numeric |
| target | Kidney stone presence (0=no, 1=yes) | binary |

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Verify API key is correct and not expired
   - Check if Watson Studio service is active
   - Ensure correct region URL is used

2. **Project Not Found**
   - Verify project ID in config.json
   - Check if project exists in Watson Studio
   - Ensure you have access to the project

3. **Data Upload Failed**
   - Check CSV file format and encoding
   - Verify all required columns are present
   - Ensure target column contains only 0/1 values

4. **Experiment Timeout**
   - Increase max_runtime_seconds in config
   - Check Watson Studio resource availability
   - Try with smaller dataset first

### Logs

Check the `watson_automl.log` file for detailed error messages and debugging information.

### Support

For IBM Watson Studio specific issues:
- [Watson Studio Documentation](https://cloud.ibm.com/docs/watson-studio)
- [AutoML Service Documentation](https://cloud.ibm.com/docs/machine-learning)

## License

This project is provided as-is for educational and research purposes.