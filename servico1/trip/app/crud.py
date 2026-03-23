from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime

# Rota
def create_rota(db: Session, rota: schemas.RotaCreate):
    db_rota = models.Rota(**rota.model_dump())
    db.add(db_rota)
    db.commit()
    db.refresh(db_rota)
    return db_rota

# Viagem
def get_viagem(db: Session, viagem_id: int):
    return db.query(models.Viagem).filter(models.Viagem.id == viagem_id).first()

def create_viagem(db: Session, viagem: schemas.ViagemCreate):
    # Verificar se rota existe
    rota = db.query(models.Rota).filter(models.Rota.id == viagem.rota_id).first()
    if not rota:
        return None
    db_viagem = models.Viagem(**viagem.model_dump())
    db.add(db_viagem)
    db.commit()
    db.refresh(db_viagem)
    # Emitir evento TripPlanned
    from app.events import emit_trip_planned
    emit_trip_planned(db_viagem.id)
    return db_viagem

def iniciar_viagem(db: Session, viagem_id: int):
    viagem = get_viagem(db, viagem_id)
    if not viagem:
        return None
    if viagem.status != models.StatusViagem.PLANEJADA:
        raise ValueError("Viagem só pode ser iniciada se estiver planejada")
    viagem.status = models.StatusViagem.EM_ANDAMENTO
    viagem.data_saida = datetime.now()
    db.commit()
    db.refresh(viagem)
    from app.events import emit_trip_started
    emit_trip_started(viagem_id)
    return viagem

def finalizar_viagem(db: Session, viagem_id: int):
    viagem = get_viagem(db, viagem_id)
    if not viagem:
        return None
    if viagem.status != models.StatusViagem.EM_ANDAMENTO:
        raise ValueError("Viagem só pode ser finalizada se estiver em andamento")
    viagem.status = models.StatusViagem.CONCLUIDA
    viagem.data_chegada = datetime.now()
    db.commit()
    db.refresh(viagem)
    from app.events import emit_trip_completed
    emit_trip_completed(viagem_id)
    return viagem
