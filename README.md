# Exemplo de Fila em Python com FastAPI + RQ (Redis Queue)

Aplicação simples que demonstra **enfileiramento de tarefas** em background usando [FastAPI](https://fastapi.tiangolo.com/), [Redis](https://redis.io/) e [RQ](https://python-rq.org/).

### Uso rápido com Docker

1. **Copie o arquivo de variáveis de ambiente**  
   ```bash
   cp .env.example .env
   
2. Build a imagem e suba os containers
   ```bash
   docker compose up -d --build
   
3. As rotas diponíveis estão em `http://127.0.0.1:8000/docs` ou IP + Porta se você alterou no `Dockerfile` e `docker-compose.yml`
