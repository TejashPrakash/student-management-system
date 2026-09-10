import os
from pathlib import Path

from dotenv import load_dotenv

from errors import ConfigurationError

# Load variables from a local .env at the repository root when present.
# Real environment variables take precedence over values in the file.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

TRUTHY = {"1", "true", "yes", "on"}


def get_db_config():
    """Build the MySQL connection settings from environment variables.

    Credentials must never be hardcoded here; set them in the environment or a
    local `.env` file (see `.env.example`).

    Raises:
        ConfigurationError: a required setting is missing or malformed.
    """
    password = os.getenv("EDUTRACK_DB_PASSWORD")
    if not password and os.getenv("EDUTRACK_ALLOW_EMPTY_PASSWORD", "").lower() not in TRUTHY:
        raise ConfigurationError(
            "EDUTRACK_DB_PASSWORD is not set. Export it (or add it to your local .env) "
            "before starting EduTrack. Set EDUTRACK_ALLOW_EMPTY_PASSWORD=1 only for a "
            "throwaway local database with no password."
        )

    raw_port = os.getenv("EDUTRACK_DB_PORT", "3306")
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ConfigurationError(
            f"EDUTRACK_DB_PORT must be an integer, got {raw_port!r}."
        ) from exc

    config = {
        "host": os.getenv("EDUTRACK_DB_HOST", "localhost"),
        "user": os.getenv("EDUTRACK_DB_USER", "root"),
        "password": password or "",
        "database": os.getenv("EDUTRACK_DB_NAME", "edutrack"),
        "port": port,
    }

    ssl_ca = os.getenv("EDUTRACK_DB_SSL_CA")
    if ssl_ca:
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_identity"] = True

    return config
