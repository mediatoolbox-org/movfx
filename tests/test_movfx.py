"""
title: Basic tests for MovFX package
"""

import douki

import movfx


@douki
def test_version() -> None:
    """
    title: Ensure the version string is returned correctly
    """
    version = movfx.__version__
    assert isinstance(version, str)
    assert version == "0.1.0"


@douki
def test_import() -> None:
    """
    title: Ensure the package can be imported without errors
    """
    assert movfx is not None
