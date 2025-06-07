from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User
from domus_backend.schemas import UserCreate, UserPublic, UserUpdate

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

    db_user = User(
        nome=user.nome,
        email=user.email,
        password=user.password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)
):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(db_user)
    session.commit()