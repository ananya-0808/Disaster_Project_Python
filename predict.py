import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from io import StringIO


url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "csv", 
    "starttime": "2025-01-01",
    "endtime": "2025-02-16", 
    "minmagnitude": 5.0,
    "maxlatitude": 90.0, 
    "minlatitude": -90.0, 
    "maxlongitude": 180.0,
    "minlongitude": -180.0 
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = pd.read_csv(StringIO(response.text)) 
    print("Fetched data successfully.")
    print(f"Fetched {len(data)} earthquake records.")
    print("Column names:", data.columns)
    print("First few rows of the data:\n", data.head())
else:
    print("Error fetching data:", response.status_code)


if 'mag' in data.columns:
    data = data.dropna()  
    features = ['latitude', 'longitude', 'depth'] 
    target = 'mag' 
    
    X = data[features]
    y = data[target]

 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    print(f"Training data shape: X_train: {X_train.shape}, y_train: {y_train.shape}")

    model_rf = RandomForestRegressor(random_state=42)
    model_rf.fit(X_train, y_train)

    print(f"Random Forest model fitted.")

    predictions_rf = model_rf.predict(X_test)

    print("Making prediction for new data...")
    try:
        new_data = [[34.0522, -118.2437, 10]]
        
        predicted_magnitude_rf = model_rf.predict(new_data)
        print(f"Predicted Magnitude (Random Forest) for the new earthquake: {predicted_magnitude_rf[0]}")

    except Exception as e:
        print(f"Error during prediction: {e}")

    plt.scatter(y_test, predictions_rf)
    plt.xlabel('Actual Magnitude')
    plt.ylabel('Predicted Magnitude')
    plt.title('Earthquake Magnitude Prediction - Random Forest')
    plt.show()
    
else:
    print("'magnitude' column not found in the dataset.")
