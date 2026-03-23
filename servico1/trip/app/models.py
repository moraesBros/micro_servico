from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class StatusViagem(str, enum.Enum):
    PLANEJADA = "planejada"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"

class Rota(Base):
    __tablename__ = "rotas"

    id = Column(Integer, primary_key=True, index=True)
    origem = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    distancia_km = Column(Float)
    duracao_estimada_horas = Column(Float)

    viagens = relationship("Viagem", back_populates="rota")

class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, index=True)
    data_saida = Column(DateTime, nullable=True)
    data_chegada = Column(DateTime, nullable=True)
    status = Column(Enum(StatusViagem), default=StatusViagem.PLANEJADA)

    rota_id = Column(Integer, ForeignKey("rotas.id"), nullable=False)
    rota = relationship("Rota", back_populates="viagens")
