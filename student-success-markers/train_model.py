import pandas as pd
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

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

# Connect and load data
engine = create_engine(get_database_url())
df = pd.read_sql('SELECT * FROM mart_student_risk', engine)

print(f"Shape: {df.shape}")
print(f"\nAt-risk distribution:\n{df['at_risk'].value_counts()}")

# Encode categorical columns
cat_cols = df.select_dtypes(include='object').columns
le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col].astype(str))

# Features and target
# Features and target
drop_cols = [
    'at_risk', 
    'student_id',
    'final_grade',
    'grade_period_1', 
    'grade_period_2',
    'avg_grade',
    'grade_trend_p1_p2',
    'grade_trend_p2_final',
    'grade_trajectory'
]

X = df.drop(columns=drop_cols)
y = df['at_risk']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Logistic Regression
lr = LogisticRegression(max_iter=1000, class_weight = "balanced")
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
print("\n--- Logistic Regression ---")
print(classification_report(y_test, lr_preds))
print(f"ROC-AUC: {roc_auc_score(y_test, lr.predict_proba(X_test)[:,1]):.3f}")

# Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight = "balanced")
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
print("\n--- Random Forest ---")
print(classification_report(y_test, rf_preds))
print(f"ROC-AUC: {roc_auc_score(y_test, rf.predict_proba(X_test)[:,1]):.3f}")

from xgboost import XGBClassifier

xgb = XGBClassifier(n_estimators=100, random_state=42, scale_pos_weight=2, eval_metric='logloss')
xgb.fit(X_train, y_train)
xgb_preds = xgb.predict(X_test)
print("\n--- XGBoost ---")
print(classification_report(y_test, xgb_preds))
print(f"ROC-AUC: {roc_auc_score(y_test, xgb.predict_proba(X_test)[:,1]):.3f}")

import shap
import matplotlib.pyplot as plt

# SHAP explainability on Logistic Regression
explainer = shap.LinearExplainer(lr, X_train)
shap_values = explainer(X_test)

# Summary plot - shows most important features overall
shap.summary_plot(shap_values, X_test, feature_names=X.columns.tolist(), show=False)
plt.title("Feature Importance - Student Risk Prediction")
plt.tight_layout()
plt.savefig("shap_summary.png", dpi=150, bbox_inches='tight')
plt.close()
print("SHAP summary plot saved as shap_summary.png")

# Bar plot - cleaner version for portfolio
shap.summary_plot(shap_values, X_test, feature_names=X.columns.tolist(), plot_type="bar", show=False)
plt.title("Mean Feature Impact on At-Risk Prediction")
plt.tight_layout()
plt.savefig("shap_bar.png", dpi=150, bbox_inches='tight')
plt.close()
print("SHAP bar plot saved as shap_bar.png")