import os
import google.generativeai as genai
import json

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")


def agent2_risk_evaluate(case_summary: dict) -> dict:
    prompt = f"""
You are a legal risk assessment AI for Indian criminal cases.

Based on the case summary below, RETURN ONLY VALID JSON:

{{
  "risk_score": number (0-10),
  "best_case": "best possible outcome",
  "worst_case": "worst possible outcome",
  "arrest_risk": "Low / Medium / High",
  "bail_difficulty": "Easy / Medium / Hard",
  "pmla_risk": "Low / Medium / High"
}}

Case Summary:
{case_summary}
"""

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print("Agent 2 error:", e)
        return {
            "risk_score": 6,
            "best_case": "Case dismissed or fine",
            "worst_case": "Conviction with imprisonment",
            "arrest_risk": "Medium",
            "bail_difficulty": "Medium",
            "pmla_risk": "Low"
        }
