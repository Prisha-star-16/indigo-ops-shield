# ✈️ IndiGo Ops Shield: Crisis Prediction Engine

A Data Science & Engineering project analyzing the IndiGo Airlines operational crisis (2025). This solution predicts flight cancellations based on pilot fatigue (FDTL) and crew shortages.

## 🚀 Features
* **Machine Learning:** Random Forest model to predict cancellation risk.
* **FastAPI Backend:** Production-ready API for real-time risk scoring.
* **Streamlit Dashboard:** Dark-mode Command Center for operations teams.

## 🛠️ Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## ▶️ How to Open and Run the Project (Windows CMD)

### Step 1: Open Command Prompt
- Press **Win + R** → type `cmd` → press **Enter**

### Step 2: Navigate to Project Folder
```cmd
cd C:\Users\<your-username>\IndigoProject
```
Verify files:
```cmd
dir
```
You should see `dashboard.py`, `main.py`, and `requirements.txt`

### Step 3: Run the Streamlit Dashboard
```cmd
python -m streamlit run dashboard.py
```
- Browser opens automatically at: `http://localhost:8501`
- Launches the **IndiGo Ops Command Center**

### Step 4 (Optional): Run the FastAPI Backend
```cmd
uvicorn main:app --reload
```
Open API docs:
```
http://127.0.0.1:8000/docs
```

### ❗ Common Errors & Fixes
- **'streamlit' not recognized** → Use:
```cmd
python -m streamlit run dashboard.py
```
- **Python not recognized** → Install Python and enable **Add Python to PATH**

---

## ✅ Conclusion
This project demonstrates an end-to-end ML-powered operational decision system for airline crisis management.

