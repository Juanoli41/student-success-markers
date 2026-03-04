# Student Success Markers

End-to-end analytics + ML project to identify students at academic risk using the UCI Student Performance dataset.  
Pipeline includes data ingestion, dbt transformations, model training, and a Streamlit app for interactive predictions.

---

## 1) Problem Statement

Educational teams need early warning signals to support students before final outcomes are locked in.  
This project predicts whether a student is **at risk** based on demographics, attendance, study behavior, and prior academic performance.

### Target Definition
- `at_risk = 1` if final grade `G3 < 10`
- `at_risk = 0` otherwise

---

## 2) Project Goals

- Build a reproducible analytics pipeline from raw CSV to modeled features
- Train baseline and tree-based classifiers for risk prediction
- Provide model interpretability using SHAP
- Deliver an easy-to-use Streamlit interface for stakeholders

---

## 3) Architecture

```text
student-mat.csv
   ↓
load_data.py (Python ingestion)
   ↓
PostgreSQL (raw_students)
   ↓
dbt models
  - stg_students
  - int_student_features
  - mart_student_risk
   ↓
train_model.py (ML training + evaluation + SHAP)
   ↓
app.py (Streamlit prediction UI)
```

### Data Layer
- **Source**: UCI Student Performance (`student-mat.csv`)
- **Database**: PostgreSQL
- **Transformation**: dbt (`DBT/UCI_Student_Info`)

### Modeling Layer
- Logistic Regression
- Random Forest
- XGBoost (if installed/configured)

### App Layer
- Streamlit app for interactive risk prediction and explainability

---

## 4) Repository Structure

```text
.
├─ app.py
├─ load_data.py
├─ train_model.py
├─ student-mat.csv
├─ README.md
├─ .env.example
└─ DBT/
   └─ UCI_Student_Info/
      ├─ models/
      │  ├─ sources.yml
      │  └─ example/
      │     ├─ stg_students.sql
      │     ├─ int_student_features.sql
      │     └─ mart_student_risk.sql
      └─ profiles.template.yml
```

---

## 5) Setup

## Prerequisites
- Python 3.10+ recommended
- PostgreSQL running locally or accessible remotely
- dbt Core + dbt-postgres
- Windows PowerShell (commands below)

## Install dependencies
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If Streamlit is missing:
```powershell
python -m pip install streamlit
```

---

## 6) Configuration

Create `.env` from `.env.example`:

```dotenv
PGHOST=localhost
PGPORT=5432
PGDATABASE=UCI_Student_Info
PGUSER=your_username
PGPASSWORD=your_password
DBT_TARGET=dev
```

> Do **not** commit `.env` or private dbt profile files.

---

## 7) Run the Pipeline

## Step 1: Load raw data into Postgres
```powershell
python load_data.py
```

## Step 2: Build dbt models
```powershell
cd .\DBT\UCI_Student_Info
dbt run
dbt test
cd ..\..
```

## Step 3: Train models + generate explainability artifacts
```powershell
python train_model.py
```

## Step 4: Launch Streamlit app
```powershell
python -m streamlit run app.py
```

---

## 8) Feature Engineering (dbt)

Key engineered features in `int_student_features.sql` include:
- grade trend deltas (`p1→p2`, `p2→final`)
- average grade features
- attendance risk (`high_absences`)
- prior failure indicator (`has_prior_failures`)
- social/behavioral score proxies
- support score proxies

These are surfaced in `mart_student_risk` for model consumption.

---

## 9) Evaluation and Findings

Current implementation supports:
- Classification metrics (precision/recall/F1)
- ROC-AUC comparison across models
- SHAP global plots (`shap_summary.png`, `shap_bar.png`)
- Local explanation flow in Streamlit app

### Key Findings (implementation-level)
1. Academic trajectory and prior failures are strong risk signals.
2. Attendance and support-related features improve separability.
3. Explainability artifacts make model behavior inspectable for non-technical users.
4. End-to-end reproducibility is achieved through Python + dbt orchestration.

---

## 10) Security and Public-Repo Hygiene

Before publishing:
- Ensure secrets are environment-based only
- Keep `.env`, local `profiles.yml`, and private keys ignored
- Validate with:
```powershell
git grep -nEi "password|secret|token|api[_-]?key|C:\\Users\\|OneDrive"
```
No output is expected.

---

## 11) Troubleshooting

## `streamlit` not found
```powershell
python -m pip install streamlit
python -m streamlit run app.py
```

## dbt profile issues
- Use local `profiles.yml` (untracked) or `profiles.template.yml` as a guide
- Confirm env vars are set in `.env`

## PostgreSQL connection errors
- Verify host/port/db/user/password
- Confirm database accepts connections from your machine

---

## 12) Future Improvements

- Add model registry + versioning
- Add CI for dbt tests + unit tests
- Add threshold tuning and cost-sensitive metrics
- Add feature drift and data quality monitoring
- Add containerized deployment (Docker)

---

## 13) License

Add your preferred license (MIT/Apache-2.0/etc.) before public release.