from fastapi import Depends
from typing import List
from datetime import datetime
from src.models.schemas.product.product_request import ProductRequest
from src.db.db import Session, get_session
from src.models.product import Product


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Product]:
        products = (
            self.session
            .query(Product)
            .order_by(
                Product.id.desc()
            )
            .all()
        )
        return products

    def get(self, product_id: int) -> Product:
        product = (
            self.session
            .query(Product)
            .filter(
                Product.id == product_id,
            )
            .first()
        )
        return product

    def add(self, product_schema: ProductRequest, creator_id: int) -> Product:
        product = Product(**product_schema.dict())
        product.created_by = creator_id
        product.created_at = datetime.utcnow()
        product.modified_by = creator_id
        product.modified_at = datetime.utcnow()
        self.session.add(product)
        self.session.commit()
        return product

    def update(self, product_id: int, product_schema: ProductRequest, modifier_id: int) -> Product:
        product = self.get(product_id)
        for field, value in product_schema:
            setattr(product, field, value)
        product.modified_by = modifier_id
        product.modified_at = datetime.utcnow()
        self.session.commit()
        return product

    def delete(self, product_id: int):
        product = self.get(product_id)
        self.session.delete(product)
