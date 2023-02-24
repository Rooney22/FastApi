from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.tank.tank_response import TankResponse
from src.models.schemas.tank.tank_request import TankRequest
from src.services.tanks import TanksService
from src.services.authorization import get_current_user_data


router = APIRouter(
    prefix='/tanks',
    tags=['tanks'],
    dependencies=[Depends(get_current_user_data)],
)


@router.get('/all', response_model=List[TankResponse], name="Получить все категории")
def get_all(tanks_service: TanksService = Depends()):
    return tanks_service.all()


@router.get('/get/{tank_id}', response_model=TankResponse, name="Получить одну категорию")
def get(tank_id: int, tanks_service: TanksService = Depends()):
    return get_with_check(tank_id, tanks_service)


def get_with_check(tank_id, tanks_service):
    result = tanks_service.get(tank_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=TankResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(tanks_schema: TankRequest, tanks_service: TanksService = Depends(), user_data: List = Depends(get_current_user_data)):
    return tanks_service.add(tanks_schema, user_data[0])


@router.put('/{tank_id}', response_model=TankResponse, name="Обновить информацию о категории")
def put(tank_id: int, tank_schema: TankRequest, tanks_service: TanksService = Depends(), user_data: List = Depends(get_current_user_data)):
    get_with_check(tank_id, tanks_service)
    return tanks_service.update(tank_id, tank_schema, user_data[0])


@router.delete('/{tank_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(tank_id: int, tanks_service: TanksService = Depends()):
    get_with_check(tank_id, tanks_service)
    return tanks_service.delete(tank_id)


@router.get('/{tank_id, new_capacity}', response_model=TankResponse, name="Обновить значение capacity")
def new_capacity(tank_id: int, new_capacity: float, tanks_service: TanksService = Depends()):
    tank = get_with_check(tank_id, tanks_service)
    tank.current_capacity = new_capacity
    return tank
