"""
Example unit tests to ensure the testing pipeline works
"""
import pytest
from app.core.config import settings


class TestExamplePassing:
    """Example test class that demonstrates passing tests"""
    
    def test_basic_assertion(self):
        """Test that basic assertions work"""
        assert True
        assert 1 + 1 == 2
        assert "hello" == "hello"
    
    def test_string_operations(self):
        """Test string operations"""
        text = "SkyTrace"
        assert text.lower() == "skytrace"
        assert text.upper() == "SKYTRACE"
        assert len(text) == 8
    
    def test_list_operations(self):
        """Test list operations"""
        aircraft_types = ["B738", "A320", "B777", "A350"]
        assert len(aircraft_types) == 4
        assert "B738" in aircraft_types
        assert "C172" not in aircraft_types
    
    def test_dictionary_operations(self):
        """Test dictionary operations"""
        aircraft = {
            "hex": "ae1460",
            "flight": "TEST123",
            "altitude": 10000
        }
        assert aircraft["hex"] == "ae1460"
        assert aircraft.get("flight") == "TEST123"
        assert aircraft.get("missing", None) is None
    
    def test_settings_import(self):
        """Test that settings can be imported and accessed"""
        assert hasattr(settings, 'DATABASE_URL')
        assert hasattr(settings, 'ENVIRONMENT')
        assert hasattr(settings, 'LOG_LEVEL')


class TestExampleMath:
    """Example math tests"""
    
    def test_addition(self):
        """Test addition"""
        assert 2 + 2 == 4
        assert 10 + 5 == 15
    
    def test_subtraction(self):
        """Test subtraction"""
        assert 10 - 5 == 5
        assert 0 - 1 == -1
    
    def test_multiplication(self):
        """Test multiplication"""
        assert 3 * 4 == 12
        assert 5 * 0 == 0
    
    def test_division(self):
        """Test division"""
        assert 10 / 2 == 5
        assert 15 / 3 == 5
    
    def test_division_by_zero(self):
        """Test that division by zero raises an error"""
        with pytest.raises(ZeroDivisionError):
            1 / 0


class TestExampleAsync:
    """Example async tests"""
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        """Test async function"""
        async def async_add(a, b):
            return a + b
        
        result = await async_add(2, 3)
        assert result == 5
    
    @pytest.mark.asyncio
    async def test_async_with_delay(self):
        """Test async function with delay"""
        import asyncio
        
        async def delayed_return(value, delay=0.01):
            await asyncio.sleep(delay)
            return value
        
        result = await delayed_return("test")
        assert result == "test"


class TestExampleParametrized:
    """Example parametrized tests"""
    
    @pytest.mark.parametrize("input_val,expected", [
        ("adsb_icao", True),
        ("mode_s", True),
        ("tisb", True),
        ("mlat", True),
        ("invalid", False),
    ])
    def test_aircraft_type_validation(self, input_val, expected):
        """Test aircraft type validation"""
        valid_types = ["adsb_icao", "mode_s", "tisb", "mlat"]
        result = input_val in valid_types
        assert result == expected
    
    @pytest.mark.parametrize("hex_code,is_valid", [
        ("ae1460", True),
        ("ABCDEF", True),
        ("123456", True),
        ("ae146", False),  # Too short
        ("ae14601", False),  # Too long
        ("zzzzzz", False),  # Invalid hex
    ])
    def test_hex_code_validation(self, hex_code, is_valid):
        """Test hex code validation"""
        result = len(hex_code) == 6 and all(c in "0123456789ABCDEFabcdef" for c in hex_code)
        assert result == is_valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])