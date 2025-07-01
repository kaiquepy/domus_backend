from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- UserUpdate ---
# Schema para atualizar um usuário. Todos os campos são opcionais.
class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    tipo: str | None = None
    # --- NOVOS ATRIBUTOS ---
    bloco: str | None = None
    apartamento: str | None = None
    curso: str | None = None
    matricula: str | None = None
    ano_de_entrada: int | None = None

# --- UserPublic ---
# O que a API retorna como dados públicos de um usuário.
class UserPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str
    # --- NOVOS ATRIBUTOS ---
    bloco: str | None = None
    apartamento: str | None = None
    curso: str | None = None
    matricula: str | None = None
    ano_de_entrada: int | None = None

    class Config:
        from_attributes = True


# --- UserCreate ---
# O que a API espera receber para criar um novo usuário.
class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    # O tipo tem um valor padrão, então não precisa ser enviado
    tipo: str = "morador"
    # --- NOVOS ATRIBUTOS (opcionais na criação) ---
    bloco: str | None = None
    apartamento: str | None = None
    curso: str | None = None
    matricula: str | None = None
    ano_de_entrada: int | None = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class SolicitacaoCreate(BaseModel):
    user_id: int
    descricao: str


class SolicitacaoPublic(BaseModel):
    id: int
    tipo_solicitacao: str
    descricao: str
    status: str
    user_id: int

    # Adicione esta classe interna
    class Config:
        from_attributes = True

class SolicitacaoUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True

# --- NOVOS SCHEMAS PARA CONSULTAS ---

# O que um usuário envia para agendar uma consulta
class ConsultaCreate(BaseModel):
    user_id: int
    horario: datetime # Ex: "2025-07-25T10:00:00"

# O que a API retorna como dados públicos de uma consulta
class ConsultaPublic(BaseModel):
    id: int
    user_id: int
    horario: datetime

    class Config:
        from_attributes = True

# O que o admin envia para bloquear um período
class IndisponibilidadeCreate(BaseModel):
    horario_inicio: datetime
    horario_fim: datetime
    motivo: str | None = None