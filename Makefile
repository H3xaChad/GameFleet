# GameFleet - Docker Management

# Configuration
DOCKER_REPO ?= h3xachad
PROJECT_NAME = gamefleet
VERSION ?= latest
BACKEND_IMAGE = $(DOCKER_REPO)/$(PROJECT_NAME)-backend
FRONTEND_IMAGE = $(DOCKER_REPO)/$(PROJECT_NAME)-frontend

# Development & Production
dev: ## Start development environment
	docker-compose up --build

up: ## Start production environment
	docker-compose up -d --build

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

# Building
build: ## Build all images
	docker-compose build --no-cache

# Docker Hub Operations
tag: ## Tag images for Docker Hub
	docker tag $(PROJECT_NAME)_backend $(BACKEND_IMAGE):$(VERSION)
	docker tag $(PROJECT_NAME)_frontend $(FRONTEND_IMAGE):$(VERSION)

push: tag ## Push images to Docker Hub
	docker push $(BACKEND_IMAGE):$(VERSION)
	docker push $(FRONTEND_IMAGE):$(VERSION)

pull: ## Pull images from Docker Hub
	docker pull $(BACKEND_IMAGE):$(VERSION)
	docker pull $(FRONTEND_IMAGE):$(VERSION)

release: build tag push ## Build, tag and push new release

# Utilities
logs: ## Follow logs from all services
	docker-compose logs -f

logs-backend: ## Follow backend logs only
	docker-compose logs -f backend

status: ## Show container status
	docker-compose ps

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

# Cleanup
clean: ## Stop and remove containers with volumes
	docker-compose down -v

clean-all: clean ## Full cleanup including images
	docker system prune -f

help: ## Show this help message
	@echo "GameFleet Docker Management"
	@echo ""
	@echo "Usage: make [target] [DOCKER_REPO=username] [VERSION=tag]"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  %-20s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)