from fastapi import HTTPException
from app.config.config_supabase import get_supabase_client
from fastapi import APIRouter, Depends, status
from app.model.product.product_model import Product
from app.middleware.id_authenticate import id_authenticate


route_product = APIRouter(prefix="/product", tags=["product"])
##client##
@route_product.get("/")
async def get_product(page: int = 1, limit: int = 20,is_authenticated: dict= Depends(id_authenticate),):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "client":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        start = (page - 1) * limit
        end = start + limit - 1
        result=supabase.table("product").select("*").range(start,end).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {
            "message": "Product data received (public access)",
            "data": result.data[start:end],
            "page": page,
            "limit": limit,
            "total": len(result.data)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@route_product.get("/getbyid")
async def get_product_by_id(product_id: int,is_authenticated: dict= Depends(id_authenticate),):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "client" and user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        result=supabase.table("product").select("*").eq("id",product_id).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {
            "message": "Product data received (public access)",
            "data": result.data[0],
            
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )




##hotel
@route_product.get("/hotel/product")
async def get_product(page: int = 1, limit: int = 20,is_authenticated: dict= Depends(id_authenticate),):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        start = (page - 1) * limit
        end = start + limit - 1
        result=supabase.table("product").select("*").eq("hotel_id",user.data[0]["id"]).range(start,end).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {
            "message": "Product data received (public access)",
            "data": result.data[start:end],
            "page": page,
            "limit": limit,
            "total": len(result.data)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

##hotel##
@route_product.post("/create")
async def create_product(product: Product,is_authenticated: dict= Depends(id_authenticate),):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user=supabase.table("user").select("*").eq("id",user_id).execute()
        if user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not authorized to perform this action"
            )
        result=supabase.table("product").insert(product.dict()).execute()
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {
            "message": "Product created successfully",
            "data": result.data
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@route_product.put("/update")
async def update_product(
    product_id: int,
    product_update: Product,
    is_authenticated: dict= Depends(id_authenticate)
):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user = await supabase.table("user").select("role").eq("id", user_id).execute()
        if not user.data or user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )

        # Vérifier si le produit existe et appartient à l'hôtel
        existing_product = await supabase.table("product") \
            .select("id, hotel_id") \
            .eq("id", product_id) \
            .eq("hotel_id", user_id) \
            .execute()
        if product_update.hotel_id != existing_product.data[0]["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
        if not existing_product.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or you don't have access to it"
            )

        # Mettre à jour le produit
        response = await supabase.table("product") \
            .update(product_update.dict(exclude_unset=True)) \
            .eq("id", product_id) \
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        return {
            "message": "Product updated successfully",
            "data": response.data[0]
        }

    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@route_product.delete("/delete")
async def delete_product(
    product_id: int,
    is_authenticated: dict= Depends(id_authenticate)
):
    try:
        supabase = await get_supabase_client()
        user_id = is_authenticated["userId"]
        user = await supabase.table("user").select("role").eq("id", user_id).execute()
        if not user.data or user.data[0]["role"] != "hotel":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
        existing_product = await supabase.table("product") \
            .select("id, hotel_id") \
            .eq("id", product_id) \
            .eq("hotel_id", user_id) \
            .execute()
        if not existing_product.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found or you don't have access to it"
            )
        if product_id != existing_product.data[0]["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to perform this action"
            )
        response = await supabase.table("product") \
            .delete() \
            .eq("id", product_id) \
            .execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return {
            "message": "Product deleted successfully",
            "data": response.data[0]
        }
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
