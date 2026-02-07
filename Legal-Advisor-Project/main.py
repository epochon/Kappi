from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.agent1_case_analyzer import agent1_analyze_case
from agents.agent2_risk_evaluator import agent2_risk_evaluate
from agents.agent3_lawyer_recommender import agent3_recommend_lawyer

app = FastAPI(title="Multi-Agent Legal AI Backend")

# -------------------------
# CORS (CRITICAL FIX)
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # THIS allows OPTIONS
    allow_headers=["*"],
)

class CaseRequest(BaseModel):
    query: str

# -------------------------
# FIXED ROUTE
# -------------------------
@app.post("/process_case", include_in_schema=True)
async def process_case(data: CaseRequest):
    case_analysis = agent1_analyze_case(data.query)
    risk_analysis = agent2_risk_evaluate(case_analysis)
    lawyer_recommendation = agent3_recommend_lawyer(risk_analysis)

    return {
    "case_summary": case_analysis,   # 🔥 key renamed
    "risk_analysis": risk_analysis,
    "lawyer_recommendation": lawyer_recommendation
}

# -------------------------
# Explicit OPTIONS handler (IMPORTANT)
# -------------------------
@app.options("/process_case")
async def process_case_options():
    return {}

@app.get("/")
def health():
    return {"status": "running"}
