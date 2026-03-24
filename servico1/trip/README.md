# Trip Service (Simplificado)

Microsserviço para planejamento e controle de viagens (saída e chegada).  
Não inclui registro de carga, associação de motorista nem atualização de status de entrega.

## Funcionalidades
- Cadastro de rotas
- Planejamento de viagens (POST /trips)
- Início de viagem (POST /trips/{id}/start)
- Finalização de viagem (POST /trips/{id}/complete)
- Consulta de viagem (GET /trips/{id})

## Tecnologias
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker / Docker Compose

## Como executar

1. Clone o repositório.
2. Navegue até o diretório do projeto.
3. Execute:
   ```bash
   docker-compose up --build
