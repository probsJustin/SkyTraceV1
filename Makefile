.PHONY: build up down logs test clean load-test-data

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Development commands
dev:
	docker-compose up

restart:
	docker-compose restart

# Database commands
db-reset:
	docker-compose down -v
	docker-compose up -d db
	sleep 5
	docker-compose up -d

# Test commands
test:
	docker-compose exec backend python -m pytest

test-local:
	./scripts/run_tests.sh

test-backend:
	cd backend && python -m pytest tests/ -v

test-frontend:
	cd frontend && npm test -- --coverage --watchAll=false

test-unit:
	cd backend && python -m pytest tests/unit/ -v

test-integration:
	cd backend && python -m pytest tests/integration/ -v

lint:
	cd backend && flake8 app/ tests/
	cd frontend && npm run lint

format:
	cd backend && black app/ tests/ && isort app/ tests/

load-test-data:
	python scripts/load_test_data.py

# Cleanup
clean:
	docker-compose down -v
	docker system prune -f

# Health check
health:
	@echo "Checking backend health..."
	@curl -f http://localhost:8000/health || echo "Backend not responding"
	@echo "Checking frontend..."
	@curl -f http://localhost:3000 || echo "Frontend not responding"

# Show logs for specific service
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f db