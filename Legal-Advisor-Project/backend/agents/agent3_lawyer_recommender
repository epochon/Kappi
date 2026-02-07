import os
import pandas as pd
import google.generativeai as genai

# -------------------------------------------------
# Gemini Configuration
# -------------------------------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")

# -------------------------------------------------
# Load Lawyer Dataset
# -------------------------------------------------
# IMPORTANT: Lawyer_ID is STRING (e.g. YL001)
df = pd.read_csv("data/lawyers.csv")

print("✅ Lawyer dataset loaded")
print("✅ Columns:", df.columns.tolist())


def agent3_recommend_lawyer(risk_analysis: dict) -> dict:
    """
    Uses Gemini to classify case type and
    recommends the best matching lawyer
    from the dataset.

    Returns data EXACTLY in UI-expected format.
    """

    # -------------------------------------------------
    # 1️⃣ Classify case type using Gemini
    # -------------------------------------------------
    prompt = f"""
Classify the legal case into ONE category only:
criminal, civil, cyber, corporate, family

Respond with ONLY ONE WORD.

Risk Analysis:
{risk_analysis}
"""

    try:
        response = model.generate_content(prompt)
        case_type = response.text.strip().lower()
    except Exception as e:
        print("❌ Gemini classification failed:", e)
        case_type = "criminal"

    # Safety fallback
    if case_type not in ["criminal", "civil", "cyber", "corporate", "family"]:
        case_type = "criminal"

    # -------------------------------------------------
    # 2️⃣ Filter lawyers by practice area
    # -------------------------------------------------
    filtered = df[
        df["Practice_Area"]
        .astype(str)
        .str.lower()
        .str.contains(case_type)
    ]

    # Fallback if nothing matches
    if filtered.empty:
        filtered = df

    # -------------------------------------------------
    # 3️⃣ Rank by experience (highest first)
    # -------------------------------------------------
    best = filtered.sort_values(
        by="Years_of_Experience",
        ascending=False
    ).iloc[0]

    # -------------------------------------------------
    # 4️⃣ Return structured response (UI SAFE)
    # -------------------------------------------------
    return {
        "recommended_lawyer": {
            "lawyer_id": str(best["Lawyer_ID"]),   # ❗ STRING, NOT int
            "name": best["Name"],
            "city": best["City"],
            "practice_area": best["Practice_Area"],
            "years_of_experience": int(best["Years_of_Experience"]),
            "languages": best["Languages"],
            "availability": best["Availability"]
        }
    }
