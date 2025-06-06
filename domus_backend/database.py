from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domus_backend.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

# Esta linha é crucial para criar o "fabricante" de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A 'Base' foi removida daqui, como instruído anteriormente, o que está correto.

def get_session():
    db = SessionLocal()  # Usamos o SessionLocal() para criar uma nova sessão
    try:
        yield db
    finally:
        db.close()