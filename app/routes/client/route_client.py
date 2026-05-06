# from fastapi import APIRouter,Depends,status
# from app.model.client.client_model import Client

# route_client = APIRouter(prefix="/client",tags=["client"])

# @route_client.post("/", status_code=status.HTTP_201_CREATED)
# async def create_client(client: Client):
#     return {"message":"okay"}



# @route_client.get("/test")
#async def test():
#     return {"message": "This is a test endpoint"}
from fastapi import APIRouter, Depends, status
from app.model.client.client_model import Client
from app.middleware.id_authenticate import id_authenticate

route_client = APIRouter(prefix="/client", tags=["client"])

#  PUBLIC 
@route_client.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(client: Client):
    """
    Crée un nouveau client. Cette route est publique et ne nécessite pas d'authentification.
    
    Args:
        client (Client): Les données du client à créer (validées par le modèle).
        
    Returns:
        dict: Un message de confirmation et les données du client reçu.
    """
    return {
        "message": "Client data received (public access)",
        "client": client.dict()
    }


#   seulement utilisateur connecté
@route_client.post("/order")
async def create_order(
    client: Client,
    user_id: str = Depends(id_authenticate)
):
    """
    Crée une commande pour un client. Cette route est protégée et nécessite d'être connecté.
    
    Args:
        client (Client): Les données de la commande/client.
        user_id (str): L'ID de l'utilisateur authentifié (injecté par le middleware).
        
    Returns:
        dict: Un message de confirmation, l'ID de l'utilisateur et les données client.
    """
    return {
        "message": "Order created successfully",
        "user_id": user_id,
        "client": client.dict()
    }


#  TEST ROUTE
@route_client.get("/test")
async def test():
    """
    Route de test simple pour vérifier que les routes client fonctionnent.
    
    Returns:
        dict: Un message de test.
    """
    return {
        "message": "This is a test endpoint"
    }