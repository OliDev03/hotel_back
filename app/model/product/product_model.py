from pydantic import BaseModel

class ProductModel(BaseModel):
    hotel_id: str
    name: str
    description: str
    price: float
    image: str
    category: str