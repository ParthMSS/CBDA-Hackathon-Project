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
│── engine/
│     ├── data_loader.py       # CSV ingestion
│     ├── rule_engine.py       # Rule evaluation logic
│     ├── alert_engine.py      # Breach / Near breach classification
│     ├── llm_explainer.py     # OpenRouter API → explanation
│     ├── scheduler.py         # Daily scheduler
│── config/
│     ├── rules.yaml           # Configurable rules
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
