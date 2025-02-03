from fastapi import APIRouter, Query
from api.put_call_us_webscraper import RatioScraperUS
from api.put_call_europe_webscraper import LastMonthDataScraperEurope
from api.construct_portfolio import ConstructPortfolio

# Créer un router pour les routes de l'API
api_router = APIRouter()
router_webscrap_us = APIRouter()
router_webscrap_eu = APIRouter()
router_portefeuille = APIRouter()

#_____________________________________status________________________________
@api_router.get("/status")
async def status():
    """
    Endpoint pour vérifier le statut de l'API.
    """
    return {"status": "ok", "message": "API is up and running"}

#______________________________________scraping________________________________

@router_webscrap_us.get("/scrape-put-call-ratio_us/")
async def scrape_put_call_ratio_us(
    start_date: str = Query(..., description="Date de début (YYYY-MM-DD)"),
    end_date: str = Query(None, description="Date de fin (YYYY-MM-DD, optionnelle)"),
    save: bool = Query(False, description="Enregistrer en CSV"),
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


@router_webscrap_eu.get("/scrape-put-call-ratio-eu/")
async def scrape_put_call_ratio_eu(save: bool = Query(False, description="Enregistrer en CSV")):
    """
    Lancer le scraping du ratio PUT/CALL pour l'Europe.
    Si `save` est activé, les résultats seront sauvegardés en CSV.
    """
    scraper = LastMonthDataScraperEurope()
    data = scraper.scrape_data()

    if save:
        filename = scraper.save_to_csv()
        return {"message": "Scraping terminé", "data": data, "csv_file": filename}
    
    return {"message": "Scraping terminé", "data": data}


#______________________________________portefeuille________________________________

FILE_PATHS = [
    "../new_data/full_data/BHP_Group_updated_financial_data.csv",
    "../new_data/full_data/BP_PLC_updated_financial_data.csv",
    "../new_data/full_data/FMC_Corp_updated_financial_data.csv",
    "../new_data/full_data/Stora_Enso_updated_financial_data.csv",
    "../new_data/full_data/Total_Energies_updated_financial_data.csv"
]
STOCK_NAMES = ["BHP_Group", "BP_PLC", "FMC_Corp", "Stora_Enso", "Total_Energies"]

@router_portefeuille.get("/calculate_weights/")
async def calculate_weights(bullish_threshold: float = -1, bearish_threshold: float = 1):
    """
    Calcule les poids du portefeuille en utilisant les fichiers CSV existants.
    """

    # Exécute l’analyse
    portfolio = ConstructPortfolio(FILE_PATHS, STOCK_NAMES)
    portfolio.merge_put_call_ratios()
    portfolio.calculate_signals(bullish_threshold, bearish_threshold)
    portfolio.calculate_dynamic_portfolio_weights()

    # Récupération des poids sous forme de dictionnaire
    weights_df = portfolio.weight_data.reset_index()
    weights_dict = weights_df.to_dict(orient="records")

    return {"weights": weights_dict}