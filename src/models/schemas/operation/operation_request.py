from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OperationRequest(BaseModel):
    mass: float
    date_start: Optional[datetime]
    date_end: Optional[datetime]
    tank_id: Optional[int]
    product_id: Optional[int]
