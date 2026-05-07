# pyrefly: ignore [missing-type-stubs]
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

class Client(BaseModel):
    name: str
    email: str
    password: str
    role: str
    address: str