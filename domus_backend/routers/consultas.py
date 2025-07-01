from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta

from domus_backend.database import get_session
from domus_backend.models import User, Consulta, Indisponibilidade
from domus_backend.schemas import ConsultaCreate, ConsultaPublic, IndisponibilidadeCreate

router = APIRouter(prefix='/consultas', tags=['consultas'])

# --- LÓGICA DE HORÁRIOS ---

def gerar_horarios_atendimento(dia: date) -> list[datetime]:
    """Gera a lista completa de horários de atendimento para um dia específico."""
    horarios_disponiveis = []
    # Horários da manhã: 8, 9, 10, 11
    for hora in range(8, 12):
        horarios_disponiveis.append(datetime.combine(dia, time(hour=hora)))
    # Horários da tarde: 13, 14, 15, 16
    for hora in range(13, 17):
        horarios_disponiveis.append(datetime.combine(dia, time(hour=hora)))
    return horarios_disponiveis

# --- ENDPOINTS PARA USUÁRIOS ---

@router.get("/horarios_disponiveis/", response_model=list[datetime])
def get_horarios_disponiveis(dia: date, session: Session = Depends(get_session)):
    """
    Retorna uma lista de horários disponíveis para agendamento em um dia específico.
    Exemplo de uso: /consultas/horarios_disponiveis/?dia=2025-07-25
    """
    # 1. Gera todos os horários possíveis para o dia
    todos_horarios = gerar_horarios_atendimento(dia)

    # 2. Busca todos os agendamentos já feitos para aquele dia
    consultas_agendadas = session.query(Consulta).filter(
        Consulta.horario >= datetime.combine(dia, time.min),
        Consulta.horario <= datetime.combine(dia, time.max)
    ).all()
    horarios_ocupados = {c.horario for c in consultas_agendadas}

    # 3. Busca os períodos de indisponibilidade definidos pelo admin
    indisponibilidades = session.query(Indisponibilidade).filter(
        Indisponibilidade.horario_inicio <= datetime.combine(dia, time.max),
        Indisponibilidade.horario_fim >= datetime.combine(dia, time.min)
    ).all()

    # 4. Remove os horários ocupados e indisponíveis da lista de todos os horários
    horarios_disponiveis = [h for h in todos_horarios if h not in horarios_ocupados]
    
    final_disponiveis = []
    for horario in horarios_disponiveis:
        indisponivel = False
        for i in indisponibilidades:
            if i.horario_inicio <= horario < i.horario_fim:
                indisponivel = True
                break
        if not indisponivel:
            final_disponiveis.append(horario)

    return final_disponiveis


@router.post("/", response_model=ConsultaPublic, status_code=status.HTTP_201_CREATED)
def agendar_consulta(consulta_data: ConsultaCreate, session: Session = Depends(get_session)):
    """Agenda uma nova consulta para um usuário em um horário específico."""
    # Validações
    if not session.query(User).filter(User.id == consulta_data.user_id).first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    dia_agendamento = consulta_data.horario.date()
    if session.query(Consulta).filter(Consulta.user_id == consulta_data.user_id, Consulta.horario >= datetime.combine(dia_agendamento, time.min), Consulta.horario <= datetime.combine(dia_agendamento, time.max)).first():
        raise HTTPException(status_code=400, detail="Usuário já possui uma consulta agendada para este dia.")

    horarios_disponiveis = get_horarios_disponiveis(dia=dia_agendamento, session=session)
    if consulta_data.horario not in horarios_disponiveis:
        raise HTTPException(status_code=400, detail="Horário indisponível ou já agendado.")

    # Criação da consulta
    nova_consulta = Consulta(**consulta_data.model_dump())
    session.add(nova_consulta)
    session.commit()
    session.refresh(nova_consulta)
    return nova_consulta

# --- ENDPOINTS PARA ADMINISTRAÇÃO ---

# O ideal é que este endpoint esteja em /admin/consultas/indisponibilidade,
# mas para simplificar, vamos colocá-lo aqui por enquanto.
@router.post("/indisponibilidade/", status_code=status.HTTP_201_CREATED)
def criar_indisponibilidade(ind_data: IndisponibilidadeCreate, session: Session = Depends(get_session)):
    """Cria um novo período de indisponibilidade (acesso de admin)."""
    nova_indisponibilidade = Indisponibilidade(**ind_data.model_dump())
    session.add(nova_indisponibilidade)
    session.commit()
    return {"message": "Período de indisponibilidade criado com sucesso."}