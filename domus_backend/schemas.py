from pydantic import BaseModel, EmailStr
from datetime import datetime

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


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    tipo: str = "morador"
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

class SolicitacaoUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True


class AvisoBase(BaseModel):
    titulo: str
    conteudo: str

class AvisoCreate(AvisoBase):
    pass

class AvisoPublic(AvisoBase):

    id: int
    data_publicacao: datetime

    class Config:
        from_attributes = True