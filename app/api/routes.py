from fastapi import APIRouter

# Créer un router pour les routes de l'API
api_router = APIRouter()

@api_router.get("/status")
async def status():
    """
    Endpoint pour vérifier le statut de l'API.
    """
    return {"status": "ok", "message": "API is up and running"}