from fastapi import Depends
from typing import List
from datetime import datetime
from src.models.schemas.user.user_request import UserRequest
from src.db.db import Session, get_session
from src.models.user import User


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[User]:
        users = (
            self.session
            .query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )
        return users

    def get(self, user_id: int) -> User:
        user = (
            self.session
            .query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )
        return user

    def add(self, user_schema: UserRequest, creator_id: int) -> User:
        user = User(**user_schema.dict())
        user.created_by = creator_id
        user.created_at = datetime.utcnow()
        user.modified_by = creator_id
        user.modified_at = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_id: int, user_schema: UserRequest, modifier_id: int) -> User:
        user = self.get(user_id)
        for field, value in user_schema:
            setattr(user, field, value)
        user.modified_by = modifier_id
        user.modified_at = datetime.utcnow()
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.session.delete(user)
