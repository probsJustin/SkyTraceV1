# Testing Guide

This document outlines the testing strategy and setup for the SkyTrace project.

## Overview

The project uses a comprehensive testing approach with:

- **Backend**: Python with pytest, async testing, integration tests
- **Frontend**: React Testing Library, Jest, TypeScript type checking
- **CI/CD**: GitHub Actions with automated testing pipeline
- **Code Quality**: Linting, formatting, security scanning

## Quick Start

### Run All Tests Locally
```bash
# Run the comprehensive test script
./scripts/run_tests.sh
```

### Backend Tests
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest

# Run specific test types
python -m pytest tests/unit/          # Unit tests only
python -m pytest tests/integration/   # Integration tests only

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run linting
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
```

### Frontend Tests
```bash
cd frontend

# Install dependencies
npm install

# Run all tests
npm test

# Run tests with coverage (CI mode)
npm run test:ci

# Run TypeScript type checking
npx tsc --noEmit

# Build project
npm run build
```

## Testing Architecture

### Backend Testing

#### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Framework**: pytest with async support
- **Coverage**: Schemas, services, clients, utilities
- **Mocking**: External dependencies mocked

Example structure:
```
tests/unit/
├── test_example.py        # Basic passing tests
├── test_schemas.py        # Pydantic schema validation
├── test_clients.py        # Data client functionality
├── test_services.py       # Business logic (to be added)
└── test_utils.py          # Utility functions (to be added)
```

#### Integration Tests (`tests/integration/`)
- **Purpose**: Test API endpoints and database interactions
- **Framework**: FastAPI TestClient with async database
- **Coverage**: API endpoints, database operations, workflows
- **Database**: In-memory SQLite for fast testing

Example structure:
```
tests/integration/
├── test_api_endpoints.py  # API endpoint testing
├── test_database.py       # Database operations (to be added)
└── test_workflows.py      # End-to-end workflows (to be added)
```

#### Test Configuration (`conftest.py`)
- Async database fixtures
- Test tenant setup
- Sample data fixtures
- Dependency overrides

### Frontend Testing

#### Component Tests (`src/components/__tests__/`)
- **Purpose**: Test React components in isolation
- **Framework**: React Testing Library + Jest
- **Coverage**: Component rendering, user interactions, props
- **Mocking**: External dependencies and complex children

#### Service Tests (`src/services/__tests__/`)
- **Purpose**: Test API services and utilities
- **Framework**: Jest
- **Coverage**: API calls, error handling, data transformation
- **Mocking**: Axios HTTP client

#### Integration Tests
- **Purpose**: Test component interactions and data flow
- **Framework**: React Testing Library
- **Coverage**: User workflows, state management, API integration

## CI/CD Pipeline

### GitHub Actions Workflow (`.github/workflows/ci.yml`)

The pipeline runs on every push and pull request with the following jobs:

#### 1. Backend Testing (`test-backend`)
- Sets up Python 3.11
- Starts PostgreSQL with PostGIS
- Installs dependencies with caching
- Runs linting (flake8)
- Runs unit tests
- Runs integration tests
- Reports coverage

#### 2. Frontend Testing (`test-frontend`)
- Sets up Node.js 18
- Installs dependencies with caching
- Runs TypeScript type checking
- Runs unit tests with coverage
- Builds production bundle

#### 3. Docker Build (`docker-build`)
- Builds backend Docker image
- Builds frontend Docker image
- Validates docker-compose configuration

#### 4. Security Scanning (`security-scan`)
- Runs Trivy vulnerability scanner
- Uploads results to GitHub Security tab
- Scans for known vulnerabilities

#### 5. Code Quality (`code-quality`)
- Checks Python code formatting (black)
- Checks import sorting (isort)
- Runs security analysis (bandit)
- Checks dependency vulnerabilities (safety)

#### 6. Notification (`notification`)
- Reports overall pipeline status
- Provides detailed results summary

## Test Data

### Sample Data
- **Aircraft data**: Realistic aviation data formats
- **Tenant data**: Multi-tenant test scenarios
- **Feature flags**: Configuration testing
- **Map layers**: Visualization testing

### Fixtures
- Pre-configured test tenants
- Sample aircraft with various states
- Feature flag configurations
- Map layer definitions

## Writing Tests

### Backend Test Examples

#### Unit Test
```python
def test_aircraft_validation():
    """Test aircraft schema validation"""
    aircraft_data = {
        "hex": "ae1460",
        "type": "adsb_icao",
        "latitude": 37.7749,
        "longitude": -122.4194
    }
    aircraft = AircraftCreate(**aircraft_data)
    assert aircraft.hex == "ae1460"
```

#### Async Test
```python
@pytest.mark.asyncio
async def test_aircraft_service():
    """Test aircraft service operations"""
    service = AircraftService(session)
    aircraft = await service.create_aircraft(tenant_id, aircraft_data)
    assert aircraft.hex == "ae1460"
```

#### Integration Test
```python
def test_aircraft_api_endpoint():
    """Test aircraft API endpoint"""
    with TestClient(app) as client:
        response = client.get("/api/v1/aircraft/")
        assert response.status_code == 200
```

### Frontend Test Examples

#### Component Test
```typescript
test('renders aircraft list', () => {
  render(<AircraftList aircraft={mockAircraft} />);
  expect(screen.getByText('TEST123')).toBeInTheDocument();
});
```

#### User Interaction Test
```typescript
test('toggles layer visibility', () => {
  render(<LayerPanel />);
  fireEvent.click(screen.getByText('Hide'));
  expect(mockToggleVisibility).toHaveBeenCalled();
});
```

#### API Service Test
```typescript
test('fetches aircraft data', async () => {
  mockAxios.get.mockResolvedValue({ data: { aircraft: [] } });
  const result = await aircraftApi.getAircraft();
  expect(result.aircraft).toEqual([]);
});
```

## Code Coverage

### Backend Coverage Targets
- **Overall**: > 80%
- **Unit tests**: > 90%
- **Integration tests**: > 70%

### Frontend Coverage Targets
- **Components**: > 80%
- **Services**: > 90%
- **Utilities**: > 95%

### Coverage Reports
- Backend: `htmlcov/index.html` (after running `pytest --cov`)
- Frontend: `coverage/lcov-report/index.html` (after running `npm run test:ci`)

## Testing Best Practices

### General
1. **Test Naming**: Descriptive test names explaining what is being tested
2. **Test Structure**: Arrange, Act, Assert pattern
3. **Test Independence**: Each test should be independent and repeatable
4. **Test Data**: Use realistic but minimal test data
5. **Error Testing**: Test both success and failure scenarios

### Backend Specific
1. **Async Testing**: Use `@pytest.mark.asyncio` for async functions
2. **Database Testing**: Use transactions and rollbacks for isolation
3. **Mocking**: Mock external services and dependencies
4. **Fixtures**: Reuse common test setup through fixtures

### Frontend Specific
1. **Component Testing**: Test behavior, not implementation
2. **User Events**: Use `fireEvent` for user interactions
3. **Async Testing**: Use `waitFor` for async operations
4. **Mocking**: Mock external dependencies and complex children

## Debugging Tests

### Backend Debugging
```bash
# Run specific test with verbose output
python -m pytest tests/unit/test_example.py::test_basic_assertion -v

# Run with debugger
python -m pytest --pdb tests/unit/test_example.py

# Run with print statements
python -m pytest -s tests/unit/test_example.py
```

### Frontend Debugging
```bash
# Run specific test
npm test -- --testNamePattern="renders aircraft list"

# Run with coverage
npm test -- --coverage --watchAll=false

# Debug in browser (rare, but possible)
npm test -- --debug
```

## Continuous Integration

### Local Pre-commit Checks
```bash
# Run before committing
./scripts/run_tests.sh

# Quick checks
make test                    # Run backend tests
cd frontend && npm test      # Run frontend tests
```

### GitHub Actions
- Automatically triggered on push/PR
- Runs comprehensive test suite
- Reports results in GitHub interface
- Blocks merge if tests fail

### Status Badges
Add to README for visibility:
```markdown
![CI Status](https://github.com/your-org/skytrace/workflows/CI%2FCD%20Pipeline/badge.svg)
```

## Performance Testing

### Load Testing (Future)
- API endpoint performance
- Database query optimization
- Frontend rendering performance

### Tools to Consider
- **Backend**: locust, pytest-benchmark
- **Frontend**: Lighthouse CI, Web Vitals
- **Database**: pgbench, query profiling

## Security Testing

### Current Tools
- **Trivy**: Vulnerability scanning
- **Bandit**: Python security analysis
- **Safety**: Dependency vulnerability check

### Future Enhancements
- Penetration testing
- Authentication testing
- Input validation testing
- OWASP compliance checks

## Maintenance

### Regular Tasks
1. Update test dependencies
2. Review and update test coverage targets
3. Clean up obsolete tests
4. Update test data as schemas evolve
5. Monitor CI/CD performance

### Test Data Management
- Keep test data minimal but realistic
- Update sample data when API changes
- Document test data sources and formats
- Rotate any sensitive test data regularly

This testing setup ensures high code quality, reliability, and maintainability for the SkyTrace project.