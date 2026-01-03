import streamlit as st
from engine.data_loader import load_metrics
from engine.rule_engine import load_rules, evaluate_rule
from engine.alert_engine import classify_alert
from engine.llm_explainer import generate_explanation

st.set_page_config(page_title="Covenant Breach Detection Agent", layout="wide")

st.title("📊 Covenant Breach Detection Agent")

df = load_metrics()
rules = load_rules()

st.header("Latest Metrics")
st.dataframe(df.tail(5))

if st.button("Run All Checks Now"):
    st.subheader("Results")
    for rule in rules:
        result = evaluate_rule(rule, df)
        status = classify_alert(result)

        color = "🟢" if status == "OK" else "🟡" if status == "NEAR_BREACH" else "🔴"

        st.write(f"{color} **{rule['id']}** → Status: **{status}**")
        st.write(f"Value: {result['value']} | Limit: {result['limit']}")

        if status != "OK":
            with st.spinner("Generating explanation using LLM..."):
                explanation = generate_explanation(result)
            st.info(explanation)
