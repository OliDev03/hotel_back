from pydantic import BaseModel

class OrderModel(BaseModel):
    hotel_id: str
    total: float
    status: str
    client_id: str
