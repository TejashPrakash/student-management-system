"""Exception types used across EduTrack."""


class EduTrackError(Exception):
    """Base class for every error raised by EduTrack."""


class ConfigurationError(EduTrackError):
    """Raised when the database configuration is missing or invalid."""


class DatabaseConnectionError(EduTrackError):
    """Raised when a connection to the database cannot be established."""


class StudentRepositoryError(EduTrackError):
    """Raised when a student query or command fails."""
