from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User
from domus_backend.schemas import UserCreate, UserPublic, UserUpdate

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


@router.post('/login', response_model=UserPublic)
def admin_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    """
    Endpoint para autenticação de administradores.
    Retorna os dados do admin em caso de sucesso.
    """
    facade = AuthFacade(session)
    admin_user = facade.login_admin(form_data)  # Usa o novo método

    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email, senha ou permissão inválidos",
        )

    return admin_user