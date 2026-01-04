Here is a **clean, complete, professional README.md** for your hackathon project.

---

# 🛡️ **CBDA – Covenant Breach Detection Agent**

An automated rule-checker that warns you *before* something breaks.

CBDA is a configurable, intelligent monitoring system that checks financial/operational metrics against user-defined rules and raises **near-breach** and **breach** alerts—with **LLM-powered explanations**.

Think of it like a **smoke alarm** for covenant violations.

---



# 📁 **Project Structure**

```
covenant-breach-agent/
│── app.py                     # Streamlit UI
│── main.py                    # Runs the pipeline
│── engine/
│     ├── alert.py             # Converts result into structured alert
│     ├── data_loader.py       # CSV ingestion
│     ├── rule_engine.py       # Rule evaluation logic
│     ├── alert_engine.py      # Breach / Near breach classification
│     ├── llm_explainer.py     # OpenRouter API → explanation
│     ├── scheduler.py         # Daily scheduler
│── config/
│     ├── rules.yaml           # Configurable rules
│     ├── investments.json     # Mocking a DB of investments
│── data/
│     ├── metrics.csv          # Example data source
│── requirements.txt
│── README.md
```

---

# 📦 **Requirements**

See `requirements.txt`

Key dependencies:

* **Python 3.10+**
* streamlit
* pandas
* pyyaml
* schedule
* requests

---

# 🔑 Environment Variables

Before running, set your **OpenRouter API key**:

```
export OPENROUTER_API_KEY="your-api-key-here"
```

On Windows (PowerShell):

```
setx OPENROUTER_API_KEY "your-api-key-here"
```

---

# 🛠️ **Setup Instructions**

Prerequisites:
- install python 3.10+

### 1️⃣ Create virtual environment (only once)

```
python -m venv .venv
```

### 2️⃣ Activate environment

**Windows:**

```
.venv\Scripts\activate
```

**Mac/Linux:**

```
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit dashboard

```
streamlit run app.py
```

---

## Features
### 1. 📊 Investment Dashboard

A comprehensive view of all investments in the system.
- Displays every investment along with its financial KPI factors (e.g., leverage ratios, liquidity ratios, returns, etc.).

- Allows users to select an investment and visualize its historical data using charts.

- Provides an intuitive way to explore performance trends, compare factors, and understand investment health.

### 2. ⚙️ Rule Configuration

Admin-style page to manage business rules applied to the dataset.

- Shows all covenant/risk rules stored in the database.

- These rules define thresholds, formulas, and logic for evaluating each investment.

- Users can modify or extend rules that influence covenant monitoring.

### 3. 🛑 Breach Detection Dashboard

Runs the entire covenant monitoring engine.

- Includes a “Run Covenant Monitoring Pipeline” button that triggers rule evaluation on all investments.

- The system computes breaches, near-breaches, and ideal metrics based on the rule engine.

- Generates a detailed, LLM-powered explanation for any alert or violation.

- Results are grouped by investment with a detailed drill-down view showing:

    - Breached rules

    - Near-breach indicators

    - Ideal/healthy metrics

    - Rule evaluation details & explanations

- Each generated report is saved automatically with a timestamp for future reference.

### 4. 🗂️ History Viewer

A full archive of all previously generated covenant-monitoring reports.

- Displays all JSON reports stored in the /history_reports/ directory.

- Users can click on any past report to view it inside the app.

- Provides a clean UI to explore older outputs including breaches, trends, and explanations.

- Enables auditability and comparison of past vs current performance.