from fastapi import FastAPI

from domus_backend.routers import auth
from domus_backend.routers import admin  # Adicionado import do admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)  # Inclui o roteador de admin

@app.get('/')
def read_root():
    return {'Message': 'Olá Mundo!'}  # Corrigido para português conforme teste
