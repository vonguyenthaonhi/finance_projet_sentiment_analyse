from fastapi import APIRouter, Query
from api.put_call_us_webscraper import RatioScraperUS

# Créer un router pour les routes de l'API
api_router = APIRouter()
router = APIRouter()

@api_router.get("/status")
async def status():
    """
    Endpoint pour vérifier le statut de l'API.
    """
    return {"status": "ok", "message": "API is up and running"}



@router.get("/scrape-put-call-ratio/")
async def scrape_put_call_ratio(
    start_date: str = Query(..., description="Date de début (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Date de fin (YYYY-MM-DD, optionnelle)"),
    save: bool = Query(False, description="Enregistrer en CSV")
):
    """
    Lancer le scraping du ratio PUT/CALL entre `start_date` et `end_date`.
    Si `save` est activé, les résultats seront sauvegardés en CSV.
    """
    scraper = RatioScraperUS(start_date, end_date, verbose=True)
    data = scraper.scrape_ratios()

    if save:
        scraper.save_to_csv(data)

    return {"message": "Scraping terminé", "data": data}
