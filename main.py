# from typing import Any, List
# from fastapi import APIRouter, FastAPI, Query, Request
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import HTMLResponse
# from loguru import logger
# from src.domain.put_call_ratio_with_contracts import calculate_put_call_ratio, compare_firms, get_historical_data
# from new_app.config import settings, setup_app_logging
# from new_app.api import api_router
# import json
# from dataclasses import dataclass
# from typing import Union


from fastapi import FastAPI
from dataclasses import dataclass
import json
from pydantic import BaseModel

class RatioPutCall(BaseModel):
    date: str
    ratio_name: str
    ratio_value: str


def charger_json(fichier_json):
    with open(fichier_json, mode='r', encoding='utf-8') as json_file:
        donnees = json.load(json_file)
    return donnees

put_call_us_list = [
    RatioPutCall(date=item['Date'], ratio_name=item['Ratio Name'], ratio_value=item['Ratio Value'])
    for item in charger_json("new_data/webscrapped_call_put_ratio/Put_Call_Ratio_2019_2024.json")
]

app = FastAPI()

@app.get("/get-ratio")
def get_ratio():
    # Retourner les objets dataclass sous forme de dictionnaire
    return [item.__dict__ for item in put_call_us_list]



















# setup_app_logging(config=settings)

# # # Create the FastAPI application
# app = FastAPI(
#     title=settings.PROJECT_NAME, 
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )
# # Root router for basic HTML response
# root_router = APIRouter()

# @root_router.get("/")
# def index(request: Request) -> Any:
#     """Basic HTML response."""
#     body = (
#         "<html>"
#         "<body style='padding: 10px;'>"
#         "<h1>Welcome to the API</h1>"
#         "<div>"
#         "Check the docs: <a href='/docs'>here</a>"
#         "</div>"
#         "</body>"
#         "</html>"
#     )
#     return HTMLResponse(content=body)

# # Include additional routes for specific API functionalities
# @root_router.get("/ratios/{firm}")
# async def get_put_call_ratio(firm: str, date: str = Query(None)):
#     """
#     Return the put/call ratio for a given firm.
#     """
#     ratio = calculate_put_call_ratio(firm, date)
#     return {"firm": firm, "date": date, "put_call_ratio": ratio}

# @root_router.get("/compare")
# async def compare_firms_ratios(firm1: str, firm2: str):
#     """
#     Compare put/call ratios between two firms.
#     """
#     comparison = compare_firms(firm1, firm2)
#     return {"firm1": firm1, "firm2": firm2, "comparison": comparison}

# @root_router.get("/historical")
# async def get_historical_ratios(firm: str, start_date: str, end_date: str):
#     """
#     Return historical put/call ratios for a given firm.
#     """
#     history = get_historical_data(firm, start_date, end_date)
#     return {"firm": firm, "history": history}

# # Include the routers
# app.include_router(api_router, prefix=settings.API_V1_STR)
# app.include_router(root_router)

# # Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# if __name__ == "__main__":
#     # Use this for debugging purposes only
#     logger.warning("Running in development mode. Do not run like this in production.")
#     import uvicorn  # type: ignore
#     uvicorn.run(app, host="localhost", port=8001, log_level="debug")
