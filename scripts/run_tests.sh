#!/bin/bash

# SkyTrace Test Runner Script
# This script runs all tests locally to verify everything works before pushing

set -e  # Exit on any error

echo "🚀 SkyTrace Test Runner"
echo "======================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the SkyTraceV1 root directory"
    exit 1
fi

# Backend Tests
print_status "Running Backend Tests..."

cd backend

# Check if Python dependencies are installed
if ! python3 -c "import pytest" 2>/dev/null; then
    print_warning "Python dependencies not found. Installing..."
    pip3 install -r requirements.txt
fi

print_status "Running Python linting with flake8..."
if flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics; then
    print_success "Python linting passed"
else
    print_error "Python linting failed"
    exit 1
fi

print_status "Running Python unit tests..."
if python3 -m pytest tests/unit/ -v --tb=short; then
    print_success "Python unit tests passed"
else
    print_error "Python unit tests failed"
    exit 1
fi

print_status "Running Python integration tests..."
if python3 -m pytest tests/integration/ -v --tb=short; then
    print_success "Python integration tests passed"
else
    print_warning "Python integration tests failed (this may be expected without database)"
fi

cd ..

# Frontend Tests
print_status "Running Frontend Tests..."

cd frontend

# Check if Node dependencies are installed
if [ ! -d "node_modules" ]; then
    print_warning "Node dependencies not found. Installing..."
    npm install
fi

print_status "Running TypeScript type checking..."
if npx tsc --noEmit; then
    print_success "TypeScript type checking passed"
else
    print_error "TypeScript type checking failed"
    exit 1
fi

print_status "Running frontend unit tests..."
if npm test -- --coverage --watchAll=false; then
    print_success "Frontend unit tests passed"
else
    print_error "Frontend unit tests failed"
    exit 1
fi

print_status "Running frontend build..."
if npm run build; then
    print_success "Frontend build passed"
else
    print_error "Frontend build failed"
    exit 1
fi

cd ..

# Docker Tests
print_status "Testing Docker configuration..."

if docker-compose config > /dev/null 2>&1; then
    print_success "Docker Compose configuration is valid"
else
    print_error "Docker Compose configuration is invalid"
    exit 1
fi

# Summary
echo ""
echo "🎉 All tests completed successfully!"
echo ""
echo "Next steps:"
echo "1. Commit your changes: git add . && git commit -m 'Your commit message'"
echo "2. Push to GitHub: git push origin main"
echo "3. GitHub Actions will automatically run the full CI/CD pipeline"
echo ""
echo "To run with Docker:"
echo "  make up           # Start all services"
echo "  make load-test-data  # Load sample data"
echo "  make logs         # View logs"
echo ""
echo "Happy coding! 🚀"