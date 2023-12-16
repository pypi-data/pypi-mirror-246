class SkycordException(Exception):
    """Base exception class for all Skycord exceptions."""


class MissingDiscordLibrary(SkycordException):
    """Raised when no discord library is found."""

    def __init__(self):
        super().__init__("No discord library found. Please install a supported library.")


class ConvertTimeError(SkycordException):
    """Raised when a time conversion fails."""


class Blacklisted(SkycordException):
    """Can be raised when a blacklisted user tries to use a command.

    This error can be caught in a command error handler to send a custom response.
    """
