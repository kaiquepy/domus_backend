# domus_backend/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User
from domus_backend.schemas import UserCreate, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/', response_model=list[UserPublic])
def get_users(session: Session = Depends(get_session)):
    """
    Lista todos os usuários. (Em um app real, isso também seria protegido).
    """
    users = session.query(User).all()
    return users


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """
    Cria um novo usuário (morador) com os dados completos.
    """
    if session.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    if user.matricula and session.query(User).filter(User.matricula == user.matricula).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Matricula already registered",
        )

    db_user = User(
        nome=user.nome,
        email=user.email,
        password=user.password,
        tipo='morador',
        bloco=user.bloco,
        apartamento=user.apartamento,
        curso=user.curso,
        matricula=user.matricula,
        ano_de_entrada=user.ano_de_entrada
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

