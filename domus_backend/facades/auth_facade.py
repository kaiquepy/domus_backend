# domus_backend/facades/auth_facade.py

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from domus_backend.models import User

class AuthFacade:
    def __init__(self, db_session: Session):
        self.db = db_session

    def login(self, form_data: OAuth2PasswordRequestForm) -> User | None:
        """Verifica as credenciais para um usuário comum."""
        user = self.db.query(User).filter(User.email == form_data.username).first()

        # Compara a senha do formulário diretamente com a senha do banco
        if not user or user.password != form_data.password:
            return None

        return user

    # --- MÉTODO NOVO PARA O LOGIN DE ADMIN ---
    def login_admin(self, form_data: OAuth2PasswordRequestForm) -> User | None:
        """
        Verifica as credenciais e o tipo do usuário para o login de admin.
        """
        user = self.db.query(User).filter(User.email == form_data.username).first()

        # 1. Verifica se o usuário existe e a senha está correta
        if not user or user.password != form_data.password:
            return None

        # 2. VERIFICAÇÃO EXTRA: Garante que o usuário é um administrador
        if user.tipo != 'admin':
            return None  # Retorna None se um usuário comum tentar logar aqui

        # 3. Se tudo estiver certo, retorna o objeto do usuário admin
        return user