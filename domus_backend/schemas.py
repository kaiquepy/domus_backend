from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    tipo: str | None = None

class UserPublic(BaseModel):
    id: int
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    tipo: str = "morador"

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

    class Config:
        from_attributes = True