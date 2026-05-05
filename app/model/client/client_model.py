from pydantic import BaseModel

class Client(BaseModel):
    name: str
    email: str
    password: str
    role: str
    address: str