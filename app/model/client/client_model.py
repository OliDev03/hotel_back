from pydantic import BaseModel

class Client(BaseModel):
    id: str
    name: str
    created_at: int
    email: str
    address: str
    password: str
    role: str