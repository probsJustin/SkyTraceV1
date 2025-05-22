-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE aircraft_type AS ENUM ('adsb_icao', 'mode_s', 'tisb', 'mlat');
CREATE TYPE emergency_type AS ENUM ('none', 'general', 'lifeguard', 'minfuel', 'nordo', 'unlawful', 'downed');

-- Create tenants table
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create users table (for future SSO)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

-- Create feature flags table
CREATE TABLE IF NOT EXISTS feature_flags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    enabled BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(tenant_id, name)
);

-- Create data sources table
CREATE TABLE IF NOT EXISTS data_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL, -- 'aircraft', 'ships', 'locations', etc.
    client_class VARCHAR(255) NOT NULL, -- Python class name for the client
    config JSONB, -- Configuration for the client
    is_active BOOLEAN DEFAULT TRUE,
    refresh_interval INTEGER DEFAULT 60, -- seconds
    last_updated TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create aircraft table
CREATE TABLE IF NOT EXISTS aircraft (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    hex VARCHAR(6) NOT NULL, -- ICAO 24-bit address
    type aircraft_type NOT NULL,
    flight VARCHAR(20),
    registration VARCHAR(20),
    aircraft_type_code VARCHAR(10), -- Aircraft type (e.g., B738, A320)
    db_flags INTEGER,
    squawk VARCHAR(4),
    emergency emergency_type DEFAULT 'none',
    category VARCHAR(5),
    
    -- Position data
    position GEOMETRY(POINT, 4326),
    altitude_baro INTEGER,
    altitude_geom INTEGER,
    ground_speed DECIMAL(8,2),
    track DECIMAL(6,2),
    true_heading DECIMAL(6,2),
    vertical_rate INTEGER,
    
    -- Quality indicators
    nic INTEGER, -- Navigation Integrity Category
    nac_p INTEGER, -- Navigation Accuracy Category - Position
    nac_v INTEGER, -- Navigation Accuracy Category - Velocity
    sil INTEGER, -- Source Integrity Level
    sil_type VARCHAR(20),
    sda INTEGER, -- System Design Assurance
    
    -- Timing and signal data
    messages BIGINT,
    seen DECIMAL(10,2),
    seen_pos DECIMAL(10,2),
    rssi DECIMAL(6,2),
    
    -- GPS data
    gps_ok_before DECIMAL(15,1),
    gps_ok_lat DECIMAL(10,6),
    gps_ok_lon DECIMAL(11,6),
    
    -- Raw data
    raw_data JSONB,
    
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(tenant_id, hex)
);

-- Create aircraft archive table (same structure but with additional fields)
CREATE TABLE IF NOT EXISTS aircraft_archive (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    original_aircraft_id UUID NOT NULL, -- Reference to original aircraft record
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    hex VARCHAR(6) NOT NULL, -- ICAO 24-bit address
    type aircraft_type NOT NULL,
    flight VARCHAR(20),
    registration VARCHAR(20),
    aircraft_type_code VARCHAR(10), -- Aircraft type (e.g., B738, A320)
    db_flags INTEGER,
    squawk VARCHAR(4),
    emergency emergency_type DEFAULT 'none',
    category VARCHAR(5),
    
    -- Position data
    position GEOMETRY(POINT, 4326),
    altitude_baro INTEGER,
    altitude_geom INTEGER,
    ground_speed DECIMAL(8,2),
    track DECIMAL(6,2),
    true_heading DECIMAL(6,2),
    vertical_rate INTEGER,
    
    -- Quality indicators
    nic INTEGER, -- Navigation Integrity Category
    nac_p INTEGER, -- Navigation Accuracy Category - Position
    nac_v INTEGER, -- Navigation Accuracy Category - Velocity
    sil INTEGER, -- Source Integrity Level
    sil_type VARCHAR(20),
    sda INTEGER, -- System Design Assurance
    
    -- Timing and signal data
    messages BIGINT,
    seen DECIMAL(10,2),
    seen_pos DECIMAL(10,2),
    rssi DECIMAL(6,2),
    
    -- GPS data
    gps_ok_before DECIMAL(15,1),
    gps_ok_lat DECIMAL(10,6),
    gps_ok_lon DECIMAL(11,6),
    
    -- Raw data
    raw_data JSONB,
    
    -- Archive-specific fields
    archived_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    original_created_at TIMESTAMP WITH TIME ZONE,
    original_last_updated TIMESTAMP WITH TIME ZONE,
    archive_reason VARCHAR(50) DEFAULT 'scheduled_refresh' -- Why this was archived
);

-- Create indexes
CREATE INDEX idx_aircraft_position ON aircraft USING GIST (position);
CREATE INDEX idx_aircraft_hex ON aircraft (hex);
CREATE INDEX idx_aircraft_tenant ON aircraft (tenant_id);
CREATE INDEX idx_aircraft_last_updated ON aircraft (last_updated);
CREATE INDEX idx_aircraft_flight ON aircraft (flight) WHERE flight IS NOT NULL;

-- Archive table indexes
CREATE INDEX idx_aircraft_archive_original_id ON aircraft_archive (original_aircraft_id);
CREATE INDEX idx_aircraft_archive_tenant ON aircraft_archive (tenant_id);
CREATE INDEX idx_aircraft_archive_hex ON aircraft_archive (hex);
CREATE INDEX idx_aircraft_archive_archived_at ON aircraft_archive (archived_at);
CREATE INDEX idx_aircraft_archive_position ON aircraft_archive USING GIST (position);

-- Create layers table for map layers
CREATE TABLE IF NOT EXISTS map_layers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    layer_type VARCHAR(100) NOT NULL, -- 'aircraft', 'geojson', 'pmtiles', etc.
    data_source_id UUID REFERENCES data_sources(id) ON DELETE SET NULL,
    style_config JSONB, -- Styling configuration
    is_visible BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE,
    z_index INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default tenant
INSERT INTO tenants (name, slug) VALUES ('Default Tenant', 'default') ON CONFLICT DO NOTHING;

-- Insert default feature flags
INSERT INTO feature_flags (tenant_id, name, enabled, description)
SELECT 
    t.id,
    flag.name,
    flag.enabled,
    flag.description
FROM tenants t, (VALUES
    ('sso_enabled', false, 'Enable Single Sign-On authentication'),
    ('multi_tenant', false, 'Enable multi-tenant functionality'),
    ('realtime_updates', true, 'Enable real-time data updates'),
    ('advanced_filtering', true, 'Enable advanced filtering options')
) AS flag(name, enabled, description)
WHERE t.slug = 'default'
ON CONFLICT DO NOTHING;