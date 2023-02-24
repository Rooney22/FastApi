from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.models.schemas.product.product_response import ProductResponse
from src.models.schemas.product.product_request import ProductRequest
from src.services.products import ProductsService
from src.services.authorization import get_current_user_data


router = APIRouter(
    prefix='/products',
    tags=['products'],
    dependencies=[Depends(get_current_user_data)]
)


@router.get('/all', response_model=List[ProductResponse], name="Получить все категории")
def get_all(products_service: ProductsService = Depends()):
    return products_service.all()


@router.get('/get/{product_id}', response_model=ProductResponse, name="Получить одну категорию")
def get(product_id: int, products_service: ProductsService = Depends()):
    return get_with_check(product_id, products_service)


def get_with_check(product_id, products_service):
    result = products_service.get(product_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=ProductResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(products_schema: ProductRequest, products_service: ProductsService = Depends(), user_data: List = Depends(get_current_user_data)):
    return products_service.add(products_schema, user_data[0])


@router.put('/{product_id}', response_model=ProductResponse, name="Обновить информацию о категории")
def put(product_id: int, product_schema: ProductRequest, products_service: ProductsService = Depends(), user_data: List = Depends(get_current_user_data)):
    get_with_check(product_id, products_service)
    return products_service.update(product_id, product_schema, user_data[0])


@router.delete('/{product_id}', status_code=status.HTTP_204_NO_CONTENT, name = "Удалить категорию")
def delete(product_id: int, products_service: ProductsService = Depends()):
    get_with_check(product_id, products_service)
    return products_service.delete(product_id)
