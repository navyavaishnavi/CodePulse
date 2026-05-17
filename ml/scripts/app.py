import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI-Powered DSA Mentor",
    page_icon="🚀",
    layout="wide"
)

# =========================
# DARK THEME CSS
# =========================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

html, body, [class*="css"] {
    color: white;
    background-color: #0E1117;
}

.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.stNumberInput label {
    color: white !important;
}

.stTextInput label {
    color: white !important;
}

h1, h2, h3 {
    color: #ff4b4b !important;
}

[data-testid="stSidebar"] {
    background-color: #161A23;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("🚀 AI-Powered DSA Mentor")

st.write(
    "Predict coding difficulty and get personalized recommendations."
)

# =========================
# LOGIN SYSTEM
# =========================

st.sidebar.title("🔐 Login System")

username = st.sidebar.text_input(
    "Username"
)

password = st.sidebar.text_input(
    "Password",
    type="password"
)

login_btn = st.sidebar.button("Login")

signup_btn = st.sidebar.button("Signup")

users_df = pd.read_csv(
    "ml/dataset/users.csv"
)

if signup_btn:

    new_user = pd.DataFrame(
        [[username, password]],
        columns=["Username", "Password"]
    )

    users_df = pd.concat(
        [users_df, new_user],
        ignore_index=True
    )

    users_df.to_csv(
        "ml/dataset/users.csv",
        index=False
    )

    st.sidebar.success(
        "Account Created Successfully!"
    )

if login_btn:

    valid_user = users_df[
        (users_df["Username"] == username)
        &
        (users_df["Password"] == password)
    ]

    if not valid_user.empty:

        st.sidebar.success(
            f"Welcome {username} 🚀"
        )

    else:

        st.sidebar.error(
            "Invalid Username or Password"
        )

# =========================
# LOAD MODEL
# =========================

model = joblib.load("ml/models/difficulty_model.pkl")

# =========================
# DIFFICULTY PREDICTOR
# =========================

st.markdown("## 🧠 Problem Difficulty Predictor")

length = st.number_input("Problem Length", min_value=0)

acceptance = st.number_input(
    "Acceptance Rate",
    min_value=0
)

tags = st.number_input(
    "Tags Count",
    min_value=0
)

labels = ['Easy', 'Hard', 'Medium']

if st.button("Predict Difficulty"):

    input_data = pd.DataFrame(
        [[length, acceptance, tags]],
        columns=[
            'Problem_Length',
            'Acceptance',
            'Tags_Count'
        ]
    )

    prediction = model.predict(input_data)

    probabilities = model.predict_proba(
        input_data
    )[0]

    confidence = max(probabilities) * 100

    predicted_label = labels[prediction[0]]

    st.success(
        f"Predicted Difficulty: {predicted_label}"
    )

    st.info(
        f"Confidence: {confidence:.2f}%"
    )

    st.markdown(
        "### 📊 Probability Breakdown"
    )

    for i in range(len(labels)):

        st.write(
            f"{labels[i]}: {probabilities[i] * 100:.2f}%"
        )

        st.progress(
            float(probabilities[i])
        )

# =========================
# DATASET ANALYTICS
# =========================

st.markdown("## 📈 Dataset Analytics")

original_df = pd.read_csv(
    "ml/dataset/problems.csv"
)

difficulty_counts = original_df[
    'Difficulty'
].value_counts()

fig, ax = plt.subplots(
    figsize=(3.5, 3.5)
)

ax.pie(
    difficulty_counts.values,
    labels=difficulty_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    radius=0.75
)

ax.set_title(
    "Difficulty Distribution"
)

st.pyplot(fig)

# =========================
# LOAD PROBLEMS DATASET
# =========================

problems_df = pd.read_csv(
    "ml/dataset/leetcode_problems.csv"
)

# =========================
# TOPIC ANALYTICS
# =========================

st.markdown(
    "## 📚 Topic-wise Problem Analysis"
)

topic_counts = problems_df[
    'Topic'
].value_counts()

st.bar_chart(topic_counts)

# =========================
# RECOMMENDATION SYSTEM
# =========================

st.markdown(
    "## 🎯 Personalized Recommendations"
)

user_df = pd.read_csv(
    "ml/dataset/user_progress.csv"
)

encoder = LabelEncoder()

user_df['Recommended'] = encoder.fit_transform(
    user_df['Recommended']
)

X = user_df[
    [
        'Solved_Count',
        'Easy_Solved',
        'Medium_Solved',
        'Hard_Solved',
        'Accuracy'
    ]
]

y = user_df['Recommended']

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

recommend_model = LogisticRegression(
    max_iter=1000
)

recommend_model.fit(
    X_train,
    y_train
)

st.markdown(
    "### 📚 Enter Your Progress"
)

solved = st.number_input(
    "Solved Count",
    min_value=0,
    key="solved"
)

easy = st.number_input(
    "Easy Solved",
    min_value=0,
    key="easy"
)

medium = st.number_input(
    "Medium Solved",
    min_value=0,
    key="medium"
)

hard = st.number_input(
    "Hard Solved",
    min_value=0,
    key="hard"
)

acc = st.number_input(
    "Accuracy (%)",
    min_value=0,
    key="accuracy"
)

if st.button(
    "Get Recommendations"
):

    user_input = pd.DataFrame(
        [[
            solved,
            easy,
            medium,
            hard,
            acc
        ]],
        columns=[
            'Solved_Count',
            'Easy_Solved',
            'Medium_Solved',
            'Hard_Solved',
            'Accuracy'
        ]
    )

    prediction = recommend_model.predict(
        user_input
    )

    probabilities = recommend_model.predict_proba(
        user_input
    )

    confidence = max(
        probabilities[0]
    ) * 100

    recommended = encoder.inverse_transform(
        prediction
    )[0]

    st.success(
        f"Recommended Next Difficulty: {recommended}"
    )

    st.info(
        f"Confidence: {confidence:.2f}%"
    )

    recommended_problems = problems_df[
        problems_df['Difficulty']
        == recommended
    ]

    st.markdown(
        "### 💡 Suggested Problems"
    )

    for index, row in recommended_problems.iterrows():

        st.write(
            f"• {row['Problem']} ({row['Topic']})"
        )

# =========================
# SAVE USER PROGRESS
# =========================

if st.button("Save Progress"):

    new_data = pd.DataFrame(
        [[
            username,
            solved,
            easy,
            medium,
            hard,
            acc
        ]],
        columns=[
            "Username",
            "Solved",
            "Easy",
            "Medium",
            "Hard",
            "Accuracy"
        ]
    )

    existing_df = pd.read_csv(
        "ml/dataset/user_data.csv"
    )

    updated_df = pd.concat(
        [existing_df, new_data],
        ignore_index=True
    )

    updated_df.to_csv(
        "ml/dataset/user_data.csv",
        index=False
    )

    st.success(
        "Progress Saved Successfully!"
    )