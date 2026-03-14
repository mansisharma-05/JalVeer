import joblib
import pandas as pd

import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "war_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_winner(attacker_data: dict, defender_data: dict):

    input_data = {
        'att_avg_threat': attacker_data['threat_level'],
        'att_avg_tech_gen': attacker_data['tech_generation'],
        'att_avg_stealth': attacker_data['stealth_rating'],
        'att_avg_ew': attacker_data['ew_capability'],
        'att_fighter_count': 50,
        'att_military_budget': 100,

        'dfn_avg_threat': defender_data['threat_level'],
        'dfn_avg_tech_gen': defender_data['tech_generation'],
        'dfn_avg_stealth': defender_data['stealth_rating'],
        'dfn_avg_ew': defender_data['ew_capability'],
        'dfn_fighter_count': 50,
        'dfn_military_budget': 100,
    }

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "attacker_win": int(prediction),
        "win_probability": float(probability)
    }