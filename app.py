import streamlit as st
from engine.data_loader import load_data_from_rule
from engine.rule_engine import load_rules, evaluate_rule
from engine.alert_engine import classify_alert
from engine.llm_explainer import generate_explanation

st.set_page_config(page_title="Covenant Breach Detection Agent", layout="wide")

st.title("Covenant Breach Detection Agent")


rules = load_rules()

if st.button("Run All Checks Now"):
    st.subheader("Results")
    for rule in rules:
        df = load_data_from_rule(rule)
        result = evaluate_rule(rule, df)
        print(result)
        # st.write(result)
        status = classify_alert(result)

        color = "🟢" if status == "OK" else "🟡" if status == "NEAR_BREACH" else "🔴"

        st.write(f"{color} **{rule['id']}** → Status: **{status}**")
        st.write(f"Current Value: {result['value']} | Limit: {result['limit']} | Operator: {result['operator']} | New Breach Value: {result['new_breach_value']}")

        # if status != "OK":
        #     # with st.spinner("Generating explanation using LLM..."):
        #     #     explanation = generate_explanation(result)
        #     st.info("explanation")
