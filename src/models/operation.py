from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.models.user import User
from src.models.tank import Tank
from src.models.product import Product
from datetime import datetime

class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    mass = Column(Float)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    tank_id = Column(Integer, ForeignKey('tanks.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)
    user1 = relationship('User', backref='operation/user1', foreign_keys=[modified_by])
    user2 = relationship('User', backref='operation/user2', foreign_keys=[created_by])
    product = relationship('Product', backref='operation/products', foreign_keys=[product_id])
    tank = relationship('Tank', backref='operation/tanks', foreign_keys=[tank_id])
