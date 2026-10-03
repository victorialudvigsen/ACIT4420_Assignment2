class InvalidIdentifierError(ValueError):
    """Raised when a participant or session ID has an invalid format."""


class InvalidRecordError(ValueError):
    """Raised when a CSV record contains invalid data."""

    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field