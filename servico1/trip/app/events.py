import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def emit_trip_planned(trip_id: int):
    logger.info(f"Evento: TripPlanned - Viagem {trip_id} planejada")

def emit_trip_started(trip_id: int):
    logger.info(f"Evento: TripStarted - Viagem {trip_id} iniciada")

def emit_trip_completed(trip_id: int):
    logger.info(f"Evento: TripCompleted - Viagem {trip_id} concluída")
