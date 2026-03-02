"""
title: MovFX - Image transition effects with sound
"""

from importlib import metadata as importlib_metadata

from movfx.core import create_transition
from movfx.effects import EFFECTS


def get_version() -> str:
    """
    title: Return the program version
    returns:
      - type: str
    """
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.1.1"  # semantic-release


__author__ = """Ivan Ogasawara"""
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = get_version()

__all__ = [
    "EFFECTS",
    "__version__",
    "create_transition",
]
