"""
title: Integration tests using real test data
summary: |
    Tests each effect with real images from tests/data/images
    and sound from tests/data/sounds. Output videos are saved
    to tests/.tmp with descriptive filenames.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from movfx import EFFECTS, create_transition

DATA_DIR = Path(__file__).parent / "data"
IMAGES_DIR = DATA_DIR / "images"
SOUNDS_DIR = DATA_DIR / "sounds"
OUTPUT_DIR = Path(__file__).parent / ".tmp"

IMG_FROM = IMAGES_DIR / "dog1.jpg"
IMG_TO = IMAGES_DIR / "dog2.jpg"
SOUND = SOUNDS_DIR / "lalala.mp3"


@pytest.fixture(autouse=True)
def _ensure_output_dir() -> None:
    """
    title: Ensure the output directory exists before each test
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _output_name(
    img_from: Path,
    img_to: Path,
    effect: str,
    sound: Path | None = None,
    **kwargs: str,
) -> str:
    """
    title: Build a descriptive output filename
    summary: |
        Composes the name from image stems, effect name,
        sound stem (if any), and extra kwargs like direction.
    """
    parts = [img_from.stem, img_to.stem, effect]
    if sound is not None:
        parts.append(sound.stem)
    for key, val in sorted(kwargs.items()):
        parts.append(f"{key}-{val}")
    return "__".join(parts) + ".mp4"


# ── Basic effects (no sound) ────────────────────────────────


class TestEffectsNoSound:
    """
    title: Integration tests for each effect without sound
    """

    @pytest.mark.parametrize("effect_name", sorted(EFFECTS.keys()))
    def test_effect_no_sound(self, effect_name: str) -> None:
        """
        title: Each effect produces a valid video without sound
        """
        out = OUTPUT_DIR / _output_name(IMG_FROM, IMG_TO, effect_name)
        result = create_transition(
            IMG_FROM,
            IMG_TO,
            effect_name,
            out,
            duration=1.0,
            fps=15,
        )
        assert result.exists()
        assert result.stat().st_size > 0


# ── Effects with sound ──────────────────────────────────────


class TestEffectsWithSound:
    """
    title: Integration tests for each effect with sound
    """

    @pytest.mark.parametrize("effect_name", sorted(EFFECTS.keys()))
    def test_effect_with_sound(self, effect_name: str) -> None:
        """
        title: Each effect produces a valid video with sound
        """
        out = OUTPUT_DIR / _output_name(
            IMG_FROM, IMG_TO, effect_name, sound=SOUND
        )
        result = create_transition(
            IMG_FROM,
            IMG_TO,
            effect_name,
            out,
            sound=SOUND,
            fps=15,
        )
        assert result.exists()
        assert result.stat().st_size > 0


# ── Directional effects ─────────────────────────────────────


class TestDirectionalEffects:
    """
    title: Integration tests for directional effect variants
    """

    @pytest.mark.parametrize(
        "effect_name,direction",
        [
            ("wipe", "left"),
            ("wipe", "right"),
            ("wipe", "up"),
            ("wipe", "down"),
            ("push", "left"),
            ("push", "right"),
            ("push", "up"),
            ("push", "down"),
        ],
    )
    def test_directional_no_sound(
        self, effect_name: str, direction: str
    ) -> None:
        """
        title: Directional effects produce valid videos
        """
        out = OUTPUT_DIR / _output_name(
            IMG_FROM,
            IMG_TO,
            effect_name,
            direction=direction,
        )
        result = create_transition(
            IMG_FROM,
            IMG_TO,
            effect_name,
            out,
            duration=1.0,
            fps=15,
            direction=direction,
        )
        assert result.exists()
        assert result.stat().st_size > 0

    @pytest.mark.parametrize(
        "effect_name,direction",
        [
            ("wipe", "left"),
            ("push", "left"),
        ],
    )
    def test_directional_with_sound(
        self, effect_name: str, direction: str
    ) -> None:
        """
        title: Directional effects with sound produce valid videos
        """
        out = OUTPUT_DIR / _output_name(
            IMG_FROM,
            IMG_TO,
            effect_name,
            sound=SOUND,
            direction=direction,
        )
        result = create_transition(
            IMG_FROM,
            IMG_TO,
            effect_name,
            out,
            sound=SOUND,
            fps=15,
            direction=direction,
        )
        assert result.exists()
        assert result.stat().st_size > 0


# ── Dissolve grain strength ─────────────────────────────────


class TestDissolveGrain:
    """
    title: Integration test for dissolve grain_strength parameter
    """

    @pytest.mark.parametrize("grain", [0.1, 0.5, 0.9])
    def test_dissolve_grain_strength(self, grain: float) -> None:
        """
        title: Dissolve with various grain strengths produces valid video
        """
        out = OUTPUT_DIR / _output_name(
            IMG_FROM,
            IMG_TO,
            f"dissolve_grain{grain}",
        )
        result = create_transition(
            IMG_FROM,
            IMG_TO,
            "dissolve",
            out,
            duration=1.0,
            fps=15,
            grain_strength=grain,
        )
        assert result.exists()
        assert result.stat().st_size > 0
