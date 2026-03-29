"""Utils module initialization."""
import sys
from pathlib import Path

# Add backend to path for imports
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from utils.logger import setup_logger

__all__ = ["setup_logger"]
