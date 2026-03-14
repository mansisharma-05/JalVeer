from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.get("/")
def get_countries():

    df = pd.read_csv("data/naval_countries_profiles.csv")

    countries = []

    for _, row in df.iterrows():
        countries.append({
            "country": row["country"],
            "flag_image": row["flag_url"]
        })

    return countries