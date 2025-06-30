from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from domus_backend.database import get_session
from domus_backend.models import Solicitacao, User
from domus_backend.schemas import SolicitacaoCreate, SolicitacaoPublic, SolicitacaoUpdate

router = APIRouter(prefix='/solicitacoes', tags=['solicitacoes'])


# Define um endpoint para criar uma nova solicitação de manutenção.
# - @router.post: Define o método HTTP como POST.
# - '/manutencao': O caminho específico deste endpoint, resultando em /solicitacoes/manutencao.
# - response_model: Especifica que a resposta deve ser formatada usando o schema SolicitacaoPublic.
# - status_code: Define o código de status HTTP para 201 Created em caso de sucesso.
@router.post('/manutencao', response_model=SolicitacaoPublic, status_code=status.HTTP_201_CREATED)
def create_manutencao(
    solicitacao_data: SolicitacaoCreate,  # Valida os dados recebidos no corpo da requisição com o schema SolicitacaoCreate.
    session: Session = Depends(get_session)  # Injeta uma sessão de banco de dados na função.
):
    """
    Cria uma nova solicitação de manutenção.
    O corpo da requisição deve conter o 'user_id' e a 'descricao'.
    """
    # Passo 1: Verificar se o usuário que está criando a solicitação realmente existe no banco.
    user = session.query(User).filter(User.id == solicitacao_data.user_id).first()
    if not user:
        # Se o usuário não for encontrado, lança um erro 404 Not Found.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {solicitacao_data.user_id} not found",
        )

    # Passo 2: Criar a instância do objeto Solicitacao com os dados recebidos.
    nova_solicitacao = Solicitacao(
        descricao=solicitacao_data.descricao,
        user_id=solicitacao_data.user_id,
        tipo_solicitacao='manutencao',  # Define o tipo fixo para este endpoint.
        # O status padrão ('Enviado') é definido automaticamente pelo modelo.
    )

    # Passo 3: Adicionar a nova solicitação à sessão e salvar as mudanças no banco de dados.
    session.add(nova_solicitacao)
    session.commit()
    # Passo 4: Atualizar a instância com os dados do banco (como o ID gerado).
    session.refresh(nova_solicitacao)

    # Retorna o objeto da solicitação criada, que será formatado pelo response_model.
    return nova_solicitacao


# Define um endpoint para listar as solicitações.
@router.get('/', response_model=list[SolicitacaoPublic])
def get_solicitacoes(
    session: Session = Depends(get_session),
    user_id: int | None = None  # Parâmetro de query opcional para filtrar por usuário.
):
    """
    Lista todas as solicitações cadastradas.
    Pode ser filtrado opcionalmente por ID de usuário através de um parâmetro na URL,
    exemplo: /solicitacoes?user_id=1
    """
    # Inicia a consulta na tabela de solicitações.
    query = session.query(Solicitacao)
    # Se um 'user_id' for fornecido como parâmetro na URL...
    if user_id:
        # ...adiciona um filtro à consulta para buscar apenas as solicitações daquele usuário.
        query = query.filter(Solicitacao.user_id == user_id)
    
    # Executa a consulta e retorna todos os resultados encontrados.
    return query.all()


# Define um endpoint para atualizar o status de uma solicitação.
# - {solicitacao_id}: Define um parâmetro de caminho que será o ID da solicitação.
@router.patch('/{solicitacao_id}/status', response_model=SolicitacaoPublic)
def update_solicitacao_status(
    solicitacao_id: int,  # Recebe o ID da URL.
    status_update: SolicitacaoUpdate,  # Valida o corpo da requisição com o schema SolicitacaoUpdate.
    session: Session = Depends(get_session)
):
    """
    Atualiza o status de uma solicitação específica (ex: 'Analisando', 'Concluído').
    O corpo da requisição deve conter o novo 'status'.
    """
    # Busca a solicitação no banco de dados pelo ID fornecido.
    db_solicitacao = session.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    # Se não for encontrada, lança um erro 404.
    if not db_solicitacao:
        raise HTTPException(status_code=404, detail="Solicitacao not found")

    # Atualiza o campo 'status' do objeto com o novo valor recebido.
    db_solicitacao.status = status_update.status
    # Adiciona à sessão e salva a alteração no banco de dados.
    session.add(db_solicitacao)
    session.commit()
    session.refresh(db_solicitacao)

    # Retorna a solicitação com os dados atualizados.
    return db_solicitacao


# Define um endpoint para excluir uma solicitação.
# - status_code=204: Define o código de sucesso como 204 No Content, que é o padrão para DELETE.
@router.delete('/{solicitacao_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_solicitacao(
    solicitacao_id: int,  # Recebe o ID da solicitação a ser excluída pela URL.
    session: Session = Depends(get_session)
):
    """
    Exclui permanentemente uma solicitação específica do banco de dados.
    """
    # Busca a solicitação a ser excluída.
    db_solicitacao = session.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()
    # Se não for encontrada, lança um erro 404.
    if not db_solicitacao:
        raise HTTPException(status_code=404, detail="Solicitacao not found")

    # Exclui o objeto do banco de dados.
    session.delete(db_solicitacao)
    # Confirma a transação.
    session.commit()
    # Como o status de sucesso é 204, a resposta não terá corpo.