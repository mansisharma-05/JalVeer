import pandas as pd
from model.predict import predict_winner

def compare_by_id(weapon1_id: str, weapon2_id: str):

    systems_df = pd.read_csv("data/navy_systems_enhanced_82.csv")
    countries_df = pd.read_csv("data/naval_countries_profiles.csv")

    w1 = systems_df[systems_df["system_id"] == weapon1_id]
    w2 = systems_df[systems_df["system_id"] == weapon2_id]

    if w1.empty or w2.empty:
        raise ValueError("Weapon not found")

    w1_data = w1.iloc[0].to_dict()
    w2_data = w2.iloc[0].to_dict()

    # Get country flag URLs
    c1 = countries_df[countries_df["country"] == w1_data["country"]]
    c2 = countries_df[countries_df["country"] == w2_data["country"]]

    flag1 = c1.iloc[0]["flag_url"] if not c1.empty else None
    flag2 = c2.iloc[0]["flag_url"] if not c2.empty else None

    # ML Prediction
    result = predict_winner(w1_data, w2_data)

    winner_weapon = (
        w1_data["system_name"]
        if result["attacker_win"] == 1
        else w2_data["system_name"]
    )

    winner_country = (
        w1_data["country"]
        if result["attacker_win"] == 1
        else w2_data["country"]
    )

    return {
        "comparison": {
            "country1": w1_data["country"],
            "flag1": flag1,
            "weapon1": w1_data["system_name"],
            "weapon1_image": w1_data["image_url"],
            "weapon1_wikipedia": w1_data["wikipedia_url"],

            "country2": w2_data["country"],
            "flag2": flag2,
            "weapon2": w2_data["system_name"],
            "weapon2_image": w2_data["image_url"],
            "weapon2_wikipedia": w2_data["wikipedia_url"]
        },

        "technical_specs": {
            "tech_generation": [w1_data["tech_generation"], w2_data["tech_generation"]],
            "stealth_rating": [w1_data["stealth_rating"], w2_data["stealth_rating"]],
            "ew_capability": [w1_data["ew_capability"], w2_data["ew_capability"]],
            "range_km": [w1_data["range_km"], w2_data["range_km"]],
            "max_speed_kmph": [w1_data["max_speed_kmph"], w2_data["max_speed_kmph"]],
            "threat_level": [w1_data["threat_level"], w2_data["threat_level"]],
            "reliability": [w1_data["reliability"], w2_data["reliability"]]
        },

        "ml_prediction": {
            "winner_weapon": winner_weapon,
            "winner_country": winner_country,
            "win_probability": result["win_probability"]
        }
    }