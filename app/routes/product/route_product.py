from fastapi import APIRouter,Depends,status
from app.config.config_supabase import get_supabase_client
from app.model.product.product_model import ProductModel
from supabase import AsyncClient


route_product = APIRouter(prefix="/product",tags=["product"])



@route_product.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(page: int = 1, supabase: AsyncClient = Depends(get_supabase_client)):
    limit = 20
    start = (page - 1) * limit
    end = start + limit - 1
    
    # On récupère les produits avec une limite de 20 par page
    response = await supabase.table("products").select("*").range(start, end).execute()
    
    return {"message": f"List of products (page {page})", "data": response.data, "page": page, "limit": limit}
    
@route_product.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # On récupère un produit spécifique grâce à son ID
    response = await supabase.table("products").select("*").eq("id", product_id).execute()
    
    return {"message": "Details for product", "data": response.data }

