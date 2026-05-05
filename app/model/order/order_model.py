from pydantic import BaseModel

class OrderModel(BaseModel):
<<<<<<< HEAD
    client_at: str
    staus: str
    total: float
    hotel_id: str
=======
    hotel_id: str
    total: float
    status: str
    client_id: str
>>>>>>> 27fbc16e2fb29f210d333725f27d935b452ab2d1
