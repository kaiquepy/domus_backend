
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# --- CONTEXTO DE CRIPTOGRAFIA PARA SENHAS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- DEFINIÇÃO DO ROTEADOR ---
router = APIRouter(prefix='/admin', tags=['admin'])

# --- MODELOS DE DADOS ---
class AdminCreate(BaseModel):
    nome: str  # Nome do administrador
    email: EmailStr  # Validação automática de e-mail
    senha: str  # Senha em texto puro (será hasheada)

class AdminResponse(BaseModel):
    id: int  # ID do administrador
    nome: str
    email: EmailStr
    tipo: str

    class Config:
        from_attributes = True  # Permite leitura de objetos ORM

# --- DEPENDÊNCIA DE AUTORIZAÇÃO (SIMULAÇÃO) ---
async def get_current_admin_user(token: str = "fake-token"):
    # Aqui deveria validar o token e buscar o admin no banco
    print(f"Token recebido e validado (simulação): {token}")
    return {"username": "admin_existente", "tipo": "Administrador"}

# --- ENDPOINT PARA CRIAR ADMINISTRADOR ---
@router.post(
    '/',
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário Administrador",
    description="Cria um novo administrador. Requer autenticação de um administrador já existente."
)
async def create_admin(
    admin_data: AdminCreate,
    current_admin: dict = Depends(get_current_admin_user)  # Autenticação simulada
):
    """
    Cria um novo usuário administrador.
    """
    # 1. Gerar hash da senha
    hashed_password = pwd_context.hash(admin_data.senha)

    # 2. Preparar dados para inserção no banco (simulado)
    new_admin_data_for_db = admin_data.model_dump()
    new_admin_data_for_db.update({
        "hashed_password": hashed_password,
        "tipo": "Administrador"
    })
    del new_admin_data_for_db["senha"]  # Nunca armazene a senha em texto puro

    # 3. Simular criação no banco e retorno do novo admin
    # (Substitua por lógica real de banco de dados)
    return {
        "id": 1,  # Simulação de ID gerado pelo banco
        "nome": admin_data.nome,
        "email": admin_data.email,
        "tipo": "Administrador"
    }
