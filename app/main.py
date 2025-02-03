from fastapi import FastAPI, APIRouter, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
import json
from typing import Any, List, Dict
from pydantic import BaseModel
from config import settings, setup_app_logging
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router, router_webscrap_eu, router_webscrap_us, router_portefeuille
from datetime import date, datetime
import yaml

#______________________________data class_______________________
@dataclass
class RatioPutCall:
    date: date
    ratio_name: str
    ratio_value: str


class RatioPutCallResponse(BaseModel):
    date: date
    ratio_name: str
    ratio_value: str


def charger_json(fichier_json):
    with open(fichier_json, mode="r", encoding="utf-8") as json_file:
        donnees = json.load(json_file)
    return donnees

#______________________________configuration_______________________


with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

PROJECT_NAME = config["app"]["name"]
API_VERSION = config["app"]["version"]
DEBUG = config["app"]["debug"]
BACKEND_CORS_ORIGINS = config["cors"]["origins"]
LOGGING_LEVEL = config["logging"]["level"]

JSON_FILE_PATH = "../new_data/direct_download_call_put/Put_Call Ration EU - Données Historiques.json"  


app = FastAPI(title=PROJECT_NAME, 
              openapi_url=f"{API_VERSION}/openapi.json"
              )

root_router = APIRouter()

#____________________________________page de démarrage______________________

@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Put/Call ratio API</h1>"
        "<div style='margin-top: 20px;'>"
        "<p>L’objectif est de récupérer le ratio put/call pour différents marchés."
        "L'intérêt de ce ratio est de vérifier si les informations issues des sentiments des marchés financiers sont déjà prises "
        "en compte dans les prix des actifs. Les données sont obtenus  "
        "en utilisant des données de marchés financiers réels "
        "et des ratios put/call collectés via des techniques de web scraping.</p>"
        "</div>"
        "<div style='margin-top: 20px;'>"
        "Merci de consulter la documentation <a href='/docs'>ici</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return HTMLResponse(content=body)

#_____________________________router_______________________

app.include_router(api_router, prefix=API_VERSION)
app.include_router(root_router)
app.include_router(router_webscrap_us, prefix="/api/v1")
app.include_router(router_webscrap_eu, prefix="/api/v1")
app.include_router(router_portefeuille, prefix="/api/v1")


#____________________________________put_call_us______________________
put_call_us_list = [
    RatioPutCall(
        date=datetime.strptime(item["Date"], "%Y-%m-%d").date(),
        ratio_name=item["Ratio Name"],
        ratio_value=item["Ratio Value"],
    )
    for item in charger_json(
        "../new_data/webscrapped_call_put_ratio/Put_Call Ratio US -Données Historiques 2019_2024.json"
    )
]
put_call_us_dict = {item.date: item for item in put_call_us_list}

@app.get("/api/v1/put-call-ratio-us/{date}", response_model=RatioPutCallResponse)
async def get_put_call_ratio_us(date: str):
    """
    Récupère le put-call-ratio dans notre base pour une date donnée (format YYYY-MM-DD).
    """
    try:
        # Conversion de la date au format datetime.date pour validation
        valid_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Format de date invalide. Utilisez 'YYYY-MM-DD'."
        )

    ratio_data = put_call_us_dict.get(valid_date)
    if not ratio_data:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune donnée trouvée pour la date {date}. Rappel, les doonnées ne sont pas disponible les week-ends",
        )

    return RatioPutCallResponse(
        date=ratio_data.date,
        ratio_name=ratio_data.ratio_name,
        ratio_value=ratio_data.ratio_value,
    )


@app.get("/api/v1/put-call-ratio-us/", response_model=List[RatioPutCallResponse])
async def get_all_put_call_ratios():
    """
    Récupère tous les put-call ratios de notre base.
    """
    return [
        RatioPutCallResponse(
            date=ratio.date, ratio_name=ratio.ratio_name, ratio_value=ratio.ratio_value
        )
        for ratio in put_call_us_list
    ]
#____________________________________put_call_europe______________________



@app.get("/api/v1/put-call-ratio-eu/", response_model=List[Dict[str, str]])
async def get_put_call_ratio_eu():
    """
    Récupère les données du Put-Call Ratio à partir d'un fichier JSON.
    """
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier JSON introuvable.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur de décodage du fichier JSON.")




#_________________________________actifs du portefeuille________________________________________________



# Initialisation du portefeuille avec des calculs dynamiques
file_paths = [
    "../new_data/full_data/BHP_Group_updated_financial_data.csv",
    "../new_data/full_data/BP_PLC_updated_financial_data.csv",
    "../new_data/full_data/FMC_Corp_updated_financial_data.csv",
    "../new_data/full_data/Stora_Enso_updated_financial_data.csv",
    "../new_data/full_data/Total_Energies_updated_financial_data.csv"
]
stock_names = ["BHP_Group", "BP_PLC", "FMC_Corp", "Stora_Enso", "Total_Energies"]
bullish_threshold = -1
bearish_threshold = 1


@app.get("/financial_data")
def get_financial_data():
    """Renvoie les cours financiers des actions."""
    financial_data = {}
    for stock in stock_names:
        df = pd.read_csv(f"new_data/full_data/{stock}_updated_financial_data.csv")
        financial_data[stock] = df[["Date", "Close"]].to_dict(orient='records')

    return financial_data


#_________________________________Var d'un portefeuille basé sur des actif du secteru de l'énergie_________________________________________



VAR_JSON_FILE = "...\new_output\results\var\financial_data_with_var.json"  # 📁 Modifier selon ton chemin réel

@app.get("/api/v1/var-data/", response_model=List[Dict[str, str]])
async def get_var_data():
    """
    Récupère les données VaR (Value at Risk) à partir d'un fichier JSON.
    """
    try:
        with open(VAR_JSON_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier JSON introuvable.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur de décodage du fichier JSON.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001, log_level="debug")








#_________________________________________________CORS__________________

# # Set all CORS enabled origins
if BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")

