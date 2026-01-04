import streamlit as st
from engine.data_loader import load_data_from_investment
from engine.rule_engine import load_rules, load_investments
from main import check_breached_covenant
import pandas as pd

st.set_page_config(page_title="Covenant Breach Detection Agent", layout="wide")

rules = load_rules()
investments = load_investments()

def investments_dashboard():
    st.subheader("Investments Overview")

    col1, col2 = st.columns(2)

    # ----------------------
    # SELECT INVESTMENT
    # ----------------------
    with col1:
        option = st.selectbox(
            "Select an investment to view details:",
            [f"{inv['id']} - {inv['name']}" for inv in investments]
        )
        inv_id = int(option.split(" - ")[0])
        investment = next((inv for inv in investments if inv['id'] == inv_id), None)

    if not investment:
        st.warning("No investment selected or investment not found.")
        return

    # ----------------------
    # SELECT METRIC TO CHART
    # ----------------------
    data = load_data_from_investment(investment)

    with col2:
        selected_metric = st.selectbox(
            "Select a factor to visualize:",
            [
                "Debt-to-EBITDA","Debt-to-Equity","Net-Debt-to-Total-Cap",
                "Senior-Debt-to-EBITDA","Interest-Coverage","DSCR",
                "Fixed-Charge-Coverage","Current-Ratio","Quick-Ratio",
                "Cash-Balance-MM","EBITDA-MM","EBITDA-Margin","ROA","ROE"
            ]
        )

    # ----------------------
    # SHOW CHART 
    # ----------------------
    st.line_chart(data, x="Period", y=selected_metric)

    # ----------------------
    # IMPROVED INVESTMENT INFO DISPLAY
    # ----------------------
    st.markdown("### 📘 Investment Summary")

    # Summary top cards
    card_col1, card_col2, card_col3 = st.columns(3)
    with card_col1:
        st.metric("💰 Amount Invested", f"${investment['amount_invested']:,}")
    with card_col2:
        st.metric("📈 Current Value", f"${investment['current_value']:,}")
    with card_col3:
        st.metric("📅 Date Invested", investment["date_invested"])

    # Divider
    st.markdown("---")

    st.markdown("### 🧾 Investment Profile")

    # Organize additional details in columns
    details = investment.get("investment_details", {})

    colA, colB = st.columns(2)

    with colA:
        st.write(f"**Industry:** {details.get('industry', 'N/A')}")
        st.write(f"**Loan Type:** {details.get('loan_type', 'N/A')}")
        st.write(f"**Interest Rate:** {details.get('interest_rate', 'N/A') * 100:.2f}%")
        st.write(f"**Maturity Date:** {details.get('maturity_date', 'N/A')}")

    with colB:
        st.write(f"**Loan Term:** {details.get('loan_term_years', 'N/A')} years")
        st.write(f"**Collateral:** {details.get('collateral', 'N/A')}")
        st.write(f"**Credit Rating:** {details.get('credit_rating', 'N/A')}")
        st.write(f"**Risk Profile:** {details.get('risk_profile', 'N/A')}")

    st.markdown("---")

    # st.markdown("### ⚖️ Covenant Status")
    # st.success(details.get("covenant_status", "Unknown"))

SEVERITY_COLORS = {
    "low": "#4CAF50",
    "medium": "#FFC107",
    "high": "#F44336"
}

def severity_badge(level):
    color = SEVERITY_COLORS.get(level, "#888")
    return f"""
<span style="
    background:{color};
    color:white;
    padding:4px 10px;
    border-radius:8px;
    font-size:12px;
    font-weight:600;">
    {level.upper()}
</span>
    """

def render_rule(rule):
    st.markdown(f"### {rule['name']} {severity_badge(rule['severity'])}", unsafe_allow_html=True)

    st.markdown(f"**Covenant Type:** `{rule['covenant_type'].upper()}`")
    st.markdown(f"**Metric:** `{rule['metric']}`")

    # Summary table
    st.markdown("#### Key Values")
    st.table(pd.DataFrame({
        "Ideal": [rule["ideal_value"]],
        "Near Breach": [rule["near_breach_value"]],
        "Threshold": [rule["threshold_value"]],
    }))

    st.markdown("#### Description")
    st.markdown(rule["description"])

def config_rules_dashboard():
    global rules
    col1, col2 = st.columns(2)

    mid = len(rules) // 2
    rules_col1 = rules[:mid]
    rules_col2 = rules[mid:]

    with col1:
        for rule in rules_col1:
            with st.expander(rule["name"],expanded=True):
                render_rule(rule)

    with col2:
        for rule in rules_col2:
            with st.expander(rule["name"],expanded=True):
                render_rule(rule)

def breach_detection_dashboard():
    st.title("Covenant Monitoring Report")

    if st.button("Run Covenant Monitoring Pipeline"):
        report = check_breached_covenant(investments, rules)
        st.session_state["report"] = report

    if "report" not in st.session_state:
        return

    report = st.session_state["report"]

    st.subheader("Portfolio Summary")
    st.metric("Total Investments", report["summary"]["total_investments"])
    st.metric("Total Breaches", report["summary"]["total_breaches"])
    st.metric("Total Near Breaches", report["summary"]["total_near_breaches"])
    st.metric("Total Ideal Ratios", report["summary"]["total_ideal"])

    st.subheader("Investment-Level Results")

    # Build UI table
    for inv in report["investments"]:
        cols = st.columns([3,2,2,2,2])

        cols[0].write(f"### {inv['name']}")
        cols[1].metric("Breaches", inv["breaches"])
        cols[2].metric("Near Breach", inv["near_breaches"])
        cols[3].metric("Ideal", inv["ideal"])

        if cols[4].button("View Details", key=f"btn_{inv['id']}"):
            st.session_state["selected_investment"] = inv

    # Popup modal
    if "selected_investment" in st.session_state:
        inv = st.session_state["selected_investment"]
        st.markdown("---")
        st.subheader(f"Detailed Covenant Data — {inv['name']}")

        for alert in inv["alerts"]:
            with st.expander(f"{alert['metric']} → {alert['severity'].upper()}"):
                st.write("**Current Value:**", alert["current_value"])
                st.write("**Limit:**", alert["limit"])
                st.write("**Trend:**", alert["trend"])
                st.write("**Rate of Change:**", alert["rate_of_change"])
                st.write("**Confidence:**", alert["trend_confidence"])

                # Render explanation if exists
                if "explanation" in alert:
                    st.markdown("### 📘 LLM Explanation")
                    st.info(alert["explanation"])

                st.write("### Rule Evaluation Details")
                st.json(alert["rule_result"])
def breach_detection_dashboard():
    st.title("Covenant Monitoring Report")

    if st.button("Run Covenant Monitoring Pipeline"):
        report = check_breached_covenant(investments, rules)
        st.session_state["report"] = report

    if "report" not in st.session_state:
        return

    report = st.session_state["report"]

    st.subheader("Portfolio Summary")
    st.metric("Total Investments", report["summary"]["total_investments"])
    st.metric("Total Breaches", report["summary"]["total_breaches"])
    st.metric("Total Near Breaches", report["summary"]["total_near_breaches"])
    st.metric("Total Ideal Ratios", report["summary"]["total_ideal"])

    st.subheader("Investment-Level Results")

    # Build UI table
    for inv in report["investments"]:
        cols = st.columns([3,2,2,2,2])

        cols[0].write(f"### {inv['name']}")
        cols[1].metric("Breaches", inv["breaches"])
        cols[2].metric("Near Breach", inv["near_breaches"])
        cols[3].metric("Ideal", inv["ideal"])

        if cols[4].button("View Details", key=f"btn_{inv['id']}"):
            st.session_state["selected_investment"] = inv

    # Popup modal
    if "selected_investment" in st.session_state:
        inv = st.session_state["selected_investment"]
        st.markdown("---")
        st.subheader(f"Detailed Covenant Data — {inv['name']}")

        for alert in inv["alerts"]:
            with st.expander(f"{alert['metric']} → {alert['severity'].upper()}"):
                st.write("**Current Value:**", alert["current_value"])
                st.write("**Limit:**", alert["limit"])
                st.write("**Trend:**", alert["trend"])
                st.write("**Rate of Change:**", alert["rate_of_change"])
                st.write("**Confidence:**", alert["trend_confidence"])

                # Render explanation if exists
                if "explanation" in alert:
                    st.markdown("### 📘 LLM Explanation")
                    st.info(alert["explanation"])

                st.write("### Rule Evaluation Details")
                st.json(alert["rule_result"])

import os
import json
HISTORY_DIR = "history"

def load_history_files():
    if not os.path.exists(HISTORY_DIR):
        return []
    return sorted(os.listdir(HISTORY_DIR), reverse=True)

def load_report(path):
    with open(path, "r") as f:
        return json.load(f)

def history_viewer():
    st.title("📜 Covenant Monitoring — History Viewer")

    files = load_history_files()

    if not files:
        st.info("No historical reports found.")
        return

    selected = st.selectbox("Select a report:", files)

    if selected:
        report_path = os.path.join(HISTORY_DIR, selected)
        report = load_report(report_path)

        st.success(f"Loaded report: {selected}")
        # st.write(f"**Generated At:** {report['generated_at']}")

        # Summary
        st.subheader("Portfolio Summary")
        colA, colB, colC, colD = st.columns(4)
        colA.metric("Total Investments", report["summary"]["total_investments"])
        colB.metric("Total Breaches", report["summary"]["total_breaches"])
        colC.metric("Total Near Breaches", report["summary"]["total_near_breaches"])
        colD.metric("Total Ideal", report["summary"]["total_ideal"])

        st.subheader("Investment-Level Results")

        for inv in report["investments"]:
            with st.expander(f"{inv['name']} — Breaches: {inv['breaches']}"):
                st.json(inv)
 

pg = st.navigation([investments_dashboard, config_rules_dashboard, breach_detection_dashboard,history_viewer],expanded=True)
pg.run()

