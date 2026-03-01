"""MovFX: Image transition effects with sound."""

from importlib import metadata as importlib_metadata


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.1.0"  # semantic-release


__author__ = """Ivan Ogasawara"""
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = get_version()
