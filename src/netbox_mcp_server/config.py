import os
import argparse
from typing import Optional, List, Dict, Any
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict, Field, ValidationError

class Settings(BaseSettings):
    NETBOX_URL: str
    NETBOX_TOKEN: str
    TIMEOUT: int = 30
    RATE_LIMIT: int = 10
    BULK_MAX: int = 100
    LOG_LEVEL: str = 'INFO'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

@lru_cache(maxsize=1)
def get_settings(cli_args: Optional[List[str]] = None) -> Settings:
    """
    Loads application settings.

    Settings are loaded from environment variables by default.
    CLI arguments can override environment variables.

    Args:
        cli_args: A list of strings representing command-line arguments.
                  If None, no CLI arguments are parsed, and settings rely solely on env vars.

    Returns:
        A cached Settings instance.

    Raises:
        ValueError: If required settings (NETBOX_URL, NETBOX_TOKEN) are missing.
    """
    settings_kwargs: Dict[str, Any] = {}

    if cli_args is not None:
        parser = argparse.ArgumentParser(description="Netbox MCP Server Settings")
        parser.add_argument('--netbox-url', type=str, help='Netbox API URL')
        parser.add_argument('--netbox-token', type=str, help='Netbox API Token')
        parser.add_argument('--timeout', type=int, help='Request timeout in seconds')
        parser.add_argument('--rate-limit', type=int, help='API rate limit per second')
        parser.add_argument('--bulk-max', type=int, help='Maximum items for bulk operations')
        parser.add_argument('--log-level', type=str, help='Logging level (e.g., INFO, DEBUG)')

        # Parse arguments. If cli_args is provided, use it.
        args = parser.parse_args(cli_args)

        # Convert argparse Namespace to a dictionary, filtering out None values
        settings_kwargs = {k: v for k, v in vars(args).items() if v is not None}

    # Instantiate Settings. BaseSettings automatically loads from env vars.
    # Providing a dictionary to the constructor will override env vars.
    # Pydantic will raise ValidationError if required fields are missing.
    try:
        settings = Settings(**settings_kwargs)
        return settings
    except ValidationError as e:
        # Re-raise as ValueError for broader compatibility or specific error handling if needed.
        # Pydantic's ValidationError is a subclass of ValueError.
        raise ValueError(f"Settings validation failed: {e}") from e
