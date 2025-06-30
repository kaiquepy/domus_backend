from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import Solicitacao, User
from domus_backend.schemas import SolicitacaoCreate, SolicitacaoPublic, SolicitacaoUpdate

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
        tipo_solicitacao='manutencao',
    )

    session.add(nova_solicitacao)
    session.commit()
    session.refresh(nova_solicitacao)

    return nova_solicitacao


@router.get('/', response_model=list[SolicitacaoPublic])
def get_solicitacoes(
    session: Session = Depends(get_session),
    user_id: int | None = None
):
    query = session.query(Solicitacao)
    if user_id:
        query = query.filter(Solicitacao.user_id == user_id)
    
    return query.all()


@router.patch('/{solicitacao_id}/status', response_model=SolicitacaoPublic)
def update_solicitacao_status(
    solicitacao_id: int,
    status_update: SolicitacaoUpdate,
    session: Session = Depends(get_session)
):
    db_solicitacao = session.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    if not db_solicitacao:
        raise HTTPException(status_code=404, detail="Solicitacao not found")

    db_solicitacao.status = status_update.status
    session.add(db_solicitacao)
    session.commit()
    session.refresh(db_solicitacao)

    return db_solicitacao


@router.delete('/{solicitacao_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_solicitacao(
    solicitacao_id: int,
    session: Session = Depends(get_session)
):
    db_solicitacao = session.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    if not db_solicitacao:
        raise HTTPException(status_code=404, detail="Solicitacao not found")

    session.delete(db_solicitacao)
    session.commit()