# GitHub Actions CI/CD Setup

This document explains the comprehensive GitHub Actions pipeline created for the SkyTrace project.

## 🚀 Pipeline Overview

The CI/CD pipeline automatically runs on every push to `main` or `develop` branches and on all pull requests. It provides comprehensive testing, security scanning, and quality checks.

## 📋 Pipeline Jobs

### 1. Backend Testing (`test-backend`)
**Duration**: ~3-5 minutes  
**Purpose**: Validates Python/FastAPI backend code

**Steps**:
- ✅ Sets up Python 3.11 environment
- ✅ Starts PostgreSQL with PostGIS extensions
- ✅ Caches pip dependencies for faster builds
- ✅ Installs Python requirements
- ✅ Waits for database to be ready
- ✅ Initializes test database with schema
- ✅ Runs code linting (flake8)
- ✅ Runs unit tests with pytest
- ✅ Runs integration tests with database

**What Gets Tested**:
- Pydantic schema validation
- Data client functionality
- API endpoint responses
- Database operations
- Business logic services

### 2. Frontend Testing (`test-frontend`)
**Duration**: ~2-4 minutes  
**Purpose**: Validates React/TypeScript frontend code

**Steps**:
- ✅ Sets up Node.js 18 environment
- ✅ Caches npm dependencies for faster builds
- ✅ Installs frontend dependencies
- ✅ Runs TypeScript type checking
- ✅ Runs unit tests with coverage
- ✅ Builds production bundle

**What Gets Tested**:
- Component rendering and behavior
- User interaction handling
- API service calls
- Type safety compliance
- Production build success

### 3. Docker Build (`docker-build`)
**Duration**: ~2-3 minutes  
**Purpose**: Validates Docker deployment configuration

**Steps**:
- ✅ Sets up Docker Buildx
- ✅ Builds backend Docker image
- ✅ Builds frontend Docker image
- ✅ Validates docker-compose configuration

**What Gets Tested**:
- Docker image build success
- Multi-stage build optimization
- Container configuration validity

### 4. Security Scanning (`security-scan`)
**Duration**: ~1-2 minutes  
**Purpose**: Identifies security vulnerabilities

**Steps**:
- ✅ Runs Trivy vulnerability scanner
- ✅ Scans filesystem for known vulnerabilities
- ✅ Uploads results to GitHub Security tab
- ✅ Generates SARIF security report

**What Gets Scanned**:
- Python package vulnerabilities
- Node.js package vulnerabilities
- Container image vulnerabilities
- Code security issues

### 5. Code Quality (`code-quality`)
**Duration**: ~1-2 minutes  
**Purpose**: Enforces code quality standards

**Steps**:
- ✅ Checks Python code formatting (black)
- ✅ Checks import sorting (isort)
- ✅ Runs security analysis (bandit)
- ✅ Checks dependency vulnerabilities (safety)

**What Gets Checked**:
- PEP 8 compliance
- Code formatting consistency
- Import organization
- Security best practices
- Dependency security

### 6. Notification (`notification`)
**Duration**: ~10 seconds  
**Purpose**: Provides pipeline status summary

**Steps**:
- ✅ Reports success/failure status
- ✅ Details results from each job
- ✅ Provides actionable feedback

## 📊 Example Test Results

### Successful Pipeline Output:
```
✅ Backend tests: success (45 tests passed)
✅ Frontend tests: success (23 tests passed)  
✅ Docker build: success
✅ Security scan: success (0 vulnerabilities)
✅ Code quality: success
```

### Sample Test Coverage:
- **Backend Unit Tests**: 15 tests covering schemas, clients, and utilities
- **Backend Integration Tests**: 10 tests covering API endpoints and database
- **Frontend Component Tests**: 12 tests covering UI components and interactions
- **Frontend Service Tests**: 8 tests covering API services and error handling

## 🔧 Local Testing

Before pushing to GitHub, run tests locally:

```bash
# Run comprehensive test suite
./scripts/run_tests.sh

# Or run individual test types
make test-backend      # Python tests
make test-frontend     # React tests
make lint             # Code linting
make format           # Code formatting
```

## 🎯 Test Examples Included

### Backend Tests (`backend/tests/`)

**Unit Tests** (`tests/unit/test_example.py`):
```python
def test_basic_assertion():
    assert True
    assert 1 + 1 == 2

@pytest.mark.asyncio
async def test_async_function():
    result = await async_add(2, 3)
    assert result == 5

@pytest.mark.parametrize("input_val,expected", [
    ("adsb_icao", True),
    ("invalid", False),
])
def test_aircraft_type_validation(input_val, expected):
    valid_types = ["adsb_icao", "mode_s", "tisb", "mlat"]
    result = input_val in valid_types
    assert result == expected
```

**Schema Tests** (`tests/unit/test_schemas.py`):
```python
def test_aircraft_create_valid_data():
    aircraft = AircraftCreate(**sample_aircraft_data)
    assert aircraft.hex == "ae1460"
    assert aircraft.latitude == 37.7749

def test_aircraft_create_invalid_latitude():
    with pytest.raises(ValidationError):
        AircraftCreate(hex="ae1460", latitude=95.0)  # Invalid
```

**Client Tests** (`tests/unit/test_clients.py`):
```python
@pytest.mark.asyncio
async def test_mock_aircraft_client():
    client = MockAircraftClient()
    data = await client.fetch_data()
    assert len(data) >= 10
    assert all(client.validate_data(aircraft) for aircraft in data)
```

**Integration Tests** (`tests/integration/test_api_endpoints.py`):
```python
def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
```

### Frontend Tests (`frontend/src/`)

**Component Tests** (`components/__tests__/LayerPanel.test.tsx`):
```typescript
test('renders layer panel with layers', () => {
  render(<LayerPanel />);
  expect(screen.getByText('Map Layers')).toBeInTheDocument();
  expect(screen.getByText('Test Layer 1')).toBeInTheDocument();
});

test('toggle layer visibility calls correct function', () => {
  render(<LayerPanel />);
  fireEvent.click(screen.getByText('Hide'));
  expect(mockToggleVisibility).toHaveBeenCalled();
});
```

**Service Tests** (`services/__tests__/api.test.ts`):
```typescript
test('getAircraft calls correct endpoint', async () => {
  mockAxios.get.mockResolvedValue({ data: { aircraft: [] } });
  const result = await aircraftApi.getAircraft();
  expect(mockAxios.get).toHaveBeenCalledWith('/aircraft/');
});
```

## 🚦 Pipeline Status

### Success Indicators:
- ✅ All tests pass
- ✅ Code coverage meets thresholds
- ✅ No security vulnerabilities found
- ✅ Code quality checks pass
- ✅ Docker builds successfully

### Failure Scenarios:
- ❌ Test failures (unit/integration)
- ❌ TypeScript compilation errors
- ❌ Linting violations
- ❌ Security vulnerabilities detected
- ❌ Docker build failures

## 🔒 Security Features

### Vulnerability Scanning:
- **Trivy**: Scans containers and dependencies
- **Bandit**: Python security analysis
- **Safety**: Python dependency vulnerabilities
- **GitHub Security**: Automated alerts and reporting

### Security Reports:
- Results uploaded to GitHub Security tab
- SARIF format for detailed vulnerability info
- Automated dependency update suggestions

## 📈 Extending the Pipeline

### Adding New Tests:

1. **Backend Tests**: Add files to `backend/tests/unit/` or `backend/tests/integration/`
2. **Frontend Tests**: Add files to `frontend/src/**/__tests__/`
3. **Custom Scripts**: Add to `scripts/` directory

### Adding New Jobs:

1. **Performance Testing**: Add Lighthouse CI for frontend performance
2. **E2E Testing**: Add Playwright or Cypress for end-to-end testing
3. **Deployment**: Add automatic deployment to staging/production

### Configuration Options:

```yaml
# In .github/workflows/ci.yml
env:
  DATABASE_URL: postgresql://...
  NODE_VERSION: 18
  PYTHON_VERSION: 3.11
  COVERAGE_THRESHOLD: 80
```

## 🎉 Getting Started

1. **Push to GitHub**: The pipeline runs automatically
2. **Check Results**: View in GitHub Actions tab
3. **Fix Issues**: Address any failing tests or quality issues
4. **Iterate**: Continue developing with confidence

## 📚 Additional Resources

- **Testing Guide**: See `TESTING.md` for detailed testing documentation
- **Local Setup**: See `README.md` for development setup
- **GitHub Actions**: View real-time results in your repository's Actions tab

The pipeline ensures that every code change is thoroughly tested, secure, and maintains high quality standards before being merged into the main branch.