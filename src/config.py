import os

TRUTHY = {"1", "true", "yes", "on"}


def get_db_config():
    """Build the MySQL connection settings from environment variables.

    Credentials must never be hardcoded here; set them in the environment or a
    local `.env` file (see `.env.example`).
    """
    password = os.getenv("EDUTRACK_DB_PASSWORD")
    if not password and os.getenv("EDUTRACK_ALLOW_EMPTY_PASSWORD", "").lower() not in TRUTHY:
        raise RuntimeError(
            "EDUTRACK_DB_PASSWORD is not set. Export it (or add it to your local .env) "
            "before starting EduTrack. Set EDUTRACK_ALLOW_EMPTY_PASSWORD=1 only for a "
            "throwaway local database with no password."
        )

    config = {
        "host": os.getenv("EDUTRACK_DB_HOST", "localhost"),
        "user": os.getenv("EDUTRACK_DB_USER", "root"),
        "password": password or "",
        "database": os.getenv("EDUTRACK_DB_NAME", "edutrack"),
        "port": int(os.getenv("EDUTRACK_DB_PORT", "3306")),
    }

    ssl_ca = os.getenv("EDUTRACK_DB_SSL_CA")
    if ssl_ca:
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_identity"] = True

    return config
