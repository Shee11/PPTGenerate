"""Tests for Source and SourceReference models."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.common.source import Source, SourceReference


class TestSourceReference:
    """Test SourceReference validation."""
    
    def test_valid_source_reference(self):
        """Verify valid SourceReference with all fields."""
        ref = SourceReference(
            source_id="550e8400-e29b-41d4-a716-446655440000",
            file_path="/path/to/file.txt",
            offset=100,
            length=50,
            line_number=10
        )
        
        assert ref.source_id == "550e8400-e29b-41d4-a716-446655440000"
        assert ref.offset == 100
        assert ref.length == 50
        assert ref.line_number == 10
    
    def test_source_reference_without_line_number(self):
        """Verify SourceReference with optional line_number as None."""
        ref = SourceReference(
            source_id="test-id",
            file_path="/path/file.txt",
            offset=0,
            length=10
        )
        
        assert ref.line_number is None
    
    def test_offset_validation(self):
        """Verify offset must be non-negative."""
        # Valid offset
        SourceReference(
            source_id="id",
            file_path="path",
            offset=0,
            length=10
        )
        
        # Invalid offset
        with pytest.raises(ValidationError):
            SourceReference(
                source_id="id",
                file_path="path",
                offset=-1,
                length=10
            )
    
    def test_length_validation(self):
        """Verify length must be positive."""
        # Valid length
        SourceReference(
            source_id="id",
            file_path="path",
            offset=0,
            length=1
        )
        
        # Invalid length (zero)
        with pytest.raises(ValidationError):
            SourceReference(
                source_id="id",
                file_path="path",
                offset=0,
                length=0
            )
        
        # Invalid length (negative)
        with pytest.raises(ValidationError):
            SourceReference(
                source_id="id",
                file_path="path",
                offset=0,
                length=-5
            )
    
    def test_line_number_validation(self):
        """Verify line_number must be >= 1 if provided."""
        # Valid line number
        SourceReference(
            source_id="id",
            file_path="path",
            offset=0,
            length=10,
            line_number=1
        )
        
        # Invalid line number (zero)
        with pytest.raises(ValidationError):
            SourceReference(
                source_id="id",
                file_path="path",
                offset=0,
                length=10,
                line_number=0
            )
        
        # Invalid line number (negative)
        with pytest.raises(ValidationError):
            SourceReference(
                source_id="id",
                file_path="path",
                offset=0,
                length=10,
                line_number=-1
            )


class TestSource:
    """Test Source model validation."""
    
    def test_valid_text_source(self):
        """Verify valid Source with text/plain content."""
        source = Source(
            source_id="550e8400-e29b-41d4-a716-446655440000",
            name="test.txt",
            file_path="/path/to/test.txt",
            content_type="text/plain",
            content="Test content here",
            metadata={"file_size": 100, "encoding": "utf-8"}
        )
        
        assert source.source_id == "550e8400-e29b-41d4-a716-446655440000"
        assert source.name == "test.txt"
        assert source.content_type == "text/plain"
        assert source.content == "Test content here"
        assert isinstance(source.created_at, datetime)
    
    def test_valid_vtt_source(self):
        """Verify valid Source with text/vtt content."""
        source = Source(
            source_id="test-id",
            name="subtitles.vtt",
            file_path="/path/to/subtitles.vtt",
            content_type="text/vtt",
            content="WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nHello world"
        )
        
        assert source.content_type == "text/vtt"
    
    def test_content_type_validation(self):
        """Verify content_type must be text/plain or text/vtt."""
        # Valid types
        Source(
            source_id="id1",
            name="file.txt",
            file_path="/path/file.txt",
            content_type="text/plain",
            content="content"
        )
        
        Source(
            source_id="id2",
            name="file.vtt",
            file_path="/path/file.vtt",
            content_type="text/vtt",
            content="content"
        )
        
        # Invalid type
        with pytest.raises(ValidationError):
            Source(
                source_id="id",
                name="file.pdf",
                file_path="/path/file.pdf",
                content_type="application/pdf",
                content="content"
            )
    
    def test_content_not_empty(self):
        """Verify content must not be empty string."""
        # Valid content
        Source(
            source_id="id",
            name="file.txt",
            file_path="/path/file.txt",
            content_type="text/plain",
            content="Some content"
        )
        
        # Invalid empty content
        with pytest.raises(ValidationError):
            Source(
                source_id="id",
                name="file.txt",
                file_path="/path/file.txt",
                content_type="text/plain",
                content=""
            )
    
    def test_created_at_auto_generated(self):
        """Verify created_at is automatically set if not provided."""
        before = datetime.utcnow()
        
        source = Source(
            source_id="id",
            name="file.txt",
            file_path="/path/file.txt",
            content_type="text/plain",
            content="content"
        )
        
        after = datetime.utcnow()
        
        assert before <= source.created_at <= after
    
    def test_metadata_optional(self):
        """Verify metadata field is optional."""
        source = Source(
            source_id="id",
            name="file.txt",
            file_path="/path/file.txt",
            content_type="text/plain",
            content="content"
        )
        
        assert source.metadata == {}
    
    def test_metadata_with_custom_data(self):
        """Verify metadata can store arbitrary key-value pairs."""
        metadata = {
            "file_size": 1024,
            "encoding": "utf-8",
            "language": "en",
            "custom_field": "custom_value"
        }
        
        source = Source(
            source_id="id",
            name="file.txt",
            file_path="/path/file.txt",
            content_type="text/plain",
            content="content",
            metadata=metadata
        )
        
        assert source.metadata == metadata
