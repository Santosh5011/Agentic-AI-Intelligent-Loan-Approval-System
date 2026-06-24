import streamlit as st
import requests
import uuid

# Set page configurations first
st.set_page_config(page_title="Intelligent Loan Approval System", page_icon="🏦", layout="wide")

st.title("🏦 Agentic AI Intelligent Loan Approval System")
st.subheader("Automated Cross-Agent Verification Pipeline Processing Panel")

st.sidebar.header("Submit Loan Application Data")

# Input Parameter Interface Generation
app_id = st.sidebar.text_input("Applicant ID", value=f"APP-{uuid.uuid4().hex[:4].upper()}")
age = st.sidebar.number_input("Applicant Age", min_value=18, max_value=100, value=30)
income = st.sidebar.number_input("Annual Gross Income ($)", min_value=0.0, value=65000.0)
employment_type = st.sidebar.selectbox("Employment Type", options=["Salaried", "Self-Employed", "Unemployed"])
credit_score = st.sidebar.slider("Credit Score Assessment Metric", min_value=300, max_value=850, value=710)
loan_amount = st.sidebar.number_input("Requested Loan Value ($)", min_value=0.0, value=150000.0)
existing_liabilities = st.sidebar.number_input("Existing Monthly Debt Obligations ($)", min_value=0.0, value=1500.0)
location = st.sidebar.text_input("Geographic Asset Location", value="Texas")

if st.sidebar.button("Run Multi-Agent Engine Assessment Pipeline"):
    payload = {
        "applicant_id": app_id,
        "age": age,
        "income": income,
        "employment_type": employment_type,
        "credit_score": credit_score,
        "loan_amount": loan_amount,
        "existing_liabilities": existing_liabilities,
        "location": location
    }
    
    with st.spinner("Orchestrator routing across active LLM agents..."):
        try:
            # Clean target URL string to prevent adapter parsing issues
            target_url = "http://127.0.0.1:8001/api/v1/evaluate-loan".strip()
            
            response = requests.post(target_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                decision_payload = result["decision"]
                audit_payload = result["compliance_and_audit"]
                logs_payload = result["agent_logs"]
                
                status = decision_payload["classification"]
                if status == "Approved":
                    st.success(f"System Decision: {status}")
                elif status == "Rejected":
                    st.error(f"System Decision: {status}")
                else:
                    st.warning(f"System Decision: {status}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Assessment Score Index", f"{round(decision_payload['risk_score'], 1)} / 100")
                col2.metric("Engine Certainty Confidence", f"{int(decision_payload['confidence_level'] * 100)}%")
                col3.metric("Assigned System Tracking Case ID", audit_payload["case_id"])
                
                st.write("### 🧠 Specialized Agent Output Metrics")
                with st.expander("1. Applicant Profile Agent Reasoning Log"):
                    st.write(logs_payload["profile_agent_summary"])
                with st.expander("2. Financial Risk Agent Reasoning Log"):
                    st.write(logs_payload["risk_agent_summary"])
                
                st.write("### 🧠 Decision Factor Analysis & Explanation")
                st.info(decision_payload["explanation"])
                
                st.write("### 📋 Audit Log & Compliance Telemetry Metrics")
                st.json(audit_payload)
                
            else:
                st.error(f"Execution Error Encountered from API Gateway Node. Code: {response.status_code}")
        except Exception as ex:
            st.error(f"Failed to securely reach backend service layers. Details: {ex}")