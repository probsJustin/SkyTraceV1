# SkyTrace V1

A modern, multi-tenant aircraft tracking and mapping system built with Python/FastAPI backend and React frontend.

## Features

- **Multi-tenant architecture** - Support for multiple organizations
- **Real-time aircraft tracking** - Live aircraft data visualization
- **Modular data clients** - Extensible system for different data sources
- **Interactive mapping** - React-based map with layer management
- **Feature flags** - Runtime feature toggles
- **PostGIS integration** - Advanced geospatial data handling
- **Docker-based deployment** - Easy setup and deployment

## Architecture

### Backend (Python/FastAPI)
- **FastAPI** - Modern, fast web framework
- **PostgreSQL + PostGIS** - Geospatial database
- **SQLAlchemy** - ORM with async support
- **Pydantic** - Data validation and serialization
- **Structured logging** - JSON-based logging
- **Feature flags** - Runtime configuration

### Frontend (React/TypeScript)
- **React 18** - Modern React with hooks
- **TypeScript** - Type-safe development
- **MapLibre GL** - High-performance mapping
- **Layer management** - Dynamic map layer control
- **Real-time updates** - Auto-refreshing data

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Make (optional, for convenience commands)

### 1. Clone and Start
```bash
git clone <repository>
cd SkyTraceV1

# Build and start all services
make up
# or
docker-compose up -d
```

### 2. Load Test Data
```bash
# Wait for services to be ready (about 30 seconds)
make load-test-data
# or
python scripts/load_test_data.py
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Development

### Project Structure
```
SkyTraceV1/
├── backend/                 # Python/FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── clients/        # Data collection clients
│   ├── sql/                # Database initialization
│   └── tests/              # Backend tests
├── frontend/               # React/TypeScript frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── scripts/                # Utility scripts
└── docker-compose.yml      # Container orchestration
```

### Database Schema

The system uses PostgreSQL with PostGIS for geospatial data:

- **tenants** - Multi-tenant organization support
- **users** - User management (for future SSO)
- **feature_flags** - Runtime feature toggles
- **data_sources** - Configurable data collection
- **aircraft** - Aircraft tracking data with PostGIS geometry
- **map_layers** - Dynamic map layer configuration

### API Endpoints

#### Aircraft
- `GET /api/v1/aircraft/` - List aircraft with pagination
- `GET /api/v1/aircraft/{id}` - Get specific aircraft
- `POST /api/v1/aircraft/` - Create aircraft
- `GET /api/v1/aircraft/geojson/all` - Get aircraft as GeoJSON
- `POST /api/v1/aircraft/bulk` - Bulk create/update aircraft

#### Map Layers
- `GET /api/v1/map-layers/` - List map layers
- `POST /api/v1/map-layers/` - Create map layer
- `PATCH /api/v1/map-layers/{id}` - Update map layer

#### Feature Flags
- `GET /api/v1/feature-flags/` - List feature flags
- `PATCH /api/v1/feature-flags/{name}` - Update feature flag

#### Data Sources
- `GET /api/v1/data-sources/` - List data sources
- `POST /api/v1/data-sources/` - Create data source

### Adding New Data Clients

1. Create a new client class in `backend/app/clients/`:
```python
from .base_client import BaseDataClient

class MyDataClient(BaseDataClient):
    async def fetch_data(self):
        # Implement data fetching logic
        pass
    
    def validate_data(self, data):
        # Implement data validation
        pass
```

2. Register the client in a data source via the API
3. The system will automatically use the client for data collection

### Commands

```bash
# Development
make dev          # Start in development mode
make up           # Start in background
make down         # Stop all services
make restart      # Restart services

# Database
make db-reset     # Reset database with fresh data

# Testing
make test         # Run backend tests
make load-test-data  # Load sample aircraft data

# Monitoring
make logs         # View all logs
make logs-backend # View backend logs
make health       # Check service health

# Cleanup
make clean        # Stop and clean all containers
```

## Configuration

### Environment Variables

Backend configuration via environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `ENVIRONMENT` - Environment name (development/production)
- `LOG_LEVEL` - Logging level
- `CORS_ORIGINS` - Allowed CORS origins
- `MULTI_TENANT_ENABLED` - Enable multi-tenant mode
- `SSO_ENABLED` - Enable SSO authentication

### Feature Flags

Runtime feature toggles available:

- `sso_enabled` - Single Sign-On authentication
- `multi_tenant` - Multi-tenant functionality
- `realtime_updates` - Real-time data updates
- `advanced_filtering` - Advanced filtering options

## Extending the System

### Adding New Layer Types

1. Create new layer type in database
2. Implement data processing in backend service
3. Add visualization in frontend MapView component

### Adding New Data Sources

1. Implement new client class extending `BaseDataClient`
2. Register client in data sources API
3. Configure refresh intervals and data processing

### Custom Map Styling

Map layers support custom styling via `style_config` JSON field:

```json
{
  "circle-radius": 8,
  "circle-color": "#ff0000",
  "circle-stroke-width": 2
}
```

## Production Deployment

### Security Considerations

- Change default database passwords
- Configure proper CORS origins
- Enable SSL/TLS termination
- Set up proper logging and monitoring
- Configure authentication when ready

### Scaling

- Use managed PostgreSQL service
- Add Redis for caching and Celery for background tasks
- Configure horizontal scaling for backend API
- Use CDN for frontend assets

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Ensure PostgreSQL container is running
   - Check connection string in environment variables

2. **Frontend can't connect to backend**
   - Verify backend is running on port 8000
   - Check CORS configuration

3. **No aircraft data showing**
   - Run `make load-test-data` to load sample data
   - Check API endpoints are responding

### Logs

```bash
# View all logs
make logs

# View specific service logs
make logs-backend
make logs-frontend
make logs-db

# Check service health
make health
```

## Contributing

1. Follow PEP 8 for Python code
2. Use TypeScript for frontend development
3. Add tests for new features
4. Update documentation for API changes

## License

See LICENSE file for details.