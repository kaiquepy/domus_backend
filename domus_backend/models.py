# domus_backend/models.py

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from domus_backend.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    tipo = Column(String, default='morador')
    bloco = Column(String, nullable=True)
    apartamento = Column(String, nullable=True)
    curso = Column(String, nullable=True)
    matricula = Column(String, nullable=True, unique=True)
    ano_de_entrada = Column(Integer, nullable=True)

    solicitacoes = relationship('Solicitacao', back_populates='user')
    consultas = relationship('Consulta', back_populates='usuario')

class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo_solicitacao = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(String, default="Enviado")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="solicitacoes")

class Aviso(Base):
    __tablename__ = "avisos"

    id = Column(Integer, primary_key=True, index=True)
    tipo_solicitacao = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    status = Column(String, default="Enviado")
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="solicitacoes")

class Aviso(Base):
    __tablename__ = "avisos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    data_publicacao = Column(
        DateTime(timezone=True), server_default=func.now()
    )

class Consulta(Base):
    __tablename__ = 'consultas'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    horario = Column(DateTime, unique=True, nullable=False)
    usuario = relationship('User', back_populates='consultas')

class Indisponibilidade(Base):
    __tablename__ = 'indisponibilidades'

    id = Column(Integer, primary_key=True, index=True)
    horario_inicio = Column(DateTime, nullable=False)
    horario_fim = Column(DateTime, nullable=False)
    motivo = Column(String, nullable=True)