from fastapi import FastAPI

from domus_backend.routers import auth, users, admin, solicitacoes
from domus_backend.database import engine
from domus_backend.db.base_class import Base

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(solicitacoes.router)


@app.get('/')
def read_root():
    return {'Message': 'Hello World'}
