# Financial Risk Analysis Agent MCP Server
from fastmcp import FastMCP

mcp = FastMCP("RiskRulesDB")

@mcp.tool()
def analyze_financial_risk(income: float, credit_score: int, loan_amount: float, existing_liabilities: float) -> dict:
    """Calculates debt-to-income ratio, risk levels, and performs anomaly detection."""
    dti = (existing_liabilities / income) if income > 0 else 1.0
    
    credit_risk = "Low" if credit_score >= 750 else ("Medium" if credit_score >= 650 else "High")
    loan_amount_risk = "High" if loan_amount > (income * 5) else "Low"
    
    anomaly_detected = False
    reasoning = f"DTI calculated at {round(dti, 2)}. Credit score indicates {credit_risk} risk."
    
    if credit_score < 500:
        anomaly_detected = True
        reasoning += " CRITICAL ALERT: Extremely low credit score."

    return {
        "debt_to_income_ratio": round(dti, 2),
        "credit_score_risk_level": credit_risk,
        "loan_amount_risk": loan_amount_risk,
        "anomaly_detection": anomaly_detected,
        "reasoning": reasoning
    }

if __name__ == "__main__":
    mcp.run()