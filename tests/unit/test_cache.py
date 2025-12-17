"""Tests for GenerationCache filesystem-based caching."""
import pytest
import json
import hashlib
from pathlib import Path
from src.utils.cache import GenerationCache


class TestGenerationCache:
    """Test hash-based filesystem caching."""
    
    def test_hash_key_generation(self, tmp_path):
        """Verify hash_key generates consistent SHA256 hashes."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        prompt = "Extract atoms"
        content = "Test content"
        
        key1 = cache.hash_key(prompt, content)
        key2 = cache.hash_key(prompt, content)
        
        # Same inputs produce same hash
        assert key1 == key2
        assert len(key1) == 64  # SHA256 produces 64 hex characters
        
        # Different inputs produce different hashes
        key3 = cache.hash_key(prompt, "Different content")
        assert key1 != key3
    
    def test_hash_key_deterministic(self, tmp_path):
        """Verify hash is deterministic across cache instances."""
        cache1 = GenerationCache(cache_dir=tmp_path)
        cache2 = GenerationCache(cache_dir=tmp_path)
        
        key1 = cache1.hash_key("prompt", "content")
        key2 = cache2.hash_key("prompt", "content")
        
        assert key1 == key2
    
    def test_save_creates_subdirectory(self, tmp_path):
        """Verify save creates subdirectory based on first 2 chars of hash."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        test_data = {"atoms": ["atom1", "atom2"]}
        key = cache.hash_key("test", "data")
        
        cache.save(key, test_data)
        
        # Check subdirectory exists (first 2 chars of hash)
        subdir = tmp_path / key[:2]
        assert subdir.exists()
        assert subdir.is_dir()
        
        # Check file exists
        cache_file = subdir / f"{key}.json"
        assert cache_file.exists()
    
    def test_save_and_load_roundtrip(self, tmp_path):
        """Verify data saved can be loaded back correctly."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        original_data = {
            "atoms": [
                {"id": "atom1", "type": "statement", "text": "Test"},
                {"id": "atom2", "type": "process", "steps": [1, 2, 3]}
            ],
            "metadata": {"count": 2}
        }
        
        key = cache.hash_key("extract", "source content")
        cache.save(key, original_data)
        
        loaded_data = cache.load(key)
        assert loaded_data == original_data
    
    def test_load_cache_miss_returns_none(self, tmp_path):
        """Verify load returns None when cache key doesn't exist."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        nonexistent_key = "a" * 64  # Valid hash format but doesn't exist
        result = cache.load(nonexistent_key)
        
        assert result is None
    
    def test_load_invalid_json_returns_none(self, tmp_path):
        """Verify load returns None when cache file contains invalid JSON."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        key = cache.hash_key("test", "data")
        subdir = tmp_path / key[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        
        # Write invalid JSON
        cache_file = subdir / f"{key}.json"
        cache_file.write_text("invalid json {]}")
        
        result = cache.load(key)
        assert result is None
    
    def test_cache_hit_and_miss(self, tmp_path):
        """Verify cache hit/miss behavior."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        key = cache.hash_key("prompt", "content")
        
        # Cache miss initially
        assert cache.load(key) is None
        
        # Save data
        test_data = {"result": "success"}
        cache.save(key, test_data)
        
        # Cache hit after save
        result = cache.load(key)
        assert result == test_data
    
    def test_multiple_cache_entries(self, tmp_path):
        """Verify multiple cache entries can coexist."""
        cache = GenerationCache(cache_dir=tmp_path)
        
        entries = [
            ("prompt1", "content1", {"data": 1}),
            ("prompt2", "content2", {"data": 2}),
            ("prompt3", "content3", {"data": 3}),
        ]
        
        # Save all entries
        keys = []
        for prompt, content, data in entries:
            key = cache.hash_key(prompt, content)
            keys.append(key)
            cache.save(key, data)
        
        # Verify all can be loaded
        for i, key in enumerate(keys):
            loaded = cache.load(key)
            assert loaded == {"data": i + 1}
    
    def test_cache_dir_creation(self, tmp_path):
        """Verify cache directory is created if it doesn't exist."""
        cache_dir = tmp_path / "nonexistent" / "cache"
        assert not cache_dir.exists()
        
        cache = GenerationCache(cache_dir=cache_dir)
        key = cache.hash_key("test", "data")
        cache.save(key, {"test": "data"})
        
        assert cache_dir.exists()
    
    def test_default_cache_dir(self):
        """Verify default cache directory is .cache."""
        cache = GenerationCache()
        assert cache.cache_dir == Path(".cache")
