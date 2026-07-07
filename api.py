from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

from main import run_pipeline_api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://finly-ai-cfo-agent.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FinlyAI API Running 🚀"}


class CFOInput(BaseModel):
    revenue: float
    expenses: float
    tax_rate: float = 0.1


@app.post("/cfo")
def cfo(data: CFOInput):
    profit = data.revenue - data.expenses
    tax = profit * data.tax_rate
    net_profit = profit - tax

    margin = (net_profit / data.revenue) * 100 if data.revenue else 0

    return {
        "revenue": data.revenue,
        "expenses": data.expenses,
        "profit_before_tax": profit,
        "tax": tax,
        "net_profit": net_profit,
        "profit_margin_percent": round(margin, 2),
        "status": "healthy" if net_profit > 0 else "loss",
    }


@app.get("/dashboard")
def dashboard():

    result = run_pipeline_api()

    if not result["success"]:
        return result

    cash = result["cashPosition"]

    analysis = result["analysis"]

    # Convert analysis to a list if needed
    if isinstance(analysis, dict):
        alerts = [f"{k}: {v}" for k, v in analysis.items()]
    elif isinstance(analysis, list):
        alerts = analysis
    else:
        alerts = [str(analysis)]

    return {
        "company": "FinlyAI",
        "timestamp": datetime.now().isoformat(),

        "kpis": {
            "total_revenue": 500000,
            "total_expenses": 320000,
            "net_profit": cash["cash_on_hand"],
            "profit_margin": 36,
        },

        "cashflow": {
            "inflow": cash["accounts_receivable_due_14d"],
            "outflow": cash["accounts_payable_due_14d"],
            "net": cash["cash_on_hand"],
        },

        "alerts": alerts,
    }