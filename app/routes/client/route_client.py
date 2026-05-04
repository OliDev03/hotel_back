from fastapi import APIRouter,Depends,status
from app.config.config_supabase import get_supabase_client
from app.model.client.client_model import Client
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt
route_client = APIRouter(prefix="/client",tags=["client"])

@route_client.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(client: Client):
    return {"message":"okay"}


@route_client.get("/test")
async def test():
    return {"message": "This is a test endpoint"}
