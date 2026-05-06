from fastapi import APIRouter, Depends, status
from app.config.config_supabase import get_supabase_client
from app.model.product.product_model import ProductModel
from supabase import AsyncClient
from app.middleware.id_authenticate import id_authenticate

route_product_hotel = APIRouter(prefix="/product_hotel", tags=["product_hotel"])

@route_product_hotel.post("/new_product", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductModel, is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Crée un nouveau produit pour un hôtel spécifique.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        product (ProductModel): Les données du produit à créer, validées par Pydantic.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message de confirmation et les données du produit créé.
    """
    hotel_id = is_auth["user_id"]
    product_data = product.model_dump()
    # On s'assure que le hotel_id dans les données correspond à celui de l'URL
    product_data["hotel_id"] = hotel_id
    
    response = await supabase.table("products").insert(product_data).execute()
    return {"message": "Product created successfully", "data": response.data}

@route_product_hotel.get("/all_product", status_code=status.HTTP_200_OK)
async def get_all_products_by_hotel(is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Récupère tous les produits d'un hôtel spécifique avec un système de pagination.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        page (int, optional): Le numéro de la page à récupérer (défaut à 1).
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message, la liste des produits pour la page demandée, le numéro de page et la limite par page.
    """
    hotel_id = is_auth["user_id"]
    # page = request.query_params.get("page", 1)
    # limit = 20
    # start = (page - 1) * limit
    # end = start + limit - 1
    
    # Récupère les produits associés à ce hotel_id (limité à 20 par page)
    response = await supabase.table("products").select("*").eq("hotel_id", hotel_id).execute()
    
    return {"message": f"List of products for hotel {hotel_id}", "data": response.data}
    
@route_product_hotel.get("/get/product", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: str,is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Récupère les détails d'un produit spécifique appartenant à un hôtel.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        product_id (str): L'identifiant unique du produit.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Les détails du produit demandé.
    """
    hotel_id = is_auth["user_id"]
    # Récupère un produit spécifique uniquement s'il appartient à cet hôtel
    response = await supabase.table("products").select("*").eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": "Details for product", "data": response.data}

@route_product_hotel.put("/update/product", status_code=status.HTTP_200_OK)
async def update_product(product_id: str,is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Met à jour les informations d'un produit existant pour un hôtel spécifique.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        product_id (str): L'identifiant unique du produit à mettre à jour.
        product (ProductModel): Les nouvelles données du produit.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message de confirmation et les données du produit mis à jour.
    """
    
    hotel_id = is_auth["user_id"]
    product_data = product_id.model_dump()
    product_data["hotel_id"] = hotel_id # Sécurité : forcer le hotel_id
    
    # Met à jour uniquement si le produit appartient à l'hôtel
    response = await supabase.table("products").update(product_data).eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Product {product_id} updated successfully", "data": response.data}

@route_product_hotel.delete("/delete/product", status_code=status.HTTP_200_OK)
async def delete_product(product_id: str,is_auth: dict = Depends(id_authenticate), supabase: AsyncClient = Depends(get_supabase_client)):
    """
    Supprime un produit spécifique appartenant à un hôtel.
    
    Args:
        hotel_id (str): L'identifiant unique de l'hôtel.
        product_id (str): L'identifiant unique du produit à supprimer.
        supabase (AsyncClient): Le client de base de données Supabase.
        
    Returns:
        dict: Un message confirmant la suppression du produit.
    """
    hotel_id = is_auth["user_id"]
    # Supprime uniquement si le produit appartient à l'hôtel
    response = await supabase.table("products").delete().eq("id", product_id).eq("hotel_id", hotel_id).execute()
    return {"message": f"Product {product_id} deleted successfully", "data": response.data}