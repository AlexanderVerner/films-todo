"""Test that SECRET_KEY and DEBUG are read from environment variables."""
import os
import sys
from pathlib import Path


def test_secret_key_from_env(monkeypatch):
    """Test that SECRET_KEY is read from environment variable."""
    # Set a custom SECRET_KEY in environment
    custom_secret = "test-secret-key-12345"
    monkeypatch.setenv("SECRET_KEY", custom_secret)
    
    # Remove the cached module to force reload
    if "_project_.settings" in sys.modules:
        del sys.modules["_project_.settings"]
    
    # Import settings after setting env var
    from _project_ import settings
    
    # Verify SECRET_KEY comes from environment
    assert settings.SECRET_KEY == custom_secret


def test_debug_from_env_true(monkeypatch):
    """Test that DEBUG is read from environment variable (true case)."""
    monkeypatch.setenv("DEBUG", "true")
    
    # Remove the cached module to force reload
    if "_project_.settings" in sys.modules:
        del sys.modules["_project_.settings"]
    
    from _project_ import settings
    
    assert settings.DEBUG is True


def test_debug_from_env_false(monkeypatch):
    """Test that DEBUG is read from environment variable (false case)."""
    monkeypatch.setenv("DEBUG", "false")
    
    # Remove the cached module to force reload
    if "_project_.settings" in sys.modules:
        del sys.modules["_project_.settings"]
    
    from _project_ import settings
    
    assert settings.DEBUG is False


def test_secret_key_default_when_not_set(monkeypatch):
    """Test that SECRET_KEY has a safe default when not set."""
    # Unset SECRET_KEY if it exists
    monkeypatch.delenv("SECRET_KEY", raising=False)
    
    # Remove the cached module to force reload
    if "_project_.settings" in sys.modules:
        del sys.modules["_project_.settings"]
    
    from _project_ import settings
    
    # Should use the default (dev) secret key
    assert "dev" in settings.SECRET_KEY.lower() or "secret" in settings.SECRET_KEY.lower()


def test_debug_default_false_when_not_set(monkeypatch):
    """Test that DEBUG defaults to False when not set in environment."""
    # Unset DEBUG if it exists
    monkeypatch.delenv("DEBUG", raising=False)
    
    # Remove the cached module to force reload
    if "_project_.settings" in sys.modules:
        del sys.modules["_project_.settings"]
    
    from _project_ import settings
    
    # Should default to False
    assert settings.DEBUG is False


def test_test_database_isolation():
    """Test that test settings use isolated database name to prevent data loss."""
    from todo.tests import settings as test_settings
    
    # Test database should use separate name, not production database
    test_db_name = test_settings.DATABASES["default"]["NAME"]
    
    # Should contain "_test" suffix or be explicitly set via TEST_POSTGRES_DATABASE_NAME
    assert "_test" in test_db_name or test_db_name != test_settings.POSTGRES_DATABASE_NAME
    
    # Verify it's different from production database name
    assert test_db_name != test_settings.POSTGRES_DATABASE_NAME
