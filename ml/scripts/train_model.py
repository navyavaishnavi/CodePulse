import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("ml/dataset/problems.csv")

# Encode labels
encoder = LabelEncoder()
df['Difficulty'] = encoder.fit_transform(df['Difficulty'])

# Features and target
X = df[['Problem_Length', 'Acceptance', 'Tags_Count']]
y = df['Difficulty']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "ml/models/difficulty_model.pkl")

# Predict on test set
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

# User input
length = int(input("Enter Problem Length: "))
acceptance = int(input("Enter Acceptance Rate: "))
tags = int(input("Enter Tags Count: "))

# Create input dataframe
input_data = pd.DataFrame(
    [[length, acceptance, tags]],
    columns=['Problem_Length', 'Acceptance', 'Tags_Count']
)

# Prediction
prediction = model.predict(input_data)

# Prediction probabilities
probabilities = model.predict_proba(input_data)

# Confidence score
confidence = max(probabilities[0]) * 100

# Convert prediction back to label
predicted_label = encoder.inverse_transform(prediction)

print("Predicted Difficulty:", predicted_label[0])
print(f"Confidence: {confidence:.2f}%")
print("Accuracy:", accuracy)

print("Model saved successfully!")