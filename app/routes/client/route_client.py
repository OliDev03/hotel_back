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
    return {
        "message": "Order created successfully",
        "user_id": user_id,
        "client": client.dict()
    }


#  TEST ROUTE
@route_client.get("/test")
async def test():
    return {
        "message": "This is a test endpoint"
    }