

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.facades.auth_facade import AuthFacade
from domus_backend.schemas import UserPublic

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/login', response_model=UserPublic)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    facade = AuthFacade(session)
    user = facade.login(form_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    return user


