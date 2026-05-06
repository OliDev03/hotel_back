from fastapi import APIRouter, Depends, status
from supabase import AsyncClient
from app.config.config_supabase import get_supabase_client
from app.model.order.order_model import OrderModel
from app.middleware.id_authenticate import id_authenticate

route_order = APIRouter(prefix="/order", tags=["order"])

# ==========================================
# ROUTES POUR LES CLIENTS
# ==========================================

@route_order.post("/client", status_code=status.HTTP_201_CREATED)
async def create_order_by_client( order:list[OrderModel], supabase: AsyncClient = Depends(get_supabase_client),is_auth:dict=Depends(id_authenticate)):
    """
    Crée une nouvelle commande pour un client.
    
    Args:
        order (OrderModel): Les données de la commande à créer.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message de confirmation et les données de la commande créée.
    """
    # Le client crée une commande

    for order_data in order:
        order_data = order.model_dump()
        client_id = is_auth["user_id"]
        order_data["client_id"] = client_id
        response = await supabase.table("orders").insert(order_data).execute()
    return {"message": "Order created successfully", "data": response.data}

@route_order.get("/client", status_code=status.HTTP_200_OK)
async def get_client_orders(is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Récupère la liste de toutes les commandes passées par le client authentifié.
    
    Args:
        is_auth (dict): Les données d'authentification du client (récupérées via middleware).
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message avec la liste des commandes du client.
    """
    # Le client peut voir ses propres commandes
    client_id = is_auth["user_id"]
    response = await supabase.table("orders").select("*").eq("client_id", client_id).execute()
    return {"message": f"List of orders for client {client_id}", "data": response.data}

@route_order.get("/client/order", status_code=status.HTTP_200_OK)
async def get_client_order_by_id(order_id: str, supabase: AsyncClient = Depends(get_supabase_client),is_auth:dict=Depends(id_authenticate)):
    """
    Récupère les détails d'une commande spécifique appartenant au client authentifié.
    
    Args:
        order_id (str): L'identifiant unique de la commande.
        supabase (AsyncClient): Le client de base de données Supabase.
        is_auth (dict): Les données d'authentification du client (récupérées via middleware).
        
    Returns:
        dict: Les détails de la commande demandée.
    """
    # Le client peut voir les détails d'une de ses commandes
    client_id = is_auth["user_id"]
    response = await supabase.table("orders").select("*").eq("id", order_id).eq("client_id", client_id).execute()
    return {"message": "Order details", "data": response.data}


# ==========================================
# ROUTES POUR LES HOTELS
# ==========================================

@route_order.get("/hotel/order", status_code=status.HTTP_200_OK)
async def get_hotel_orders(is_auth:dict=Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Récupère la liste de toutes les commandes adressées à un hôtel spécifique.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message avec la liste des commandes pour cet hôtel.
    """
    hotel_id = is_auth["user_id"]
    # L'hôtel peut voir toutes les commandes qui lui sont adressées
    response = await supabase.table("orders").select("*").eq("hotel_id", hotel_id).execute()
    return {"message": f"List of orders for hotel {hotel_id}", "data": response.data}

@route_order.get("/hotel/order/get/id", status_code=status.HTTP_200_OK)
async def get_hotel_order_by_id(order_id: str,is_auth:dict=Depends(id_authenticate)  , supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Récupère les détails d'une commande spécifique destinée à un hôtel.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        order_id (str): L'identifiant unique de la commande.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Les détails de la commande demandée.
    """
    hotel_id = is_auth["user_id"]
    # L'hôtel peut voir les détails d'une commande qui lui est adressée
    response = await supabase.table("orders").select("*").eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": "Order details", "data": response.data}

@route_order.put("/hotel/order/update/id", status_code=status.HTTP_200_OK)
async def update_hotel_order( order_id: str, order: OrderModel, supabase: AsyncClient = Depends(get_supabase_client),is_auth:dict=Depends(id_authenticate)):
    """
    Met à jour les informations d'une commande spécifique pour un hôtel (ex: changer le statut).
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        order_id (str): L'identifiant unique de la commande à mettre à jour.
        order (OrderModel): Les nouvelles données de la commande validées par Pydantic.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message de confirmation et les données de la commande mise à jour.
    """
    hotel_id = is_auth["user_id"]
    # L'hôtel peut mettre à jour le statut d'une de ses commandes
    order_data = order.model_dump()
    order_data["hotel_id"] = hotel_id # Sécurité
    
    response = await supabase.table("orders").update(order_data).eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Order {order_id} updated successfully", "data": response.data}

@route_order.delete("/hotel/order/delete/id", status_code=status.HTTP_200_OK)
async def delete_hotel_order( order_id: str,is_auth:dict=Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Supprime ou annule une commande spécifique pour un hôtel.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        order_id (str): L'identifiant unique de la commande à supprimer.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message confirmant la suppression de la commande.
    """
    hotel_id = is_auth["user_id"]
    # L'hôtel peut annuler/supprimer une commande
    response = await supabase.table("orders").delete().eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Order {order_id} deleted successfully", "data": response.data}
