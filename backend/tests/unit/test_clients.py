"""
Unit tests for data clients
"""
import pytest
from app.clients.mock_aircraft_client import MockAircraftClient
from app.clients.base_client import BaseDataClient


class TestMockAircraftClient:
    """Test the mock aircraft client"""
    
    @pytest.mark.asyncio
    async def test_fetch_data_returns_list(self):
        """Test that fetch_data returns a list"""
        client = MockAircraftClient()
        data = await client.fetch_data()
        
        assert isinstance(data, list)
        assert len(data) >= 10  # Should generate at least 10 aircraft
        assert len(data) <= 50  # Should generate at most 50 aircraft
    
    @pytest.mark.asyncio
    async def test_fetch_data_structure(self):
        """Test the structure of fetched data"""
        client = MockAircraftClient()
        data = await client.fetch_data()
        
        if data:  # If we have data
            aircraft = data[0]
            
            # Check required fields
            assert "hex" in aircraft
            assert "type" in aircraft
            assert "lat" in aircraft
            assert "lon" in aircraft
            
            # Check hex format
            assert isinstance(aircraft["hex"], str)
            assert len(aircraft["hex"]) == 6
            
            # Check coordinates are valid
            assert -90 <= aircraft["lat"] <= 90
            assert -180 <= aircraft["lon"] <= 180
    
    def test_validate_data_valid_aircraft(self):
        """Test validation with valid aircraft data"""
        client = MockAircraftClient()
        
        valid_aircraft = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "lat": 37.7749,
            "lon": -122.4194
        }
        
        assert client.validate_data(valid_aircraft) is True
    
    def test_validate_data_missing_hex(self):
        """Test validation fails with missing hex"""
        client = MockAircraftClient()
        
        invalid_aircraft = {
            "type": "adsb_icao",
            "lat": 37.7749,
            "lon": -122.4194
        }
        
        assert client.validate_data(invalid_aircraft) is False
    
    def test_validate_data_invalid_hex_length(self):
        """Test validation fails with invalid hex length"""
        client = MockAircraftClient()
        
        invalid_aircraft = {
            "hex": "ae14",  # Too short
            "type": "adsb_icao",
            "lat": 37.7749,
            "lon": -122.4194
        }
        
        assert client.validate_data(invalid_aircraft) is False
    
    def test_validate_data_invalid_coordinates(self):
        """Test validation fails with invalid coordinates"""
        client = MockAircraftClient()
        
        # Invalid latitude
        invalid_aircraft1 = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "lat": 95.0,  # Invalid latitude
            "lon": -122.4194
        }
        assert client.validate_data(invalid_aircraft1) is False
        
        # Invalid longitude
        invalid_aircraft2 = {
            "hex": "ae1460",
            "type": "adsb_icao",
            "lat": 37.7749,
            "lon": 185.0  # Invalid longitude
        }
        assert client.validate_data(invalid_aircraft2) is False
    
    def test_validate_data_missing_coordinates_ok(self):
        """Test validation passes with missing coordinates"""
        client = MockAircraftClient()
        
        valid_aircraft = {
            "hex": "ae1460",
            "type": "adsb_icao"
            # No lat/lon - should still be valid
        }
        
        assert client.validate_data(valid_aircraft) is True
    
    @pytest.mark.asyncio
    async def test_process_data_integration(self):
        """Test the complete process_data workflow"""
        client = MockAircraftClient()
        processed_data = await client.process_data()
        
        assert isinstance(processed_data, list)
        
        # All processed data should be valid
        for aircraft in processed_data:
            assert client.validate_data(aircraft) is True


class TestBaseDataClient:
    """Test the base data client abstract class"""
    
    def test_base_client_is_abstract(self):
        """Test that BaseDataClient cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseDataClient()
    
    def test_base_client_subclass_must_implement_methods(self):
        """Test that subclasses must implement abstract methods"""
        
        class IncompleteClient(BaseDataClient):
            # Missing implementation of abstract methods
            pass
        
        with pytest.raises(TypeError):
            IncompleteClient()
    
    def test_base_client_complete_implementation(self):
        """Test that complete implementation works"""
        
        class CompleteClient(BaseDataClient):
            async def fetch_data(self):
                return [{"test": "data"}]
            
            def validate_data(self, data):
                return "test" in data
        
        # Should be able to instantiate
        client = CompleteClient()
        assert client is not None
        
        # Should have config attribute
        assert hasattr(client, 'config')
        assert client.config == {}
    
    @pytest.mark.asyncio
    async def test_base_client_process_data_workflow(self):
        """Test the process_data workflow in base client"""
        
        class TestClient(BaseDataClient):
            async def fetch_data(self):
                return [
                    {"valid": True, "data": "test1"},
                    {"invalid": True},  # Will fail validation
                    {"valid": True, "data": "test2"}
                ]
            
            def validate_data(self, data):
                return "valid" in data and data["valid"]
        
        client = TestClient()
        processed = await client.process_data()
        
        # Should only return valid data
        assert len(processed) == 2
        assert all(item["valid"] for item in processed)