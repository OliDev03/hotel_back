from pydantic import BaseModel

class HotelModel(BaseModel):
    id: str 
    name: str
    mail: str
<<<<<<< HEAD
    created_at: int
    password: str
    role: str
    address: str
=======
    password:str
    adress:str
    phone:str
>>>>>>> 27fbc16e2fb29f210d333725f27d935b452ab2d1
