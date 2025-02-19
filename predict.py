import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from io import StringIO

# Define the base URL for the USGS Earthquake API
url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Set up the parameters for the query
params = {
    "format": "csv",  # Output format (CSV in this case)
    "starttime": "2025-01-01",  # Start date for the data (example: January 1, 2025)
    "endtime": "2025-02-16",  # End date for the data (example: February 1, 2025)
    "minmagnitude": 5.0,  # Minimum magnitude (e.g., magnitude >= 5.0)
    "maxlatitude": 90.0,  # Maximum latitude (northernmost point on the globe)
    "minlatitude": -90.0,  # Minimum latitude (southernmost point on the globe)
    "maxlongitude": 180.0,  # Maximum longitude (easternmost point on the globe)
    "minlongitude": -180.0  # Minimum longitude (westernmost point on the globe)
}

# Send a GET request to the USGS API with the parameters
response = requests.get(url, params=params)

# Check if the request was successful (status code 200 means OK)
if response.status_code == 200:
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(StringIO(response.text))  # Use StringIO to parse CSV data
    # Print the column names and first few rows to debug
    print("Fetched data successfully.")
    print(f"Fetched {len(data)} earthquake records.")
    print("Column names:", data.columns)  # Check the actual column names
    print("First few rows of the data:\n", data.head())  # Preview the data
else:
    print("Error fetching data:", response.status_code)

# If the 'mag' column exists, proceed with preprocessing and training
if 'mag' in data.columns:
    # Data Preprocessing and Cleaning
    data = data.dropna()  # Remove rows with missing values

    # Feature Engineering: Select relevant features for prediction
    features = ['latitude', 'longitude', 'depth']  # Using latitude, longitude, and depth as features
    target = 'mag'  # We want to predict the magnitude of the earthquake

    # Assign features (X) and target (y)
    X = data[features]
    y = data[target]

    # Split the data into training and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)  # Removed fixed random_state

    # Check if there is enough data to train
    print(f"Training data shape: X_train: {X_train.shape}, y_train: {y_train.shape}")

    # --- Random Forest Regressor Model ---
    # Create and train the Random Forest Regressor model
    model_rf = RandomForestRegressor(random_state=42)
    model_rf.fit(X_train, y_train)

    # Print model details after training
    print(f"Random Forest model fitted.")

    # Evaluate the Random Forest model
    predictions_rf = model_rf.predict(X_test)

    print("Making prediction for new data...")
    try:
        new_data = [[34.0522, -118.2437, 10]]  # Example: lat, lon, depth (e.g., Los Angeles, CA)

        # Random Forest Prediction
        predicted_magnitude_rf = model_rf.predict(new_data)
        print(f"Predicted Magnitude (Random Forest) for the new earthquake: {predicted_magnitude_rf[0]}")

    except Exception as e:
        print(f"Error during prediction: {e}")

    # Plot the predicted vs actual values for Random Forest
    plt.scatter(y_test, predictions_rf)
    plt.xlabel('Actual Magnitude')
    plt.ylabel('Predicted Magnitude')
    plt.title('Earthquake Magnitude Prediction - Random Forest')
    plt.show()

    # --- Making Predictions for New Data ---
else:
    print("'magnitude' column not found in the dataset.")
