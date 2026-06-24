# Applicant Profile Agent MCP Server
from fastmcp import FastMCP
import random

mcp = FastMCP("ApplicantDB")

@mcp.tool()
def evaluate_applicant_profile(age: int, income: float, employment_type: str) -> dict:
    """Analyzes income stability, employment risks, and application completeness."""
    # Logic mock for the profile evaluation
    income_stability_score = 0.95 if employment_type.lower() == "salaried" else 0.75
    employment_risk = "Low" if income > 50000 and employment_type.lower() == "salaried" else "Medium"
    
    return {
        "income_stability_score": income_stability_score,
        "employment_risk": employment_risk,
        "credit_history_summary": "Clean recent history, no defaults recorded.",
        "application_completeness_flags": True
    }

if __name__ == "__main__":
    mcp.run()