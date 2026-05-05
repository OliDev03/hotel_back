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