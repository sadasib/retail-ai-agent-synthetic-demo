import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Retail AI Agent Demo", layout="wide")

BASE = Path(__file__).resolve().parents[1]
CSV_PATH = BASE / "data" / "synthetic_scenarios.csv"

def load_data() -> pd.DataFrame:
    return pd.read_csv(CSV_PATH)

st.title("Retail AI Agent Demo")
st.caption("Synthetic retail scenarios showing how an AI assistant should answer, clarify, or escalate.")

cases = load_data()

col1, col2, col3 = st.columns(3)
col1.metric("Scenarios", len(cases))
col2.metric("Answer", int((cases["recommended_action"] == "Answer").sum()))
col3.metric("Escalate", int((cases["recommended_action"] == "Escalate").sum()))

st.markdown("## Scenario Explorer")
selected = st.selectbox("Choose a scenario", cases["scenario_name"].tolist())
row = cases[cases["scenario_name"] == selected].iloc[0]

left, right = st.columns([1, 1])
with left:
    st.subheader("Customer need")
    st.write(row["customer_need"])
    st.subheader("Agent decision")
    st.success(row["recommended_action"])
    st.subheader("Why")
    st.write(row["rationale"])

with right:
    st.subheader("Risk signals")
    st.write(row["risk_signals"])
    st.subheader("Suggested response pattern")
    st.write(row["response_pattern"])

st.markdown("## All scenarios")
st.dataframe(cases[["scenario_name", "use_case", "recommended_action", "risk_level"]], use_container_width=True)

st.markdown("## Product leadership notes")
st.info("The goal is not to build a perfect chatbot. The goal is to define the customer problem, the safety boundaries, the escalation path, and the evaluation criteria before launch.")
