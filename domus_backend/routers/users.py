# domus_backend/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User
from domus_backend.schemas import UserCreate, UserPublic


router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserPublic])
def get_users(session: Session = Depends(get_session)):
    users = session.query(User).all()
    return users


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # A senha agora é salva diretamente como veio na requisição
    db_user = User(
        nome=user.nome,
        email=user.email,
        password=user.password  # <<< VOLTOU A SALVAR A SENHA EM TEXTO PURO
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user