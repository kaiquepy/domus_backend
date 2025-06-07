# domus_backend/facades/auth_facade.py

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from domus_backend.models import User


# from domus_backend.security import verify_password <<< REMOVA ESTE IMPORT

class AuthFacade:
    def __init__(self, db_session: Session):
        self.db = db_session

    def login(self, form_data: OAuth2PasswordRequestForm) -> User | None:
        """
        Verifica as credenciais do usuário comparando texto puro.
        """
        user = self.db.query(User).filter(User.email == form_data.username).first()

        # Se usuário não existe, retorna None
        if not user:
            return None

        # --- LÓGICA DE COMPARAÇÃO ALTERADA ---
        # Compara a senha do formulário diretamente com a senha do banco
        if user.password != form_data.password:
            return None

        return user