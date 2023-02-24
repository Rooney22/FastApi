from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
from datetime import datetime
from src.models.schemas.operation.operation_response import OperationResponse
from src.models.schemas.operation.operationjoin_response import OperationJoinResponse
from src.models.schemas.operation.operation_request import OperationRequest
from src.services.operations import OperationsService
from src.services.tanks import TanksService
from src.services.authorization import get_current_user_data


router = APIRouter(
    prefix='/operations',
    tags=['operations'],
    dependencies=[Depends(get_current_user_data)]
)


@router.get('/all', response_model=List[OperationJoinResponse], name="Получить все категории")
def get_all(operations_service: OperationsService = Depends()):
    return operations_service.all()


@router.get('/get/{operation_id}', response_model=OperationResponse, name="Получить одну категорию")
def get(operation_id: int, operations_service: OperationsService = Depends()):
    return get_with_check(operation_id, operations_service)


def get_with_check(operation_id, operation_service):
    result = operation_service.get(operation_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return result


@router.post('/', response_model=OperationResponse, status_code=status.HTTP_201_CREATED, name="Добавить категорию")
def add(operations_schema: OperationRequest, operations_service: OperationsService = Depends(), user_data: List = Depends(get_current_user_data)):
    return operations_service.add(operations_schema, user_data[0])


@router.put('/{operation_id}', response_model=OperationResponse, name="Обновить информацию о категории")
def put(operation_id: int, operations_schema: OperationRequest, operations_service: OperationsService = Depends(), user_data: List = Depends(get_current_user_data)):
    get_with_check(operation_id, operations_service)
    return operations_service.update(operation_id, operations_schema, user_data[0])


@router.delete('/{operation_id}', status_code=status.HTTP_204_NO_CONTENT, name = "Удалить категорию")
def delete(operation_id: int, operations_service: OperationsService = Depends()):
    get_with_check(operation_id, operations_service)
    return operations_service.delete(operation_id)


@router.get('/{tank_id}', response_model=List[OperationResponse], name="Получить все операции по резервуару")
def get_operations(tank_id: int, operations_service: OperationsService = Depends(), tanks_service: TanksService = Depends()):
    get_with_check(tank_id, tanks_service)
    return operations_service.get_operations(tank_id)


@router.get('/download/{tank_id}', name='Создать отчёт по параметрам')
def get_report(tank_id: int, product_id: int, date_start: datetime, date_end: datetime, operations_service: OperationsService = Depends()):
    report = operations_service.get_report(tank_id, product_id, date_start, date_end)
    return StreamingResponse(report, media_type='text/csv',
                             headers={"Content-Disposition": "attachment; filename=report.csv"})
