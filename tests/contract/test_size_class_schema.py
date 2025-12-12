"""Contract tests for SizeClass enum schema validation."""
import pytest
from pydantic import BaseModel, ValidationError
from src.common.size_class import SizeClass


class TestSizeClassSchema:
    """Test SizeClass enum schema and validation."""
    
    def test_size_class_enum_values(self) -> None:
        """Test that SizeClass has correct enum values."""
        assert SizeClass.S.value == 1
        assert SizeClass.M.value == 2
        assert SizeClass.L.value == 3
        assert SizeClass.XL.value == 4
    
    def test_size_class_ordering(self) -> None:
        """Test that size classes can be compared."""
        assert SizeClass.S < SizeClass.M
        assert SizeClass.M < SizeClass.L
        assert SizeClass.L < SizeClass.XL
        assert SizeClass.XL > SizeClass.S
    
    def test_size_class_in_pydantic_model(self) -> None:
        """Test that SizeClass works in Pydantic models."""
        
        class TestModel(BaseModel):
            size: SizeClass
        
        # Valid creation
        model = TestModel(size=SizeClass.M)
        assert model.size == SizeClass.M
        
        # Integer value conversion should work
        model2 = TestModel(size=3)  # L has value 3
        assert model2.size == SizeClass.L
    
    def test_size_class_from_string(self) -> None:
        """Test creating SizeClass from string."""
        assert SizeClass.from_string("S") == SizeClass.S
        assert SizeClass.from_string("M") == SizeClass.M
        assert SizeClass.from_string("L") == SizeClass.L
        assert SizeClass.from_string("XL") == SizeClass.XL
        
        # Case insensitive
        assert SizeClass.from_string("s") == SizeClass.S
        assert SizeClass.from_string("xl") == SizeClass.XL
    
    def test_size_class_invalid_string(self) -> None:
        """Test that invalid strings raise ValueError."""
        with pytest.raises(ValueError, match="Invalid size"):
            SizeClass.from_string("INVALID")
        
        with pytest.raises(ValueError, match="Invalid size"):
            SizeClass.from_string("XXL")
    
    def test_size_class_string_representation(self) -> None:
        """Test string representation of SizeClass."""
        assert str(SizeClass.S) == "S"
        assert str(SizeClass.M) == "M"
        assert str(SizeClass.L) == "L"
        assert str(SizeClass.XL) == "XL"
