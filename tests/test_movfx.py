"""
title: Basic tests for MovFX package
"""

import movfx


def test_version() -> None:
    """
    title: Ensure the version string is returned correctly
    """
    version = movfx.__version__
    assert isinstance(version, str)
    assert version == "0.1.0"


def test_import() -> None:
    """
    title: Ensure the package can be imported without errors
    """
    assert movfx is not None


def test_create_transition_importable() -> None:
    """
    title: Ensure create_transition is accessible from the package
    """
    assert hasattr(movfx, "create_transition")
    assert callable(movfx.create_transition)


def test_effects_registry_importable() -> None:
    """
    title: Ensure EFFECTS registry is accessible from the package
    """
    assert hasattr(movfx, "EFFECTS")
    assert len(movfx.EFFECTS) > 0
