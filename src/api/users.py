from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.user.user_response import UserResponse
from src.models.schemas.user.user_request import UserRequest
from src.services.users import UsersService
from src.services.authorization import get_current_user_data
from src.models.schemas.utils.rolechecker import RoleChecker

allower = RoleChecker(["admin"])
router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(allower)],
)
@router.get('/all', response_model=List[UserResponse], name="Получить все категории")
def get_all(users_service: UsersService = Depends()):
    return users_service.all()


@router.get('/get/{user_id}', response_model=UserResponse, name="Получить одну категорию")
def get(user_id: int, users_service: UsersService = Depends()):
    return get_with_check(user_id, users_service)


def get_with_check(user_id, users_service):
    result = users_service.get(user_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(user_schema: UserRequest, users_service: UsersService = Depends(), user_data: List = Depends(get_current_user_data)):
    return users_service.add(user_schema, user_data[0])


@router.put('/{user_id}', response_model=UserResponse, name="Обновить информацию о категории")
def put(user_id: int, user_schema: UserRequest, users_service: UsersService = Depends(), user_data: List = Depends(get_current_user_data)):
    get_with_check(user_id, users_service)
    return users_service.update(user_id, user_schema, user_data[0])


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, name="Удалить категорию")
def delete(user_id: int, users_service: UsersService = Depends()):
    get_with_check(user_id, users_service)
    return users_service.delete(user_id)
