import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load user progress dataset
df = pd.read_csv("ml/dataset/user_progress.csv")

# Encode labels
encoder = LabelEncoder()
df['Recommended'] = encoder.fit_transform(df['Recommended'])

# Features and target
X = df[['Solved_Count', 'Easy_Solved', 'Medium_Solved',
        'Hard_Solved', 'Accuracy']]

y = df['Recommended']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# User input
solved = int(input("Solved Count: "))
easy = int(input("Easy Solved: "))
medium = int(input("Medium Solved: "))
hard = int(input("Hard Solved: "))
acc = int(input("Accuracy: "))

# Input dataframe
input_data = pd.DataFrame(
    [[solved, easy, medium, hard, acc]],
    columns=[
        'Solved_Count',
        'Easy_Solved',
        'Medium_Solved',
        'Hard_Solved',
        'Accuracy'
    ]
)

# Prediction
prediction = model.predict(input_data)

# Confidence
probabilities = model.predict_proba(input_data)
confidence = max(probabilities[0]) * 100

# Decode recommendation
recommended = encoder.inverse_transform(prediction)[0]

print("\nRecommended Next Difficulty:", recommended)
print(f"Confidence: {confidence:.2f}%")
print("Model Accuracy:", accuracy)

# Load LeetCode problems
problems_df = pd.read_csv("ml/dataset/leetcode_problems.csv")

# Filter recommended problems
recommended_problems = problems_df[
    problems_df['Difficulty'] == recommended
]

print("\nSuggested Problems:\n")

# Show problems
for index, row in recommended_problems.iterrows():
    print(f"- {row['Problem']} ({row['Topic']})")