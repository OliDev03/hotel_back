from pydantic import BaseModel

class HotelModel(BaseModel):
    id: str 
    name: str
    mail: str
    created_at: int
    password: str
    role: str
    address: str