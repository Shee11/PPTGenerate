"""Hash-based filesystem cache for LLM responses."""
import json
import hashlib
from pathlib import Path
from typing import Optional, Any


class GenerationCache:
    """
    Filesystem-based cache for LLM generation results.
    
    Uses SHA256 hashing of (prompt + content) as cache keys.
    Stores cached responses as JSON files in subdirectories based on
    first 2 characters of hash (for better filesystem performance).
    
    Attributes:
        cache_dir: Root directory for cache storage
    """
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache with specified directory.
        
        Args:
            cache_dir: Cache root directory (default: .cache)
        """
        self.cache_dir = cache_dir if cache_dir is not None else Path(".cache")
    
    def hash_key(self, prompt: str, input_content: str) -> str:
        """
        Generate SHA256 hash key from prompt and input content.
        
        Args:
            prompt: LLM prompt text
            input_content: Input content being processed
            
        Returns:
            str: 64-character hexadecimal SHA256 hash
        """
        combined = f"{prompt}||{input_content}"
        return hashlib.sha256(combined.encode('utf-8')).hexdigest()
    
    def save(self, key: str, data: dict) -> None:
        """
        Save data to cache with given key.
        
        Creates subdirectory based on first 2 characters of key
        for better filesystem performance with many cache entries.
        
        Args:
            key: Cache key (SHA256 hash)
            data: Data to cache (must be JSON-serializable)
        """
        # Create subdirectory based on first 2 chars of hash
        subdir = self.cache_dir / key[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        
        # Write data as JSON
        cache_file = subdir / f"{key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, key: str) -> Optional[dict]:
        """
        Load data from cache by key.
        
        Args:
            key: Cache key (SHA256 hash)
            
        Returns:
            dict: Cached data if found, None if cache miss or invalid JSON
        """
        subdir = self.cache_dir / key[:2]
        cache_file = subdir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # Return None on invalid JSON or read errors
            return None
