from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime, time, timedelta

from domus_backend.database import get_session
from domus_backend.models import User, Consulta, Indisponibilidade
from domus_backend.schemas import ConsultaCreate, ConsultaPublic, IndisponibilidadeCreate

router = APIRouter(prefix='/consultas', tags=['consultas'])


def gerar_horarios_atendimento(dia: date) -> list[datetime]:
    horarios_disponiveis = []
    for hora in range(8, 12):
        horarios_disponiveis.append(datetime.combine(dia, time(hour=hora)))
    for hora in range(13, 17):
        horarios_disponiveis.append(datetime.combine(dia, time(hour=hora)))
    return horarios_disponiveis


@router.get("/horarios_disponiveis/", response_model=list[datetime])
def get_horarios_disponiveis(dia: date, session: Session = Depends(get_session)):
    
    todos_horarios = gerar_horarios_atendimento(dia)

    consultas_agendadas = session.query(Consulta).filter(
        Consulta.horario >= datetime.combine(dia, time.min),
        Consulta.horario <= datetime.combine(dia, time.max)
    ).all()
    horarios_ocupados = {c.horario for c in consultas_agendadas}

    indisponibilidades = session.query(Indisponibilidade).filter(
        Indisponibilidade.horario_inicio <= datetime.combine(dia, time.max),
        Indisponibilidade.horario_fim >= datetime.combine(dia, time.min)
    ).all()

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

    if not session.query(User).filter(User.id == consulta_data.user_id).first():
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    dia_agendamento = consulta_data.horario.date()
    if session.query(Consulta).filter(Consulta.user_id == consulta_data.user_id, Consulta.horario >= datetime.combine(dia_agendamento, time.min), Consulta.horario <= datetime.combine(dia_agendamento, time.max)).first():
        raise HTTPException(status_code=400, detail="Usuário já possui uma consulta agendada para este dia.")

    horarios_disponiveis = get_horarios_disponiveis(dia=dia_agendamento, session=session)
    if consulta_data.horario not in horarios_disponiveis:
        raise HTTPException(status_code=400, detail="Horário indisponível ou já agendado.")

    nova_consulta = Consulta(**consulta_data.model_dump())
    session.add(nova_consulta)
    session.commit()
    session.refresh(nova_consulta)
    return nova_consulta


@router.post("/indisponibilidade/", status_code=status.HTTP_201_CREATED)
def criar_indisponibilidade(ind_data: IndisponibilidadeCreate, session: Session = Depends(get_session)):

    nova_indisponibilidade = Indisponibilidade(**ind_data.model_dump())
    session.add(nova_indisponibilidade)
    session.commit()
    return {"message": "Período de indisponibilidade criado com sucesso."}