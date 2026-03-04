import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_dotenv() -> None:
    try:
        __import__("dotenv").load_dotenv()
    except Exception:
        return None


def get_database_url() -> str:
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    host = os.getenv("PGHOST", "localhost")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE", "UCI_Student_Info")
    user = os.getenv("PGUSER", "postgres")
    password = quote_plus(os.getenv("PGPASSWORD", ""))
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

st.title("Student At-Risk Predictor")
st.markdown("Enter a student's information to predict whether they are at risk of academic failure.")

@st.cache_resource
def load_model():
    engine = create_engine(get_database_url())
    df = pd.read_sql('SELECT * FROM mart_student_risk', engine)

    drop_cols = [
        'at_risk', 'student_id', 'final_grade', 'grade_period_1',
        'grade_period_2', 'avg_grade', 'grade_trend_p1_p2',
        'grade_trend_p2_final', 'grade_trajectory'
    ]

    cat_cols = df.select_dtypes(include='object').columns
    le = LabelEncoder()
    for col in cat_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop(columns=drop_cols)
    y = df['at_risk']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000, class_weight='balanced')
    model.fit(X_train, y_train)

    return model, X_train, X.columns.tolist()

# Build UI first
col1, col2, col3 = st.columns(3)

with col1:
    age = st.slider("Age", 15, 22, 17)
    study_time = st.selectbox("Study Time (hrs/week)", [1, 2, 3, 4], index=1)
    past_failures = st.selectbox("Past Course Failures", [0, 1, 2, 3])
    absences = st.slider("Absences", 0, 30, 5)

with col2:
    goout = st.slider("Go Out Frequency (1-5)", 1, 5, 3)
    weekday_alcohol = st.slider("Weekday Alcohol (1-5)", 1, 5, 1)
    weekend_alcohol = st.slider("Weekend Alcohol (1-5)", 1, 5, 2)
    health = st.slider("Health (1-5)", 1, 5, 3)

with col3:
    family_relationship = st.slider("Family Relationship (1-5)", 1, 5, 3)
    mother_education = st.selectbox("Mother Education (0-4)", [0, 1, 2, 3, 4], index=2)
    father_education = st.selectbox("Father Education (0-4)", [0, 1, 2, 3, 4], index=2)
    support_score = st.slider("Support Score (0-3)", 0, 3, 1)

# Load model after UI renders
with st.spinner("Loading model..."):
    model, X_train, feature_names = load_model()

st.success("Model ready!")

# Derived features
high_absences = 1 if absences > 10 else 0
total_alcohol_score = weekday_alcohol + weekend_alcohol
social_risk_score = goout + weekday_alcohol + weekend_alcohol
has_prior_failures = 1 if past_failures > 0 else 0

input_data = pd.DataFrame([{
    'age': age,
    'mother_education': mother_education,
    'father_education': father_education,
    'travel_time': 1,
    'study_time': study_time,
    'past_failures': past_failures,
    'family_relationship': family_relationship,
    'freetime': 3,
    'goout': goout,
    'weekday_alcohol': weekday_alcohol,
    'weekend_alcohol': weekend_alcohol,
    'health': health,
    'absences': absences,
    'social_risk_score': social_risk_score,
    'total_alcohol_score': total_alcohol_score,
    'support_score': support_score,
    'high_absences': high_absences,
    'has_prior_failures': has_prior_failures
}])

for col in feature_names:
    if col not in input_data.columns:
        input_data[col] = 0
input_data = input_data[feature_names]

if st.button("Predict Risk"):
    prob = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    st.markdown("---")
    if prediction == 1:
        st.error(f"At-Risk — Risk Probability: {prob:.1%}")
    else:
        st.success(f"On Track — Risk Probability: {prob:.1%}")

    st.subheader("Why this prediction?")
    explainer = shap.LinearExplainer(model, X_train)
    shap_values = explainer(input_data)

    fig, ax = plt.subplots()
    shap.waterfall_plot(shap_values[0], show=False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()