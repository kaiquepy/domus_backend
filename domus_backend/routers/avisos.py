# domus_backend/routers/avisos.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from domus_backend.database import get_session
from domus_backend.models import Aviso
from domus_backend.schemas import AvisoPublic

router = APIRouter(prefix='/avisos', tags=['avisos'])

@router.get('/', response_model=List[AvisoPublic])
def get_avisos(session: Session = Depends(get_session)):

    avisos = session.query(Aviso).order_by(Aviso.data_publicacao.desc()).all()
    return avisos