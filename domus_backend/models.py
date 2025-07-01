# domus_backend/models.py

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from domus_backend.db.base_class import Base

# Classe que representa um usuário do sistema
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    tipo = Column(String, default='morador')

    # --- NOVOS ATRIBUTOS ---
    bloco = Column(String, nullable=True)          # Ex: "A", "B", etc.
    apartamento = Column(String, nullable=True)   # Ex: "101", "204"
    curso = Column(String, nullable=True)         # Ex: "Engenharia de Software"
    matricula = Column(String, nullable=True, unique=True) # Matrícula do aluno
    ano_de_entrada = Column(Integer, nullable=True) # Ex: 2023

    solicitacoes = relationship('Solicitacao', back_populates='user')
    consultas = relationship('Consulta', back_populates='usuario')

# Classe que representa uma solicitação feita por um usuário
class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id = Column(Integer, primary_key=True, index=True)  # Identificador único da solicitação
    tipo_solicitacao = Column(String, nullable=False)   # Tipo da solicitação (ex: manutenção, documento)
    descricao = Column(String, nullable=False)          # Descrição detalhada da solicitação
    status = Column(String, default="Enviado")          # Status atual da solicitação (ex: Enviado, Analisando, Concluído, Negado)
    user_id = Column(Integer, ForeignKey("users.id"))   # Chave estrangeira para o usuário que fez a solicitação

    user = relationship("User", back_populates="solicitacoes")  # Relação com o usuário que fez a solicitação

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