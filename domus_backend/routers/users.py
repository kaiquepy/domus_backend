from fastAPI import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import User
from domus_backend.schemas import UserCreate, UserResponse

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    db_user = User(
        nome=user.username, email=user.email, password=user.password, tipo=user.tipo
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user