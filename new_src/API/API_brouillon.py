from fastapi import FastAPI, Query
from typing import List
import polygon
from src.domain.put_call_ratio_with_contracts import calculate_put_call_ratio, compare_firms

app = FastAPI()

@app.get("/ratios/{firm}")
async def get_put_call_ratio(firm: str, date: str = Query(None)):
    """
    Retourne le ratio put/call pour une firme donnée.
    """
    ratio = calculate_put_call_ratio(firm, date)
    return {"firm": firm, "date": date, "put_call_ratio": ratio}

@app.get("/compare")
async def compare_firms_ratios(firm1: str, firm2: str):
    """
    Compare les ratios put/call entre deux firmes.
    """
    comparison = compare_firms(firm1, firm2)
    return {"firm1": firm1, "firm2": firm2, "comparison": comparison}

@app.get("/historical")
async def get_historical_ratios(firm: str, start_date: str, end_date: str):
    """
    Retourne les ratios historiques pour une firme donnée.
    """
    history = get_historical_data(firm, start_date, end_date)
    return {"firm": firm, "history": history}
