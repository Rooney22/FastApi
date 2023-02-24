from fastapi import APIRouter

from src.api import tanks
from src.api import users
from src.api import authorization
from src.api import operaions
from src.api import products


router = APIRouter()
router.include_router(tanks.router)
router.include_router(users.router)
router.include_router(authorization.router)
router.include_router(operaions.router)
router.include_router(products.router)
