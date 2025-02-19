from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Import and load data
crop = pd.read_csv('Crop_recommendation.csv')

# Create a mapping for crop labels
crop_dict = {
    'rice': 1, 'maize': 2, 'jute': 3, 'cotton': 4, 'coconut': 5,
    'papaya': 6, 'orange': 7, 'apple': 8, 'muskmelon': 9, 'watermelon': 10,
    'grapes': 11, 'mango': 12, 'banana': 13, 'pomegranate': 14,
    'lentil': 15, 'blackgram': 16, 'mungbean': 17, 'mothbeans': 18,
    'pigeonpeas': 19, 'kidneybeans': 20, 'chickpea': 21, 'coffee': 22
}

# Map the 'label' column to numerical values
crop['label_num'] = crop['label'].map(crop_dict)

# Features (X) and label (y)
# Exclude 'label' and 'label_num' from the features
X = crop.drop(columns=['label', 'label_num'])
y = crop['label_num']  # Use 'label_num' as the target

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train the RandomForest model
rdf = RandomForestClassifier()
rdf.fit(X_train_scaled, y_train)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_crop():
    # Get the input data from the request
    data = request.json
    # Extract the feature values from the request and reshape for scaling
    input_values = np.array([[data['N'], data['P'], data['K'], data['temperature'], data['humidity'], data['ph'], data['rainfall']]])
    
    # Scale the input values using the same scaler as training
    input_values_scaled = scaler.transform(input_values)
    
    # Make a prediction using the trained model
    prediction = rdf.predict(input_values_scaled)
    
    # Map the numerical prediction back to the crop name
    prediction_label = list(crop_dict.keys())[list(crop_dict.values()).index(prediction[0])]
    
    # Return the prediction as a JSON response
    return jsonify({'predicted_crop': prediction_label})

if __name__ == '__main__':
    app.run(debug=True)
