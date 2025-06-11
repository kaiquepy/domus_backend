from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import Solicitacao, User
from domus_backend.schemas import SolicitacaoCreate, SolicitacaoPublic

router = APIRouter(prefix='/solicitacoes', tags=['solicitacoes'])


@router.post('/manutencao', response_model=SolicitacaoPublic, status_code=status.HTTP_201_CREATED)
def create_manutencao(
    solicitacao_data: SolicitacaoCreate,
    session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.id == solicitacao_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {solicitacao_data.user_id} not found",
        )

    nova_solicitacao = Solicitacao(
        descricao=solicitacao_data.descricao,
        user_id=solicitacao_data.user_id,
        tipo_solicitacao='manutencao'
    )

    session.add(nova_solicitacao)
    session.commit()
    session.refresh(nova_solicitacao)

    return nova_solicitacao