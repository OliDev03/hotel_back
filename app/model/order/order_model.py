from pydantic import BaseModel

class OrderModel(BaseModel):
    client_at: str
    staus: str
    total: float
    hotel_id: str