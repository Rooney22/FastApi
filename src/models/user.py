from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.models.base import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    created_by = Column(Integer, ForeignKey('users.id'), index=True)
    modified_at = Column(DateTime)
    modified_by = Column(Integer, ForeignKey('users.id'), index=True)
