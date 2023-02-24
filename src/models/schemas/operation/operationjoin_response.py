from pydantic import BaseModel
from datetime import datetime
from src.models.schemas.tank.tank_response import TankResponse
from src.models.schemas.product.product_response import ProductResponse


class OperationJoinResponse(BaseModel):
    id: int
    mass: float
    date_start: datetime
    date_end: datetime
    created_at: datetime
    created_by: int
    modified_at: datetime
    modified_by: int
    product: ProductResponse
    tank: TankResponse

    class Config:
        orm_mode = True
