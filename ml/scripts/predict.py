import pandas as pd
import joblib

# Load saved model
model = joblib.load("ml/models/difficulty_model.pkl")

# User input
length = int(input("Enter Problem Length: "))
acceptance = int(input("Enter Acceptance Rate: "))
tags = int(input("Enter Tags Count: "))

# Create dataframe
input_data = pd.DataFrame(
    [[length, acceptance, tags]],
    columns=['Problem_Length', 'Acceptance', 'Tags_Count']
)

# Prediction
prediction = model.predict(input_data)

# Probability
probabilities = model.predict_proba(input_data)

# Confidence
confidence = max(probabilities[0]) * 100

# Difficulty labels
labels = ['Easy', 'Hard', 'Medium']

print("Predicted Difficulty:", labels[prediction[0]])
print(f"Confidence: {confidence:.2f}%")