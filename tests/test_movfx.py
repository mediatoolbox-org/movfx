"""Basic tests for MovFX package."""

import movfx


def test_version() -> None:
    """Ensure the version string is returned correctly."""
    version = movfx.__version__()
    assert isinstance(version, str)
    assert version == "0.1.0"


def test_import() -> None:
    """Ensure the package can be imported without errors."""
    assert movfx is not None
