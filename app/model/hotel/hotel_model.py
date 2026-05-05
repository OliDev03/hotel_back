from pydantic import BaseModel

class HotelModel(BaseModel):
    name:str
    mail: str
    password:str
    adress:str
    phone:str