from pydantic import BaseModel
from typing import List, Optional


     # Prix unitaire au moment de la commande (optionnel mais recommandé)

class OrderModel(BaseModel):
    hotel_id: str
    total: float
    status: str
    client_id: Optional[str] = None # Rendu optionnel car il est souvent ajouté par le backend via le token
    product_id: str
    quantity: int
    price: float# Liste des produits de la commande
