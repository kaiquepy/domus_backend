from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User, Aviso

from domus_backend.schemas import (
    UserCreate,
    UserPublic,
    UserUpdate,
    AvisoCreate, # <-- Add this
    AvisoPublic  # <-- Add this
)

router = APIRouter(prefix='/admin', tags=['admin'])


@router.post('/', response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_admin(user_data: UserCreate, session: Session = Depends(get_session)):
    if session.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    db_admin = User(
        nome=user_data.nome,
        email=user_data.email,
        password=user_data.password,
        tipo='admin',
    )
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


@router.get('/', response_model=list[UserPublic])
def get_admins(session: Session = Depends(get_session)):
    admins = session.query(User).filter(User.tipo == 'admin').all()
    return admins


@router.put('/{admin_id}', response_model=UserPublic)
def update_admin(
    admin_id: int, user_update: UserUpdate, session: Session = Depends(get_session)
):
    db_admin = session.query(User).filter(User.id == admin_id, User.tipo == 'admin').first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin user not found")

    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_admin, key, value)
    
    session.add(db_admin)
    session.commit()
    session.refresh(db_admin)
    return db_admin


@router.delete('/{admin_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, session: Session = Depends(get_session)):
    db_admin = session.query(User).filter(User.id == admin_id, User.tipo == 'admin').first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin user not found")
    
    session.delete(db_admin)
    session.commit()


@router.patch('/promote/{user_id}', response_model=UserPublic)
def promote_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.tipo == 'admin':
        raise HTTPException(status_code=400, detail="User is already an admin")

    db_user.tipo = 'admin'
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post('/avisos/', response_model=AvisoPublic, status_code=status.HTTP_201_CREATED)
def create_aviso(
    aviso_data: AvisoCreate,
    session: Session = Depends(get_session)

):

    novo_aviso = Aviso(
        titulo=aviso_data.titulo,
        conteudo=aviso_data.conteudo
    )
    session.add(novo_aviso)
    session.commit()
    session.refresh(novo_aviso)
    return novo_aviso


@router.delete('/avisos/{aviso_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_aviso(aviso_id: int, session: Session = Depends(get_session)):

    db_aviso = session.query(Aviso).filter(Aviso.id == aviso_id).first()

    if not db_aviso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aviso not found"
        )

    session.delete(db_aviso)
    session.commit()

    return