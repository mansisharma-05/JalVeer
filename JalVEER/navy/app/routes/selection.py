from fastapi import APIRouter, HTTPException, Query
import pandas as pd

router = APIRouter(prefix="/weapon-selection", tags=["Weapon Selection"])

@router.get("/")
def get_weapons_for_two_countries(
    country1: str = Query(...),
    country2: str = Query(...)
):

    df = pd.read_csv("data/navy_systems_enhanced_82.csv")

    weapons_country1 = df[df["country"].str.strip().str.lower() == country1.strip().lower()]
    weapons_country2 = df[df["country"].str.strip().str.lower() == country2.strip().lower()]

    if weapons_country1.empty:
        raise HTTPException(status_code=404, detail=f"No weapons found for {country1}")

    if weapons_country2.empty:
        raise HTTPException(status_code=404, detail=f"No weapons found for {country2}")

    return {
        "country1": {
            "name": country1,
            "weapons": [
                {
                    "system_id": row["system_id"],
                    "name": row["system_name"],
                    "image": row["image_url"]
                }
                for _, row in weapons_country1.iterrows()
            ]
        },
        "country2": {
            "name": country2,
            "weapons": [
                {
                    "system_id": row["system_id"],
                    "name": row["system_name"],
                    "image": row["image_url"]
                }
                for _, row in weapons_country2.iterrows()
            ]
        }
    }