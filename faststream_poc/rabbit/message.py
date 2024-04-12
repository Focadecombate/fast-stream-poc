
from pydantic import BaseModel


class HealthMessage(BaseModel):
    id: str
    event: str = "Hello World"
