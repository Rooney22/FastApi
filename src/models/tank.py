from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.models.user import User
from src.models.product import Product
from datetime import datetime


class Tank(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    max_capacity = Column(Float)
    current_capacity = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', backref='tank/user', foreign_keys=[created_by])
    user1 = relationship('User', backref='tank/user1', foreign_keys=[modified_by])
    product = relationship('Product', backref='tank/products', foreign_keys=[product_id])
