# from fastapi import APIRouter,Depends,status
# from app.model.client.client_model import Client

# route_client = APIRouter(prefix="/client",tags=["client"])

# @route_client.post("/", status_code=status.HTTP_201_CREATED)
# async def create_client(client: Client):
#     return {"message":"okay"}



# @route_client.get("/test")
#async def test():
#     return {"message": "This is a test endpoint"}
from fastapi import HTTPException
from fastapi import APIRouter, Depends, status
from app.model.client.client_model import Client
from app.middleware.id_authenticate import id_authenticate
from app.config.config_supabase import get_supabase_client
from app.model.product.product_model import Product


route_client = APIRouter(prefix="/client", tags=["client"])

#  PUBLIC 
@route_client.put("/modify", status_code=status.HTTP_201_CREATED)
async def modify_infos(new_user: Client,is_authenticated: dict= Depends(id_authenticate),):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user =supabase.table("client").select("*").eq("id", user_id).execute()
        if not user.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user.data[0]["role"] != "client":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
        if new_user.id != user.data[0]["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
        
        response=await supabase.table("user").update(new_user).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return {
            "message": "User modified successfully",
            "user": response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


#   seulement utilisateur connecté
@route_client.post("/order")
async def create_order(
    client: Client,
    product: Product,
    quantity: int,
    is_authenticated: dict = Depends(id_authenticate)
    
    
    ):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "client":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        new_order={
            "name":client.name,
            "mail":client.mail,
            "hotel_id":product.hotel_id,
            "product_id":product.id,
            "user_id":is_authenticated,
            "status":product.status,
            "totale":product.price*quantity
        }
        result=supabase.table("order").insert(new_order).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return {
            "message": "Order created successfully",
            "order": result.data[0]
    }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@route_client.delete("/self")
async def delete_client(id: str, is_authenticated: dict= Depends(id_authenticate)):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "client" and user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        result=supabase.table("user").delete().eq("id", user_id).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return {
            "message": "Client deleted successfully",
            "client": result.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )