"""
title: Shared fixtures for MovFX tests
"""

from __future__ import annotations

import math
import struct
import wave

from pathlib import Path

import numpy as np
import pytest

from PIL import Image


@pytest.fixture()
def tmp_dir(tmp_path: Path) -> Path:
    """
    title: Provide a temporary directory for test artifacts
    parameters:
      tmp_path:
        type: Path
    returns:
      - type: Path
    """
    return tmp_path


@pytest.fixture()
def sample_images(tmp_dir: Path) -> tuple[Path, Path]:
    """
    title: Create two small test images
    summary: |
      Generates a 64x64 red image and a 64x64 blue image
      for transition testing.
    parameters:
      tmp_dir:
        type: Path
    returns:
      - type: tuple[Path, Path]
    """
    img_a = Image.fromarray(np.full((64, 64, 3), [255, 0, 0], dtype=np.uint8))
    img_b = Image.fromarray(np.full((64, 64, 3), [0, 0, 255], dtype=np.uint8))
    path_a = tmp_dir / "img_from.png"
    path_b = tmp_dir / "img_to.png"
    img_a.save(path_a)
    img_b.save(path_b)
    return path_a, path_b


@pytest.fixture()
def sample_sound(tmp_dir: Path) -> Path:
    """
    title: Create a short test audio file
    summary: |
      Generates a 2-second 440 Hz sine wave as a WAV file
      using the standard library (no pydub dependency).
    parameters:
      tmp_dir:
        type: Path
    returns:
      - type: Path
    """
    path = tmp_dir / "test_sound.wav"
    sample_rate = 44100
    duration_sec = 2.0
    frequency = 440.0
    n_samples = int(sample_rate * duration_sec)

    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            value = int(32767 * math.sin(2 * math.pi * frequency * t))
            wf.writeframes(struct.pack("<h", value))

    return path
