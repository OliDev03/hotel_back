from pydantic import BaseModel

class Client(BaseModel):
<<<<<<< HEAD
    id: str
=======
>>>>>>> 27fbc16e2fb29f210d333725f27d935b452ab2d1
    name: str
    created_at: int
    email: str
<<<<<<< HEAD
    address: str
    password: str
    role: str
=======
    password: str
    role: str
    address: str
>>>>>>> 27fbc16e2fb29f210d333725f27d935b452ab2d1
