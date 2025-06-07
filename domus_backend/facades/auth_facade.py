# domus_backend/facades/auth_facade.py

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from domus_backend.models import User

class AuthFacade:
    def __init__(self, db_session: Session):
        self.db = db_session

    def login(self, form_data: OAuth2PasswordRequestForm) -> User | None:
        """
        Verifica as credenciais para qualquer tipo de usuário.
        Retorna o objeto User completo em caso de sucesso, ou None caso contrário.
        """
        user = self.db.query(User).filter(User.email == form_data.username).first()

        # Verifica se o usuário existe e se a senha está correta
        # (usando a comparação direta que você definiu)
        if not user or user.password != form_data.password:
            return None

        # Se chegou aqui, o login é válido. Retornamos o usuário.
        # A responsabilidade de verificar o "tipo" agora é do cliente.
        return user