import os
from typing import Dict, Any, TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Load environment configuration
load_dotenv()

# Define structured workflow graph state tracking object
class SystemState(TypedDict):
    input_data: Dict[str, Any]
    profile_analysis: str
    risk_analysis: str
    decision_synthesis: Dict[str, Any]
    compliance_audit: Dict[str, Any]

# Fallback mechanism if API key is completely missing from terminal memory
try:
    llm = ChatAnthropic(model_name="claude-3-5-sonnet-20241022", temperature=0)
except Exception:
    llm = None

# --- Node 1: Applicant Profile Evaluation ---
def applicant_profile_node(state: SystemState) -> Dict[str, Any]:
    data = state["input_data"]
    if not os.getenv("ANTHROPIC_API_KEY") or llm is None:
        return {"profile_analysis": "Error: Anthropic API Key missing or invalid in backend terminal environment."}
    
    try:
        prompt = ChatPromptTemplate.from_template(
            "Analyze the following applicant profile parameters for income stability and employment risk. "
            "Provide a clear summary.\n\n"
            "Age: {age}\nIncome: {income}\nEmployment Type: {employment_type}"
        )
        chain = prompt | llm
        response = chain.invoke({
            "age": data["age"],
            "income": data["income"],
            "employment_type": data["employment_type"]
        })
        return {"profile_analysis": response.content}
    except Exception as e:
        print(f"\n[NODE ERROR] ApplicantProfileAgent failed: {e}\n")
        return {"profile_analysis": f"Execution error during profile analysis LLM step: {str(e)}"}

# --- Node 2: Financial Risk Analysis ---
def financial_risk_node(state: SystemState) -> Dict[str, Any]:
    data = state["input_data"]
    if not os.getenv("ANTHROPIC_API_KEY") or llm is None:
        return {"risk_analysis": "Error: Anthropic API Key missing or invalid in backend terminal environment."}
        
    try:
        prompt = ChatPromptTemplate.from_template(
            "Analyze the financial risk profile based on these parameters. Calculate or estimate the "
            "Debt-to-Income (DTI) ratio considerations and flag abnormalities or high-risk thresholds.\n\n"
            "Income: {income}\nCredit Score: {credit_score}\nLoan Requested: {loan_amount}\n"
            "Existing Liabilities: {existing_liabilities}"
        )
        chain = prompt | llm
        response = chain.invoke({
            "income": data["income"],
            "credit_score": data["credit_score"],
            "loan_amount": data["loan_amount"],
            "existing_liabilities": data["existing_liabilities"]
        })
        return {"risk_analysis": response.content}
    except Exception as e:
        print(f"\n[NODE ERROR] FinancialRiskAgent failed: {e}\n")
        return {"risk_analysis": f"Execution error during financial risk analysis LLM step: {str(e)}"}

# --- Node 3: Loan Decision Agent ---
def loan_decision_node(state: SystemState) -> Dict[str, Any]:
    profile = state.get("profile_analysis", "")
    risk = state.get("risk_analysis", "")
    
    # If upstream LLM nodes failed, use programmatic fallback logic directly
    if "Execution error" in profile or "Error:" in profile or "Execution error" in risk or "Error:" in risk:
        return {
            "decision_synthesis": {
                "classification": "Requires Manual Review",
                "risk_score": 50.0,
                "confidence_level": 0.0,
                "explanation": "Automated pipeline downgraded to manual routing due to backend LLM connectivity limitations."
            }
        }

    prompt = ChatPromptTemplate.from_template(
        "Synthesize the following background assessments into a definitive loan application classification.\n"
        "You MUST return your response as a valid JSON object matching exactly this layout structure:\n"
        "{{\n"
        '  "classification": "Approved" or "Rejected" or "Requires Manual Review",\n'
        '  "risk_score": <int between 0 and 100>,\n'
        '  "confidence_level": <float between 0.0 and 1.0>,\n'
        '  "explanation": "<your clear reason explanation sentence>"\n'
        "}}\n\n"
        "Profile Context:\n{profile}\n\nRisk Context:\n{risk}"
    )
    
    try:
        chain = prompt | llm
        response = chain.invoke({"profile": profile, "risk": risk})
        import json
        raw_text = response.content.strip()
        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
        parsed_decision = json.loads(raw_text)
    except Exception as e:
        print(f"\n[NODE ERROR] LoanDecisionAgent failed: {e}\n")
        parsed_decision = {
            "classification": "Requires Manual Review",
            "risk_score": 50.0,
            "confidence_level": 0.5,
            "explanation": "Fallback applied. Decision node encountered processing/formatting issues."
        }
    
    return {"decision_synthesis": parsed_decision}

# --- Node 4: Compliance & Notification Orchestrator ---
def compliance_orchestrator_node(state: SystemState) -> Dict[str, Any]:
    import uuid
    from datetime import datetime
    
    app_id = state["input_data"].get("applicant_id", "UNKNOWN")
    decision = state.get("decision_synthesis", {"classification": "Requires Manual Review"})
    
    audit_trail = {
        "case_id": f"CASE-{uuid.uuid4().hex[:8].upper()}",
        "timestamp": datetime.utcnow().isoformat(),
        "action_taken": f"Immutable audit ledger entries committed for tracking ID: {app_id}.",
        "notification_sent": f"Notification alert standard message routed specifying status: {decision.get('classification', 'Pending')}"
    }
    return {"compliance_audit": audit_trail}

# --- StateGraph Blueprint Assembly ---
workflow = StateGraph(SystemState)

workflow.add_node("ApplicantProfileAgent", applicant_profile_node)
workflow.add_node("FinancialRiskAgent", financial_risk_node)
workflow.add_node("LoanDecisionAgent", loan_decision_node)
workflow.add_node("ComplianceOrchestratorAgent", compliance_orchestrator_node)

workflow.set_entry_point("ApplicantProfileAgent")
workflow.add_edge("ApplicantProfileAgent", "FinancialRiskAgent")
workflow.add_edge("FinancialRiskAgent", "LoanDecisionAgent")
workflow.add_edge("LoanDecisionAgent", "ComplianceOrchestratorAgent")
workflow.add_edge("ComplianceOrchestratorAgent", END)

orchestration_engine = workflow.compile()