from pydantic import BaseModel

class HotelModel(BaseModel):
    name:str
    mail: str
    password:str
    role:str