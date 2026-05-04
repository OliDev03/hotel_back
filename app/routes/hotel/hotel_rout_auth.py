from fastapi import APIRouter, Depends,HTTPException,status,Response
from app.config.config_supabase import get_supabase_client
from app.model.hotel.hotel_model import HotelModel
from passlib.context import CryptContext

hotel_auth_route = APIRouter(
    prefix="/auth/hotel",
    tags=["hotel_auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@hotel_auth_route.post("/register")
async def register_hotel_user(data:HotelModel):
    try:
        supabase = await get_supabase_client()
        new_user={
            "name":data.name,
            "mail": data.mail,
            "password": get_password_hash(data.password),
            "role": data.role
        }
        await supabase.table("user").insert(new_user).execute()
        return {"message":"User registered successfully"}
    except Exception as e:
        print(e)

@hotel_auth_route.post("/login")
async def login_hotel_user(credentials: dict, response: Response):
    # Implement login logic
    pass



@hotel_auth_route.post("/logout")
async def logout_hotel_user(response: Response):
    # Implement logout logic
    pass


@hotel_auth_route.get("/profile")
async def get_hotel_user_profile(response: Response):
    # Implement get user profile logic
    pass