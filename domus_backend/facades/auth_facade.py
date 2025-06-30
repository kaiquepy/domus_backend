
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from domus_backend.models import User

class AuthFacade:
    def __init__(self, db_session: Session):
        self.db = db_session

    def login(self, form_data: OAuth2PasswordRequestForm) -> User | None:
        # TODA A LÓGICA DE LOGIN ESTÁ ESCONDIDA AQUI:

        # 1. Encontra o usuário no BD
        user = self.db.query(User).filter(User.email == form_data.username).first()

        # 2. Verifica a senha
        if not user or user.password != form_data.password:
            return None

        return user



