from fastapi import APIRouter, Depends,HTTPException,status,Response,Request
from app.config.config_supabase import get_supabase_client
from app.model.hotel.hotel_model import HotelModel
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
#from bson import ObjectId
import os
import jwt
from app.middleware.id_authenticate import id_authenticate

hotel_auth_route = APIRouter(
    prefix="/auth/hotel",
    tags=["hotel_auth"]
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expire_delta) -> str:
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    if not secret_key or not algorithm:
        raise ValueError("Missing JWT configuration")
    if expire_delta:
        expiration = datetime.utcnow() + expire_delta
    else:
        expiration = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"exp": expiration, **data}
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)



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
        print(get_password_hash(data.password))
        await supabase.table("user").insert(new_user).execute()
        return {"message":"User registered successfully"}
    except Exception as e:
        print(e)


@hotel_auth_route.post("/login")
async def login_hotel_user(credentials: dict, response: Response):
    try:
        supabase = await get_supabase_client()

        user = (
            await supabase
            .table("user")
            .select("*")
            .eq("mail", credentials["mail"])
            .execute()
        )
        if not user.data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        if not verify_password(
            credentials["password"],
            user.data[0]["password"]
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        access_token_expire = timedelta(
            minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE", 30))
        )
        access_token = create_access_token(
            data={"userId": user.data[0]["id"]},
            expire_delta=access_token_expire
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="None"
        )

        print(access_token)
        return {
            "message": "Login successful",
            "access_token": access_token
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# @hotel_auth_route.post("/login")
# async def login_hotel_user(credentials: dict, response: Response):
#     try:
#         supabase = await get_supabase_client()
#         user = await supabase.table("user").select("*").eq("mail", credentials["mail"]).execute()
#         if not user.data:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
#         if not verify_password(credentials["password"], user.data[0]["password"]):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
#         access_token_expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE", 30)))
#         access_token = create_access_token(data={"userId": user}, expires_delta=access_token_expire)
#         print(access_token)
#         return {"message": "Login successful", "access_token": access_token}
#     except Exception as e:
#         print(e)
    

@hotel_auth_route.post("/logout")
async def logout_hotel_user(response: Response, is_authenticated: dict= Depends(id_authenticate)):
    response.delete_cookie("access_token")
    return {"message": "Logout successful"}


@hotel_auth_route.get("/profile")
async def get_hotel_user_profile(
    request: Request,
    response: Response
):
    try:
        # Récupérer l'user_id via le cookie JWT
        user_id = await id_authenticate(request)

        supabase = await get_supabase_client()

        result = (
            await supabase
            .table("user")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user = result.data[0]

        return {
            "message": "Profile fetched successfully",
            "user": {
                "id": user["id"],
                "mail": user["mail"],
                "name": user["name"],
                "role": user["role"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
        
# @hotel_auth_route.get("/profile")
# async def get_hotel_user_profile(response: Response):
#     # Implement get user profile logic
#     try : 
        
        
#     pass