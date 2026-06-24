# Loan Decision Agent MCP Server
from fastmcp import FastMCP

mcp = FastMCP("DecisionSynthesis")

@mcp.tool()
def synthesize_decision(profile_summary: dict, risk_summary: dict) -> dict:
    """Synthesizes all factors into a definitive loan approval classification status."""
    
    if risk_summary.get("anomaly_detection") or risk_summary.get("credit_score_risk_level") == "High":
        classification = "Rejected"
        confidence_level = 0.98
        explanation = "Application rejected due to critical financial risk indicators or anomalies."
    elif risk_summary.get("credit_score_risk_level") == "Medium" or risk_summary.get("debt_to_income_ratio", 0) > 0.45:
        classification = "Requires Manual Review"
        confidence_level = 0.85
        explanation = "Borderline metrics detected (high DTI or fair credit score). Routing to credit officers."
    else:
        classification = "Approved"
        confidence_level = 0.95
        explanation = "Applicant meets all healthy automated safety thresholds."

    return {
        "classification": classification,
        "risk_score": 100 - (0.4 * risk_summary.get("debt_to_income_ratio", 0)*100), # Mock index
        "confidence_level": confidence_level,
        "key_decision_factors": f"DTI: {risk_summary.get('debt_to_income_ratio')}, Employment Risk: {profile_summary.get('employment_risk')}",
        "explanation": explanation
    }

if __name__ == "__main__":
    mcp.run()