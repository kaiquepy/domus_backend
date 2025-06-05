from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    tipo: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    tipo: str = "morador"

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str