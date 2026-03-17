import os
from joblib import Memory

# Create a joblib Memory instance in the local cache directory
# This allows caching expensive computations between runs.
CACHE_DIR = os.environ.get("STATFORGE_CACHE_DIR", ".statforge_cache")
cache = Memory(CACHE_DIR, verbose=0)
