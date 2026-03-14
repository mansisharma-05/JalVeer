from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import country, weapons, comparison
from routes import selection

app = FastAPI(title="Naval Weapon Comparison API")

# Include routes
app.include_router(country.router)
app.include_router(weapons.router)
app.include_router(selection.router)
app.include_router(comparison.router)

@app.get("/")
def read_root():
    return {"Welcome to the Naval Weapon Comparison API!"}

# Static images route
app.mount("/static", StaticFiles(directory="static"), name="static")