from fastapi import Depends
from typing import List
from datetime import datetime
from src.models.schemas.operation.operation_request import OperationRequest
from src.db.db import Session, get_session
from src.models.operation import Operation
from src.models.tank import Tank
from src.models.product import Product
import csv
from io import StringIO
from typing import BinaryIO


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Operation]:
        operations = (
            self.session
            .query(Operation)
            .join(Tank, Tank.id == Operation.tank_id)
            .join(Product, Product.id == Operation.product_id)
            .order_by(
                Operation.id.desc()
            )
            .all()
        )
        return operations

    def get(self, operation_id: int) -> Operation:
        operation = (
            self.session
            .query(Operation)
            .filter(
                Operation.id == operation_id,
            )
            .first()
        )
        return operation

    def add(self, operation_schema: OperationRequest, creator_id: int) -> Operation:
        operation = Operation(**operation_schema.dict())
        operation.created_by = creator_id
        operation.created_at = datetime.utcnow()
        operation.modified_by = creator_id
        operation.modified_at = datetime.utcnow()
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, operation_id: int, operation_schema: OperationRequest, modifier_id: int) -> Operation:
        operation = self.get(operation_id)
        for field, value in operation_schema:
            setattr(operation, field, value)
        operation.modified_by = modifier_id
        operation.modified_at = datetime.utcnow()
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self.get(operation_id)
        self.session.delete(operation)

    def get_operations(self, tank_id) -> List[Operation]:
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id
            )
            .all()
        )
        return operations

    def get_report_list(self, tank_id: int, product_id: int, date_start: datetime, date_end: datetime):
        operations = (
            self.session
            .query(Operation)
            .filter(
                Operation.tank_id == tank_id,
                Operation.product_id == product_id,
                Operation.date_start >= date_start,
                Operation.date_end <= date_end,
            )
            .all()
        )
        return operations
