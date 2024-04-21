from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select

from config import get_session
from core.models.user import User
from core.schemas.user import UserOutput

security = HTTPBasic()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session: Session = Depends(get_session),
) -> UserOutput:
    statement = select(User).where(User.username == credentials.username)
    user = session.exec(statement).first()

    if user and user.verify_password(credentials.password):
        return UserOutput.model_validate(user)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
    )
