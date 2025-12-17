from pathlib import Path  # Line 1: Import Path class (no alias - clearer)
import logging
import os  # Added: For os.access permission checking

logger = logging.getLogger(__name__)

# Use absolute paths, not relative
# Path.cwd() gets current working directory
# .parent goes up one level (if your structure is bootmgr/src/config.py)
BOOTMGR_ROOT = Path.cwd().parent  # Goes from src/ to bootmgr/
PROJECTS_DIR = BOOTMGR_ROOT / "projects"
LOGS_DIR = BOOTMGR_ROOT / "logs"
STATE_FILE = BOOTMGR_ROOT / "state"

SCHEMA_VERSION = "v1.0"

def ensure_dirs():
    """Ensure all required directories exist with proper permissions."""
    
    # not BOOTMGR_ROOT.exists() = True when directory DOESN'T exist
    if not BOOTMGR_ROOT.exists():
        logger.error(f'Root project directory not found: {BOOTMGR_ROOT}')
        raise FileNotFoundError(f'Bootcamp root directory not found: {BOOTMGR_ROOT}')
    
    # Check if we have read/write permissions
    if not os.access(BOOTMGR_ROOT, os.R_OK | os.W_OK):
        logger.error(f'No read/write permissions for: {BOOTMGR_ROOT}')
        raise PermissionError(f'Cannot access: {BOOTMGR_ROOT}')
    
    # Create directories (exist_ok=True means no error if already exists)
    PROJECTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    logger.info(f'Directories ensured in: {BOOTMGR_ROOT}')
    return True  # Success indicator