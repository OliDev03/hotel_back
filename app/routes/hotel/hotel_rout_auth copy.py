# from fastapi import APIRouter, Depends,HTTPException,status,Response
# from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
# import supabase
# from models.user_supabase import User_supabase
# from config.supabase_client import get_supabase_client
# from dotenv import load_dotenv
# from datetime import datetime,timedelta
# from passlib.context import CryptContext
# from bson import ObjectId
# from cryptography.fernet import Fernet
# from middleware.is_auth import is_authenticate
# import jwt
# import os

# load_dotenv()

# user_supabase_route = APIRouter(
#     prefix="/v1/user"
# )


# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# #hash password
# def get_password_hash(password):
#     return pwd_context.hash(password)

# #verify password
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)


# #create token
# def create_access_token(data:dict, expires_delta:timedelta):
#     to_encode = data.copy()
#     secret_key = os.getenv("SECRET_KEY")
#     algorithm = os.getenv("ALGORITHM")
#     if not secret_key or not algorithm:
#         raise RuntimeError("SECRET_KEY and ALGORITHM environment variables must be set")
#     if expires_delta:
#         expire = datetime.now() + timedelta(minutes=15)
#     else:
#         expire = datetime.now() + timedelta(minutes=15)
#     return jwt.encode(to_encode, secret_key, algorithm=algorithm)

# @user_supabase_route.get("")
# async def user_get(is_auth:dict = Depends(is_authenticate)):
#     return {"message":"supabase route"}

# @user_supabase_route.post("/register")
# async def register(data: User_supabase):
#     supabase =  await get_supabase_client()

#     is_user_exist = await supabase.table("USERS_EMAIL").select("*").eq("email_address", data.email_address).execute()
#     if is_user_exist.data:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="email already registered"
#         )
#     new_user = {
#         "email_address": data.email_address,
#         "password": get_password_hash(data.password),
#         "created_at": datetime.now().isoformat(),
#         "updated_at": datetime.now().isoformat(),
#         "last_sync": datetime.now().isoformat()
#     }
#     result = await supabase.table("USERS_EMAIL").insert(new_user).execute()
#     return {"message": "User registered successfully"}



# @user_supabase_route.post("/connect-email")
# async def email_connect(data: User_supabase, res: Response):
#     supabase = await get_supabase_client()
#     try:
#         is_user_exist = await supabase.table('USERS_EMAIL').select("*").eq("email_address", data.email_address).limit(1).execute()
#         if not is_user_exist.data or len(is_user_exist.data) == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         user = is_user_exist.data[0]
#         if not verify_password(data.password, user['password']):
#             raise HTTPException(status_code=401, detail="Incorrect password")
#         # Créer le token d'authentification
#         access_token_expire = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE", 30)))
#         access_token = create_access_token(data={"userId": str(user['id'])}, expires_delta=access_token_expire)
#         res.set_cookie(key="vellar_tech_auth", value=access_token, httponly=True)
#         # Mettre à jour le champ auth-token dans la table USERS_EMAIL
#         await supabase.table('USERS_EMAIL').update({"auth_tokens": access_token,"sync_status":"connected","last_sync":datetime.now().isoformat()}).eq("id", user['id']).execute()
#         return {"message": "Login successful"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# #
# #   required field : app_password 
# #
# @user_supabase_route.patch("/update_app_password")
# async def update_user(data: dict, is_auth: dict = Depends(is_authenticate)):
#     supabase = await get_supabase_client()
#     try:
#         userId = is_auth['userId']
#         is_user_exist = await supabase.table('USERS_EMAIL').select("*").eq("id", userId).execute()
#         if not is_user_exist.data or len(is_user_exist.data) == 0:
#             raise HTTPException(status_code=404, detail="User not found")
#         new_app_password = data.get('app_password')
#         if not new_app_password:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="champ app_password vide"
#             )
#         encrypted_password = fernet.encrypt(new_app_password.encode()).decode()
#         result = await supabase.table('USERS_EMAIL').update({"app_password": encrypted_password,"updated_at":datetime.now().isoformat()}).eq("id", userId).execute()
#         if result.data and len(result.data) > 0:
#             return {"message": "app password modified"}
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="erreur d'update"
#             )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @user_supabase_route.get("/me")
# async def get_me(is_auth:dict = Depends(is_authenticate)):
#     supabase = await get_supabase_client()
#     try:
#         userId = is_auth['userId']
#         user = await supabase.table("USERS_EMAIL").select("*").eq("id",userId).limit(1).execute()
#         if not user.data:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="user not found"
#             )
#         return user.data[0]
#     except:
#         pass

# @user_supabase_route.get("/logout")
# async def logout(res:Response,is_auth:dict = Depends(is_authenticate)):
#     supabase = await get_supabase_client()
#     try:
#         res.delete_cookie(key="vellar_tech_auth")
#         userId = is_auth['userId']
#         user = await supabase.table("USERS_EMAIL").update({"sync_status":"Deconnected","last_sync":datetime.now().isoformat()}).eq("id",userId).execute()
#         return {"message": "logout successfully"}
#     except:
#         return {"message":"erreur de logout"}