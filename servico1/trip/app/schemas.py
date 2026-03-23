from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.models import StatusViagem

# Rota
class RotaBase(BaseModel):
    origem: str
    destino: str
    distancia_km: Optional[float] = None
    duracao_estimada_horas: Optional[float] = None

class RotaCreate(RotaBase):
    pass

class RotaResponse(RotaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

# Viagem
class ViagemBase(BaseModel):
    rota_id: int

class ViagemCreate(ViagemBase):
    pass

class ViagemResponse(BaseModel):
    id: int
    rota_id: int
    data_saida: Optional[datetime]
    data_chegada: Optional[datetime]
    status: StatusViagem
    rota: RotaResponse

    model_config = ConfigDict(from_attributes=True)
