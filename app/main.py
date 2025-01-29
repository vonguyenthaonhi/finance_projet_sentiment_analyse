# from typing import Any, List
# from fastapi import APIRouter, FastAPI, Query, Request
# from fastapi.middleware.cors import CORSMiddleware
# from loguru import logger
# from src.domain.put_call_ratio_with_contracts import calculate_put_call_ratio, compare_firms, get_historical_data
# from new_app.api import api_router
# import json
# from dataclasses import dataclass
# from typing import Union


from fastapi import FastAPI, APIRouter, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse
from dataclasses import dataclass
import json
from typing import Any, List
from pydantic import BaseModel
from config import settings, setup_app_logging
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router, router
from datetime import date, datetime
import yaml


@dataclass
class RatioPutCall():
    date: date
    ratio_name: str
    ratio_value: str


class RatioPutCallResponse(BaseModel):
    date: date
    ratio_name: str
    ratio_value: str


def charger_json(fichier_json):
    with open(fichier_json, mode='r', encoding='utf-8') as json_file:
        donnees = json.load(json_file)
    return donnees

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

PROJECT_NAME = config["app"]["name"]
API_VERSION = config["app"]["version"]
DEBUG = config["app"]["debug"]
BACKEND_CORS_ORIGINS = config["cors"]["origins"]
# DATABASE_URL = config["database"]["url"]
LOGGING_LEVEL = config["logging"]["level"]


put_call_us_list = [
    RatioPutCall(
        date=datetime.strptime(item['Date'], "%Y-%m-%d").date(),
        ratio_name=item['Ratio Name'],
        ratio_value=item['Ratio Value']
    )
    for item in charger_json("../new_data/webscrapped_call_put_ratio/Put_Call Ratio US -Données Historiques 2019_2024.json")
]
put_call_us_dict = {item.date: item for item in put_call_us_list}

# setup_app_logging(config=settings)

app = FastAPI(
    title=PROJECT_NAME, 
    openapi_url=f"{API_VERSION}/openapi.json"
)

root_router = APIRouter()

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


app.include_router(api_router, prefix=settings.API_VERSION)
app.include_router(root_router)
app.include_router(router, prefix="/api/v1")


@app.get("/api/v1/put-call-ratio-us/{date}", response_model=RatioPutCallResponse)
async def get_put_call_ratio_us(date: str):
    """
    Récupère le put-call-ratio dans notre base pour une date donnée (format YYYY-MM-DD).
    """
    try:
        # Conversion de la date au format datetime.date pour validation
        valid_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez 'YYYY-MM-DD'.")

    ratio_data = put_call_us_dict.get(valid_date)
    if not ratio_data:
        raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour la date {date}. Rappel, les doonnées ne sont pas disponible les week-ends")

    return RatioPutCallResponse(
        date=ratio_data.date,
        ratio_name=ratio_data.ratio_name,
        ratio_value=ratio_data.ratio_value
    )


@app.get("/api/v1/put-call-ratio-us/", response_model=List[RatioPutCallResponse])
async def get_all_put_call_ratios():
    """
    Récupère tous les put-call ratios de notre base.
    """
    return [
        RatioPutCallResponse(
            date=ratio.date,
            ratio_name=ratio.ratio_name,
            ratio_value=ratio.ratio_value
        )
        for ratio in put_call_us_list
    ]
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




# put_call_eu_list = [
#     RatioPutCall(date=item['Date'], ratio_name=None,  ratio_value=item['Ouverture'])
#     for item in charger_json("../new_data/webscrapped_call_put_ratio/Put_Call Ration EU - Données Historiques 12-2024 -01-2025.json")
# ]
# put_call_eu_dict = {item.date: item for item in put_call_eu_list}



# @app.get("/api/v1/put-call-ratio-eu/{date}", 
#          response_model=RatioPutCallResponse)
# async def get_put_call_ratio_eu(date: str):
#     """
#     Récupère le put-call-ratio pour une date donnée.
#     """
#     ratio_data = put_call_eu_dict.get(date)
#     if not ratio_data:
#         raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour la date {date}")
    
#     return RatioPutCallResponse(
#         date=ratio_data.date,
#         ratio_name=ratio_data.ratio_name,
#         ratio_value=ratio_data.ratio_value
#     )

# @app.get("/api/v1/compare-put-call-ratio/{date}")
# async def compare_put_call_ratio(date: str):
#     """
#     Compare le put-call-ratio pour une date donnée entre les données US et EU.
#     """
#     ratio_us = put_call_us_dict.get(date)
#     ratio_eu = put_call_eu_dict.get(date)
    
#     if not ratio_us and not ratio_eu:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Aucune donnée trouvée pour la date {date} ni pour les données US ni EU."
#         )
#     elif not ratio_us:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Aucune donnée trouvée pour les données US à la date {date}."
#         )
#     elif not ratio_eu:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Aucune donnée trouvée pour les données EU à la date {date}."
#         )
    
#     return {
#         "date": date,
#         "us_ratio": {
#             "ratio_name": ratio_us.ratio_name,
#             "ratio_value": ratio_us.ratio_value,
#         },
#         "eu_ratio": {
#             "ratio_name": ratio_eu.ratio_name,
#             "ratio_value": ratio_eu.ratio_value,
#         },
#         "comparison": {
#             "is_us_higher": float(ratio_us.ratio_value) > float(ratio_eu.ratio_value),
#             "difference": round(float(ratio_us.ratio_value) - float(ratio_eu.ratio_value), 2),
#         },
#     }