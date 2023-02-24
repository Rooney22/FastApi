from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from src.models.user import User
from datetime import datetime


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', backref='product/user', foreign_keys=[created_by])
    user1 = relationship('User', backref='product/user1', foreign_keys=[modified_by])
