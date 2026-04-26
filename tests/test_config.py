import os
import pytest
from typing import List, Optional

from netbox_mcp_server.config import get_settings, Settings

# --- Fixtures ---

@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mocks environment variables for testing."""
    def _mock_env(vars_dict: dict):
        for key, value in vars_dict.items():
            if value is None:
                monkeypatch.delenv(key, raising=False)
            else:
                monkeypatch.setenv(key, str(value))
    return _mock_env

@pytest.fixture
def mock_cli_args():
    """Helper to create mock CLI arguments."""
    def _mock_cli(args: Optional[List[str]] = None) -> Optional[List[str]]:
        return args
    return _mock_cli

# --- Tests ---

def test_get_settings_defaults(mock_env_vars, mock_cli_args):
    """Test that default values are used when no env vars or CLI args are provided."""
    # Ensure no env vars are set that might interfere
    mock_env_vars({'NETBOX_URL': None, 'NETBOX_TOKEN': None})

    # Call get_settings without any arguments
    # This should raise a ValueError because NETBOX_URL and NETBOX_TOKEN are required
    with pytest.raises(ValueError, match="Settings validation failed"):
        get_settings()

def test_get_settings_from_env(mock_env_vars, mock_cli_args):
    """Test that settings are loaded correctly from environment variables."""
    env_vars = {
        'NETBOX_URL': 'http://env.netbox.local',
        'NETBOX_TOKEN': 'env_token_123',
        'TIMEOUT': '60',
        'RATE_LIMIT': '5',
        'BULK_MAX': '200',
        'LOG_LEVEL': 'DEBUG',
    }
    mock_env_vars(env_vars)

    settings = get_settings()

    assert settings.NETBOX_URL == 'http://env.netbox.local'
    assert settings.NETBOX_TOKEN == 'env_token_123'
    assert settings.TIMEOUT == 60
    assert settings.RATE_LIMIT == 5
    assert settings.BULK_MAX == 200
    assert settings.LOG_LEVEL == 'DEBUG'

def test_get_settings_cli_override_env(mock_env_vars, mock_cli_args):
    """Test that CLI arguments override environment variables."""
    env_vars = {
        'NETBOX_URL': 'http://env.netbox.local',
        'NETBOX_TOKEN': 'env_token_123',
        'TIMEOUT': '60',
    }
    mock_env_vars(env_vars)

    cli_args = [
        '--netbox-url', 'http://cli.netbox.local',
        '--timeout', '120',
        '--rate-limit', '20', # This env var is not set, should be taken from CLI
    ]
    settings = get_settings(cli_args=mock_cli_args(cli_args))

    assert settings.NETBOX_URL == 'http://cli.netbox.local' # Overridden
    assert settings.NETBOX_TOKEN == 'env_token_123'      # Not overridden, from env
    assert settings.TIMEOUT == 120                       # Overridden
    assert settings.RATE_LIMIT == 20                       # From CLI, env not set
    assert settings.BULK_MAX == 100                      # Default value
    assert settings.LOG_LEVEL == 'INFO'                  # Default value

def test_get_settings_missing_required_env_and_cli(mock_env_vars, mock_cli_args):
    """Test that ValueError is raised if required env vars and CLI args are missing."""
    mock_env_vars({'NETBOX_URL': None, 'NETBOX_TOKEN': None}) # Ensure they are not set

    # No CLI args provided
    with pytest.raises(ValueError, match="Settings validation failed"):
        get_settings(cli_args=mock_cli_args([]))

    # CLI args provided but missing required ones
    cli_args_partial = ['--timeout', '60']
    with pytest.raises(ValueError, match="Settings validation failed"):
        get_settings(cli_args=mock_cli_args(cli_args_partial))

def test_get_settings_cached(mock_env_vars, mock_cli_args):
    """Test that get_settings returns a cached instance."""
    mock_env_vars({'NETBOX_URL': 'http://cached.netbox.local', 'NETBOX_TOKEN': 'cached_token'})

    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2 # Should be the same instance

    # Modify env vars and check if cache is respected (it should be)
    mock_env_vars({'NETBOX_URL': 'http://new.netbox.local', 'NETBOX_TOKEN': 'new_token'})
    settings3 = get_settings() # Should still return the cached instance from the first call

    # The cached instance should still hold the old values because the cache was not cleared
    # and get_settings was not called with new cli_args to force re-parsing.
    assert settings3.NETBOX_URL == 'http://cached.netbox.local'
    assert settings3.NETBOX_TOKEN == 'cached_token'

    # To get new settings, we need to clear the cache or call with different cli_args
    get_settings.cache_clear()
    settings4 = get_settings()
    assert settings4 is not settings3
    assert settings4.NETBOX_URL == 'http://new.netbox.local'
    assert settings4.NETBOX_TOKEN == 'new_token'

def test_get_settings_cli_only(mock_env_vars, mock_cli_args):
    """Test settings loading when only CLI args are provided (no env vars)."""
    mock_env_vars({'NETBOX_URL': None, 'NETBOX_TOKEN': None}) # Ensure no env vars

    cli_args = [
        '--netbox-url', 'http://cli-only.netbox.local',
        '--netbox-token', 'cli_only_token',
        '--log-level', 'WARNING',
    ]
    settings = get_settings(cli_args=mock_cli_args(cli_args))

    assert settings.NETBOX_URL == 'http://cli-only.netbox.local'
    assert settings.NETBOX_TOKEN == 'cli_only_token'
    assert settings.LOG_LEVEL == 'WARNING'
    assert settings.TIMEOUT == 30 # Default
    assert settings.RATE_LIMIT == 10 # Default
    assert settings.BULK_MAX == 100 # Default
