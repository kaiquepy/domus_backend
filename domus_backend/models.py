from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from domus_backend.database import Base

# Classe que representa um usuário do sistema
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Identificador único do usuário
    nome = Column(String, nullable=False)               # Nome do usuário
    email = Column(String, unique=True, index=True, nullable=False)  # E-mail do usuário (único)
    password = Column(String, nullable=False)           # Senha do usuário
    tipo = Column(String, default='morador')            # Tipo do usuário (ex: morador, administrador)

    solicitacoes = relationship('Solicitacao', back_populates='user')  # Relação com as solicitações feitas pelo usuário

# Classe que representa uma solicitação feita por um usuário
class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)  # Identificador único da solicitação
    tipo_solicitacao = Column(String, nullable=False)   # Tipo da solicitação (ex: manutenção, documento)
    descricao = Column(String, nullable=False)          # Descrição detalhada da solicitação
    status = Column(String, default="Enviado")          # Status atual da solicitação (ex: Enviado, Analisando, Concluído, Negado)
    user_id = Column(Integer, ForeignKey("users.id"))   # Chave estrangeira para o usuário que fez a solicitação

    user = relationship("User", back_populates="solicitacoes")  # Relação com o usuário que fez a solicitação