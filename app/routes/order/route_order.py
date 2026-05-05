<<<<<<< HEAD
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import AsyncClient
from app.config.config_supabase import get_supabase_client
from app.middleware.id_authenticate import id_authenticate
from app.model.order.order_model import OrderModel

logger = logging.getLogger(__name__)

route_order = APIRouter(
    prefix="/order",
    tags=["order"]
)


# ───────────────── CLIENT ROUTES ─────────────────

@route_order.post("/client", status_code=status.HTTP_201_CREATED)
async def create_order_by_client(
    order: OrderModel,
    current_user_id: str = Depends(id_authenticate),
    supabase: AsyncClient = Depends(get_supabase_client),
):
    try:

        order_data = order.model_dump()

        order_data["client_id"] = current_user_id

        response = (
            await supabase
            .table("orders")
            .insert(order_data)
            .execute()
        )

        return {
            "message": "Order created successfully",
            "data": response.data
        }

    except Exception as e:
        logger.error("Create order error: %s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create order"
        )


@route_order.get("/client", status_code=status.HTTP_200_OK)
async def get_my_orders(
    current_user_id: str = Depends(id_authenticate),
    supabase: AsyncClient = Depends(get_supabase_client),
):
    try:

        response = (
            await supabase
            .table("orders")
            .select("*")
            .eq("client_id", current_user_id)
            .execute()
        )

        return {
            "message": "Orders fetched successfully",
            "data": response.data
        }

    except Exception as e:
        logger.error("Get client orders error: %s", e)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders"
        )
=======
from fastapi import APIRouter, Depends, status
from supabase import AsyncClient
from app.config.config_supabase import get_supabase_client
from app.model.order.order_model import OrderModel

route_order = APIRouter(prefix="/order", tags=["order"])

# ==========================================
# ROUTES POUR LES CLIENTS
# ==========================================

@route_order.post("/client/{client_id}", status_code=status.HTTP_201_CREATED)
async def create_order_by_client(client_id: str, order: OrderModel, supabase: AsyncClient = Depends(get_supabase_client)):
    # Le client crée une commande
    order_data = order.model_dump()
    order_data["client_id"] = client_id # Sécurité: forcer l'ID du client
    
    response = await supabase.table("orders").insert(order_data).execute()
    return {"message": "Order created successfully", "data": response.data}

@route_order.get("/client/{client_id}", status_code=status.HTTP_200_OK)
async def get_client_orders(client_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # Le client peut voir ses propres commandes
    response = await supabase.table("orders").select("*").eq("client_id", client_id).execute()
    return {"message": f"List of orders for client {client_id}", "data": response.data}

@route_order.get("/client/{client_id}/{order_id}", status_code=status.HTTP_200_OK)
async def get_client_order_by_id(client_id: str, order_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # Le client peut voir les détails d'une de ses commandes
    response = await supabase.table("orders").select("*").eq("id", order_id).eq("client_id", client_id).execute()
    return {"message": "Order details", "data": response.data}


# ==========================================
# ROUTES POUR LES HOTELS
# ==========================================

@route_order.get("/hotel/{hotel_id}", status_code=status.HTTP_200_OK)
async def get_hotel_orders(hotel_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # L'hôtel peut voir toutes les commandes qui lui sont adressées
    response = await supabase.table("orders").select("*").eq("hotel_id", hotel_id).execute()
    return {"message": f"List of orders for hotel {hotel_id}", "data": response.data}

@route_order.get("/hotel/{hotel_id}/{order_id}", status_code=status.HTTP_200_OK)
async def get_hotel_order_by_id(hotel_id: str, order_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # L'hôtel peut voir les détails d'une commande qui lui est adressée
    response = await supabase.table("orders").select("*").eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": "Order details", "data": response.data}

@route_order.put("/hotel/{hotel_id}/{order_id}", status_code=status.HTTP_200_OK)
async def update_hotel_order(hotel_id: str, order_id: str, order: OrderModel, supabase: AsyncClient = Depends(get_supabase_client)):
    # L'hôtel peut mettre à jour le statut d'une de ses commandes
    order_data = order.model_dump()
    order_data["hotel_id"] = hotel_id # Sécurité
    
    response = await supabase.table("orders").update(order_data).eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Order {order_id} updated successfully", "data": response.data}

@route_order.delete("/hotel/{hotel_id}/{order_id}", status_code=status.HTTP_200_OK)
async def delete_hotel_order(hotel_id: str, order_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # L'hôtel peut annuler/supprimer une commande
    response = await supabase.table("orders").delete().eq("id", order_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Order {order_id} deleted successfully", "data": response.data}
>>>>>>> 27fbc16e2fb29f210d333725f27d935b452ab2d1
