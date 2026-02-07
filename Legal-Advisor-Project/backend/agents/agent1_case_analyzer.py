import os
import google.generativeai as genai
import json

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")


def agent1_analyze_case(query: str) -> dict:
    prompt = f"""
You are a senior Indian criminal lawyer.

Analyse the case and RETURN ONLY VALID JSON in this format:

{{
  "charge": "IPC section / offence",
  "severity": "Low / Medium / High",
  "max_punishment_years": number,
  "key_defence_point": "short defence",
  "case_duration_years": "estimated duration"
}}

Case:
{query}
"""

    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print("Agent 1 error:", e)
        return {
            "charge": "Unknown IPC offence",
            "severity": "Medium",
            "max_punishment_years": 5,
            "key_defence_point": "Insufficient evidence",
            "case_duration_years": "2–3 years"
        }
