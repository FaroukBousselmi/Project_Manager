# python -m pytest tests/test_config.py -v
from pathlib import Path
import pytest
import tempfile
import sys  # Access Python system paths
import os  # Operating system functions

# Tell Python where to find our code
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the module we're testing
from src.config import ensure_dirs

# TEST 1 - Should work with existing directory
def test_ensure_dirs_with_existing_root():
    """
    Test that ensure_dirs() works when root directory exists.
    """
    # Create a temporary directory (auto-cleaned after test)
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory
        original_dir = os.getcwd()  # Save current directory
        os.chdir(tmpdir)  # Move to temp dir
        
        # THE TEST: Call ensure_dirs() - should work
        result = ensure_dirs()
        
        # VERIFY: Should return None (or not -1 for error)
        assert result != -1, "ensure_dirs() returned -1 (error) with valid directory!"
        
        # Cleanup: Return to original directory
        os.chdir(original_dir)
    
    # tests/test_config.py - ADD THIS TEST

def test_ensure_dirs_with_missing_root():
    """
    Test that ensure_dirs() FAILS when root doesn't exist.
    """
    import tempfile
    
    # Create and immediately delete a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        missing_dir = os.path.join(tmpdir, "nonexistent")
        
        # We expect FileNotFoundError to be raised
        with pytest.raises(FileNotFoundError) as exc_info:
            # Temporarily change BOOTMGR_ROOT for test
            import src.config
            original_root = src.config.BOOTMGR_ROOT
            src.config.BOOTMGR_ROOT = Path(missing_dir)
            
            src.config.ensure_dirs()
            
            # Restore original
            src.config.BOOTMGR_ROOT = original_root
        
        # Verify error message contains path
        assert "not found" in str(exc_info.value)
    
def test_ensure_dirs_creates_required_folders():
    """
    Test that projects/ and logs/ directories are created.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        import src.config
        
        # Setup test
        original_root = src.config.BOOTMGR_ROOT
        src.config.BOOTMGR_ROOT = Path(tmpdir)
        
        # Execute
        result = src.config.ensure_dirs()
        
        # Verify
        projects_path = Path(tmpdir) / "projects"
        logs_path = Path(tmpdir) / "logs"
        
        assert projects_path.exists(), "projects/ directory was not created!"
        assert logs_path.exists(), "logs/ directory was not created!"
        assert result == True, "Function should return True on success"
        
        # Cleanup
        src.config.BOOTMGR_ROOT = original_root    