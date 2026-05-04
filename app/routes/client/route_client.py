from fastapi import APIRouter,Depends,status
from app.model.client.client_model import Client

route_client = APIRouter(prefix="/client",tags=["client"])

@route_client.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(client: Client):
    return {"message":"okay"}


@route_client.get("/test")
async def test():
    return {"message": "This is a test endpoint"}
