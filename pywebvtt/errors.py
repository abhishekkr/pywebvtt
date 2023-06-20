__all__ = ['BadDataError', 'BadTimestamp', 'MissingFileError']


class BadDataError(Exception):
    """[ERROR] Provided data is not proper VTT structured."""


class BadTimestamp(Exception):
    """[ERROR] Provided timestamp is of bad format."""


class MissingFileError(Exception):
    """[ERROR] Provided file path for VTT data is unavailable."""
