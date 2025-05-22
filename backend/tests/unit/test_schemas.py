"""
Unit tests for Pydantic schemas
"""
import pytest
from pydantic import ValidationError
from app.schemas.aircraft import AircraftCreate, AircraftUpdate
from app.schemas.tenant import TenantCreate
from app.schemas.feature_flag import FeatureFlagCreate


class TestAircraftSchemas:
    """Test aircraft Pydantic schemas"""
    
    def test_aircraft_create_valid_data(self, sample_aircraft_data):
        """Test creating aircraft with valid data"""
        aircraft = AircraftCreate(**sample_aircraft_data)
        assert aircraft.hex == "ae1460"
        assert aircraft.type == "adsb_icao"
        assert aircraft.flight == "TEST123"
        assert aircraft.latitude == 37.7749
        assert aircraft.longitude == -122.4194
    
    def test_aircraft_create_minimal_data(self):
        """Test creating aircraft with minimal required data"""
        minimal_data = {
            "hex": "ae1460",
            "type": "adsb_icao"
        }
        aircraft = AircraftCreate(**minimal_data)
        assert aircraft.hex == "ae1460"
        assert aircraft.type == "adsb_icao"
        assert aircraft.flight is None
        assert aircraft.latitude is None
    
    def test_aircraft_create_invalid_hex_length(self):
        """Test that invalid hex length raises validation error"""
        invalid_data = {
            "hex": "ae146",  # Too short
            "type": "adsb_icao"
        }
        with pytest.raises(ValidationError) as exc_info:
            AircraftCreate(**invalid_data)
        
        errors = exc_info.value.errors()
        assert any("at least 6 characters" in str(error) for error in errors)
    
    def test_aircraft_create_invalid_latitude(self):
        """Test that invalid latitude raises validation error"""
        invalid_data = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "latitude": 95.0  # Invalid latitude > 90
        }
        with pytest.raises(ValidationError) as exc_info:
            AircraftCreate(**invalid_data)
        
        errors = exc_info.value.errors()
        assert any("less than or equal to 90" in str(error) for error in errors)
    
    def test_aircraft_create_invalid_longitude(self):
        """Test that invalid longitude raises validation error"""
        invalid_data = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "longitude": 185.0  # Invalid longitude > 180
        }
        with pytest.raises(ValidationError) as exc_info:
            AircraftCreate(**invalid_data)
        
        errors = exc_info.value.errors()
        assert any("less than or equal to 180" in str(error) for error in errors)
    
    def test_aircraft_update_partial_data(self):
        """Test updating aircraft with partial data"""
        update_data = {
            "flight": "UPDATED123",
            "altitude_baro": 15000
        }
        aircraft_update = AircraftUpdate(**update_data)
        assert aircraft_update.flight == "UPDATED123"
        assert aircraft_update.altitude_baro == 15000
        assert aircraft_update.hex is None  # Not provided, should be None


class TestTenantSchemas:
    """Test tenant Pydantic schemas"""
    
    def test_tenant_create_valid_data(self):
        """Test creating tenant with valid data"""
        tenant_data = {
            "name": "Test Organization",
            "slug": "test-org",
            "is_active": True
        }
        tenant = TenantCreate(**tenant_data)
        assert tenant.name == "Test Organization"
        assert tenant.slug == "test-org"
        assert tenant.is_active is True
    
    def test_tenant_create_minimal_data(self):
        """Test creating tenant with minimal data"""
        tenant_data = {
            "name": "Test",
            "slug": "test"
        }
        tenant = TenantCreate(**tenant_data)
        assert tenant.name == "Test"
        assert tenant.slug == "test"
        assert tenant.is_active is True  # Default value
    
    def test_tenant_create_empty_name(self):
        """Test that empty name raises validation error"""
        tenant_data = {
            "name": "",
            "slug": "test"
        }
        with pytest.raises(ValidationError) as exc_info:
            TenantCreate(**tenant_data)
        
        errors = exc_info.value.errors()
        assert any("at least 1 character" in str(error) for error in errors)


class TestFeatureFlagSchemas:
    """Test feature flag Pydantic schemas"""
    
    def test_feature_flag_create_valid_data(self):
        """Test creating feature flag with valid data"""
        flag_data = {
            "name": "test_feature",
            "enabled": True,
            "description": "Test feature flag"
        }
        flag = FeatureFlagCreate(**flag_data)
        assert flag.name == "test_feature"
        assert flag.enabled is True
        assert flag.description == "Test feature flag"
    
    def test_feature_flag_create_minimal_data(self):
        """Test creating feature flag with minimal data"""
        flag_data = {
            "name": "test_feature"
        }
        flag = FeatureFlagCreate(**flag_data)
        assert flag.name == "test_feature"
        assert flag.enabled is False  # Default value
        assert flag.description is None
    
    def test_feature_flag_create_empty_name(self):
        """Test that empty name raises validation error"""
        flag_data = {
            "name": ""
        }
        with pytest.raises(ValidationError) as exc_info:
            FeatureFlagCreate(**flag_data)
        
        errors = exc_info.value.errors()
        assert any("at least 1 character" in str(error) for error in errors)