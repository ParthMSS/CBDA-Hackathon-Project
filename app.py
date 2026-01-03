import streamlit as st
from engine.data_loader import load_data_from_investment
from engine.rule_engine import load_rules, load_investments, evaluate_rule
from engine.alert_engine import classify_alert
from engine.llm_explainer import generate_explanation
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
    st.subheader("Covenant Breach Detection")
    st.info("This section will display real-time breach detection results once implemented.")

pg = st.navigation([investments_dashboard, config_rules_dashboard, breach_detection_dashboard],expanded=True)
pg.run()
# if st.button("Run All Checks Now"):
#     st.subheader("Results")
#     for rule in rules:
#         df = load_data_from_rule(rule)
#         result = evaluate_rule(rule, df)
#         print(result)
#         # st.write(result)
#         status = classify_alert(result)

#         color = "🟢" if status == "OK" else "🟡" if status == "NEAR_BREACH" else "🔴"

#         st.write(f"{color} **{rule['id']}** → Status: **{status}**")
#         st.write(f"Current Value: {result['value']} | Limit: {result['limit']} | Operator: {result['operator']} | New Breach Value: {result['new_breach_value']}")

        # if status != "OK":
        #     # with st.spinner("Generating explanation using LLM..."):
        #     #     explanation = generate_explanation(result)
        #     st.info("explanation")
