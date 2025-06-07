# domus_backend/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# Supondo que você criou os arquivos como instruído anteriormente
from domus_backend.database import get_session
from domus_backend.facades.auth_facade import AuthFacade
from domus_backend.schemas import UserPublic

router = APIRouter(prefix='/auth', tags=['auth'])


# Esta linha define a rota que você está tentando acessar.
# O caminho é '/login' e o método é POST.
@router.post('/login', response_model=UserPublic)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """
    Endpoint de login que retorna 200 em sucesso ou 401 em falha.
    """
    # Se você removeu a segurança, o facade faz a comparação direta.
    # Se manteve a segurança, ele verifica o hash da senha.
    facade = AuthFacade(session)
    user = facade.login(form_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    return user


