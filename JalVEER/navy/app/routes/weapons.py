from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter(prefix="/weapons", tags=["Weapons"])

@router.get("/{country}")
def get_weapons(country: str):

    df = pd.read_csv("data/navy_systems_enhanced_82.csv")

    filtered = df[df["country"].str.strip().str.lower() == country.strip().lower()]

    if filtered.empty:
        raise HTTPException(status_code=404, detail="No weapons found")

    weapons = []

    for _, row in filtered.iterrows():
        weapons.append({
            "system_id": row["system_id"],
            "name": row["system_name"],
            "type": row["system_type"],
            "image": row["image_url"],
            "wikipedia": row["wikipedia_url"]
        })

    return weapons