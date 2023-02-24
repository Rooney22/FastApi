from typing import Optional
from pydantic import BaseModel


class TankRequest(BaseModel):
    name: str
    max_capacity: Optional[float]
    current_capacity: Optional[float]
    product_id: Optional[int]




