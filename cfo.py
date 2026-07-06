import os
import json
import logging
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from billing import DraftPurchaseOrder

# Setting up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Schema for structured output
class PORecommendation(BaseModel):
    po_id: str
    decision: str = Field(description="Decision: APPROVE, APPROVE WITH CONDITIONS, or HOLD")
    reasoning: str = Field(description="Brief explanation of the decision based on cash flow impact")

class CFORecommendationResponse(BaseModel):
    projected_14d_cash: float
    risk_flag: bool = Field(description="True if there is a cash flow risk, otherwise False")
    risk_reasoning: str = Field(description="Overall cash flow risk assessment and reasoning")
    recommendations: List[PORecommendation]


def build_cfo_prompt(drafts: List[DraftPurchaseOrder], cash: Dict[str, float]) -> str:
    po_lines = "\n".join(
        f"- {p.po_id}: {p.qty} units of {p.sku} ({p.name}) from {p.vendor}, cost ${p.total_cost:,.2f}"
        for p in drafts
    ) or "- No purchase orders pending."

    return f"""You are FinlyAI, an autonomous virtual CFO for a small business.

Current cash position:
- Cash on hand: ${cash['cash_on_hand']:,.2f}
- Accounts receivable due in 14 days: ${cash['accounts_receivable_due_14d']:,.2f}
- Accounts payable due in 14 days: ${cash['accounts_payable_due_14d']:,.2f}
- Average daily burn rate: ${cash['avg_daily_burn']:,.2f}

Pending draft purchase orders triggered by low inventory:
{po_lines}

Task:
1. Calculate the projected 14-day cash position if all draft POs are approved.
   Projected Cash = Cash on Hand + AR (14d) - AP (14d) - Total PO Outflow - (Daily Burn * 14)
2. Flag any cash flow risk. A risk exists if the projected balance falls below a safety floor of 30 days of burn rate.
   Safety Floor = Daily Burn * 30.
3. Give a clear APPROVE / APPROVE WITH CONDITIONS / HOLD recommendation for each PO.
   - APPROVE if there is sufficient liquidity.
   - APPROVE WITH CONDITIONS (e.g. net-30 terms) if liquidity is tight but the PO is smaller.
   - HOLD if it is a large PO contributing heavily to a shortfall.
4. Keep the response executive-style.
"""


def mock_llm_cfo_analysis(drafts: List[DraftPurchaseOrder], cash: Dict[str, float]) -> Dict[str, Any]:
    """Deterministic mock reasoning engine. Matches structure of live API response."""
    total_outflow = sum(p.total_cost for p in drafts)
    projected_cash = (
        cash["cash_on_hand"]
        + cash["accounts_receivable_due_14d"]
        - cash["accounts_payable_due_14d"]
        - total_outflow
        - (cash["avg_daily_burn"] * 14)
    )
    safety_floor = cash["avg_daily_burn"] * 30
    risk = projected_cash < safety_floor

    recommendations = []
    for p in drafts:
        if not risk:
            decision = "APPROVE"
            reason = "Sufficient liquidity to cover this order without breaching safety floor."
        elif p.total_cost < total_outflow * 0.5:
            decision = "APPROVE WITH CONDITIONS"
            reason = "Approve but delay payment terms (net-30) to preserve short-term liquidity."
        else:
            decision = "HOLD"
            reason = "Largest contributor to projected shortfall — hold until receivables clear."
        
        recommendations.append({
            "po_id": p.po_id,
            "decision": decision,
            "reasoning": reason
        })

    return {
        "projected_14d_cash": round(projected_cash, 2),
        "risk_flag": risk,
        "risk_reasoning": "CASH FLOW RISK DETECTED - Projected cash is below safety floor of 30 days burn." if risk else "Within safe operating range.",
        "recommendations": recommendations
    }


def live_llm_cfo_analysis(prompt: str, api_key: str) -> Dict[str, Any]:
    """Calls real Gemini API using google-genai SDK, enforcing a structured JSON response."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logging.error("google-genai package is not installed. Falling back to mock reasoning.")
        raise

    client = genai.Client(api_key=api_key)
    
    # We call the gemini-2.5-flash model and require JSON outputs matching the schema
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CFORecommendationResponse,
            temperature=0.1  # Low temperature for more deterministic analysis
        ),
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response from Gemini API: {response.text}")
        raise e


def run_cfo_agent(drafts: List[DraftPurchaseOrder], cash: Dict[str, float]) -> Dict[str, Any]:
    """Fragment 3 entrance point. Analyzes cash flow impact and outputs results."""
    print("\n=== FRAGMENT 3: AI Virtual CFO Agent ===")
    print("Running cash-flow impact analysis on Fragment 1 & 2 outputs...\n")

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("[MOCK MODE - no API key set]")
        analysis = mock_llm_cfo_analysis(drafts, cash)
    else:
        try:
            prompt = build_cfo_prompt(drafts, cash)
            analysis = live_llm_cfo_analysis(prompt, api_key)
        except Exception as e:
            logging.error(f"Error during live Gemini analysis: {e}. Falling back to mock mode.")
            print("[MOCK MODE - fallback due to API error]")
            analysis = mock_llm_cfo_analysis(drafts, cash)

    # Print the analysis results in a readable format
    print("CFO Analysis Results:")
    print(f"  Projected 14-Day Cash: ${analysis.get('projected_14d_cash', 0.0):,.2f}")
    print(f"  Risk Flag: {'[RISK DETECTED]' if analysis.get('risk_flag') else '[SAFE]'}")
    print(f"  Risk Reasoning: {analysis.get('risk_reasoning')}")
    print("  Recommendations:")
    for rec in analysis.get("recommendations", []):
        print(f"    - {rec.get('po_id')}: {rec.get('decision')}")
        print(f"        Reason: {rec.get('reasoning')}")
        
    print("\n>> Fragment 3 complete: CFO recommendation delivered.")
    return analysis
