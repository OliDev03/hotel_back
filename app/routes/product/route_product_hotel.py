from fastapi import APIRouter, Depends, status
from app.config.config_supabase import get_supabase_client
from app.model.product.product_model import ProductModel
from supabase import AsyncClient

route_product_hotel = APIRouter(prefix="/product_hotel", tags=["product_hotel"])

@route_product_hotel.post("/{hotel_id}", status_code=status.HTTP_201_CREATED)
async def create_product(hotel_id: str, product: ProductModel, supabase: AsyncClient = Depends(get_supabase_client)):
    product_data = product.model_dump()
    # On s'assure que le hotel_id dans les données correspond à celui de l'URL
    product_data["hotel_id"] = hotel_id
    
    response = await supabase.table("products").insert(product_data).execute()
    return {"message": "Product created successfully", "data": response.data}

@route_product_hotel.get("/{hotel_id}", status_code=status.HTTP_200_OK)
async def get_all_products_by_hotel(hotel_id: str, page: int = 1, supabase: AsyncClient = Depends(get_supabase_client)):
    limit = 20
    start = (page - 1) * limit
    end = start + limit - 1
    
    # Récupère les produits associés à ce hotel_id (limité à 20 par page)
    response = await supabase.table("products").select("*").eq("hotel_id", hotel_id).range(start, end).execute()
    
    return {"message": f"List of products for hotel {hotel_id} (page {page})", "data": response.data, "page": page, "limit": limit}
    
@route_product_hotel.get("/{hotel_id}/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(hotel_id: str, product_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # Récupère un produit spécifique uniquement s'il appartient à cet hôtel
    response = await supabase.table("products").select("*").eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": "Details for product", "data": response.data}

@route_product_hotel.put("/{hotel_id}/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(hotel_id: str, product_id: str, product: ProductModel, supabase: AsyncClient = Depends(get_supabase_client)):
    product_data = product.model_dump()
    product_data["hotel_id"] = hotel_id # Sécurité : forcer le hotel_id
    
    # Met à jour uniquement si le produit appartient à l'hôtel
    response = await supabase.table("products").update(product_data).eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Product {product_id} updated successfully", "data": response.data}

@route_product_hotel.delete("/{hotel_id}/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(hotel_id: str, product_id: str, supabase: AsyncClient = Depends(get_supabase_client)):
    # Supprime uniquement si le produit appartient à l'hôtel
    response = await supabase.table("products").delete().eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Product {product_id} deleted successfully", "data": response.data}