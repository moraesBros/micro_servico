from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Trip Service", description="Microsserviço de Operações Logísticas (Planejamento e Controle de Viagens)")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Rotas ---
@app.post("/rotas", response_model=schemas.RotaResponse)
def create_rota(rota: schemas.RotaCreate, db: Session = Depends(get_db)):
    return crud.create_rota(db, rota)

# --- Viagens ---
@app.post("/trips", response_model=schemas.ViagemResponse)
def planejar_viagem(viagem: schemas.ViagemCreate, db: Session = Depends(get_db)):
    """Planeja uma nova viagem (cria uma viagem com status planejada)."""
    db_viagem = crud.create_viagem(db, viagem)
    if db_viagem is None:
        raise HTTPException(status_code=400, detail="Rota inválida")
    return db_viagem

@app.post("/trips/{viagem_id}/start", response_model=schemas.ViagemResponse)
def iniciar_viagem(viagem_id: int, db: Session = Depends(get_db)):
    """Inicia a viagem: registra data de saída e altera status para 'em_andamento'."""
    try:
        viagem = crud.iniciar_viagem(db, viagem_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if viagem is None:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem

@app.post("/trips/{viagem_id}/complete", response_model=schemas.ViagemResponse)
def finalizar_viagem(viagem_id: int, db: Session = Depends(get_db)):
    """Finaliza a viagem: registra data de chegada e altera status para 'concluida'."""
    try:
        viagem = crud.finalizar_viagem(db, viagem_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if viagem is None:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem

@app.get("/trips/{viagem_id}", response_model=schemas.ViagemResponse)
def get_viagem(viagem_id: int, db: Session = Depends(get_db)):
    viagem = crud.get_viagem(db, viagem_id)
    if viagem is None:
        raise HTTPException(status_code=404, detail="Viagem não encontrada")
    return viagem
