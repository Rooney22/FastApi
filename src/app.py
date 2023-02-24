from fastapi import FastAPI
from datetime import datetime
from src.api.base_router import router
from src.db.db import get_session, Session
from fastapi import Depends
from src.models.user import User
from src.services.utils.hash import hash_password
from src.core.settings import settings


def admin_registration() -> None:
    with Session.begin() as session:
        admin_username = settings.admin_username
        admin_password = settings.admin_password
        admin_user = session.query(User).filter_by(username=admin_username).first()

        if not admin_user:
            user = User(
                id=1,
                username=admin_username,
                password_hashed=hash_password(admin_password),
                role='admin',
                created_at=datetime.now(),
                created_by=1,
                modified_at=datetime.now(),
                modified_by=1,
            )
            session.add(user)
            session.commit()


app = FastAPI(
    title="Мое первое приложение FastAPI",
    description="Первое приложение",
    version="0.0.1",
    on_startup=admin_registration()
)



app.include_router(router)
