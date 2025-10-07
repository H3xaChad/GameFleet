# Development
dev: dev-backend dev-frontend
dev-backend:
    cd backend && make dev
dev-frontend:
    cd frontend && make dev

# Docker
build:
    docker-compose build
up:
    docker-compose up -d
down:
    docker-compose down

# Setup
install:
    cd backend && uv sync
    cd frontend && pnpm install