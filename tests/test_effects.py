"""
title: Tests for the movfx effects system
"""

from __future__ import annotations

import warnings

from pathlib import Path

import numpy as np
import pytest

from movfx import EFFECTS, create_transition
from movfx.effects.base import BaseEffect, resolve_duration
from movfx.effects.dissolve import DissolveEffect
from movfx.effects.fade import FadeEffect
from movfx.effects.push import PushEffect
from movfx.effects.wipe import WipeEffect


# ── Registry ────────────────────────────────────────────────


class TestRegistry:
    """
    title: Tests for the effect registry
    """

    def test_all_effects_registered(self) -> None:
        """
        title: Ensure all four built-in effects are in the registry
        """
        assert set(EFFECTS.keys()) == {
            "fade",
            "dissolve",
            "wipe",
            "push",
        }

    def test_registry_values_are_base_subclasses(self) -> None:
        """
        title: Ensure registry values are BaseEffect subclasses
        """
        for cls in EFFECTS.values():
            assert issubclass(cls, BaseEffect)


# ── Render Frame ────────────────────────────────────────────


class TestRenderFrame:
    """
    title: Tests for individual effect render_frame methods
    """

    @pytest.fixture()
    def images(self) -> tuple[np.ndarray, np.ndarray]:
        """
        title: Small in-memory test arrays
        returns:
          - type: tuple[np.ndarray, np.ndarray]
        """
        a = np.full((8, 8, 3), 0, dtype=np.uint8)
        b = np.full((8, 8, 3), 255, dtype=np.uint8)
        return a, b

    def test_fade_start(self, images: tuple[np.ndarray, np.ndarray]) -> None:
        """
        title: Fade at progress=0 returns the source image
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = FadeEffect().render_frame(a, b, 0.0)
        np.testing.assert_array_equal(result, a)

    def test_fade_end(self, images: tuple[np.ndarray, np.ndarray]) -> None:
        """
        title: Fade at progress=1 returns the destination image
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = FadeEffect().render_frame(a, b, 1.0)
        np.testing.assert_array_equal(result, b)

    def test_fade_mid(self, images: tuple[np.ndarray, np.ndarray]) -> None:
        """
        title: Fade at progress=0.5 returns the midpoint blend
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = FadeEffect().render_frame(a, b, 0.5)
        assert np.allclose(result, 127, atol=1)

    def test_dissolve_returns_valid_range(
        self, images: tuple[np.ndarray, np.ndarray]
    ) -> None:
        """
        title: Dissolve output stays in valid uint8 range
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = DissolveEffect().render_frame(a, b, 0.5)
        assert result.dtype == np.uint8
        assert result.min() >= 0
        assert result.max() <= 255

    def test_wipe_left_start(
        self, images: tuple[np.ndarray, np.ndarray]
    ) -> None:
        """
        title: Wipe left at progress=0 shows the source
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = WipeEffect(direction="left").render_frame(a, b, 0.0)
        np.testing.assert_array_equal(result, a)

    def test_wipe_left_end(
        self, images: tuple[np.ndarray, np.ndarray]
    ) -> None:
        """
        title: Wipe left at progress=1 shows the destination
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = WipeEffect(direction="left").render_frame(a, b, 1.0)
        np.testing.assert_array_equal(result, b)

    def test_push_start(self, images: tuple[np.ndarray, np.ndarray]) -> None:
        """
        title: Push at progress=0 shows the source
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = PushEffect(direction="left").render_frame(a, b, 0.0)
        np.testing.assert_array_equal(result, a)

    def test_push_end(self, images: tuple[np.ndarray, np.ndarray]) -> None:
        """
        title: Push at progress=1 shows the destination
        parameters:
          images:
            type: tuple[np.ndarray, np.ndarray]
        """
        a, b = images
        result = PushEffect(direction="left").render_frame(a, b, 1.0)
        np.testing.assert_array_equal(result, b)


# ── Duration Resolution ─────────────────────────────────────


class TestDurationResolution:
    """
    title: Tests for resolve_duration logic
    """

    def test_default_duration(self) -> None:
        """
        title: Returns the requested duration when no constraints
        """
        effect = FadeEffect()
        assert resolve_duration(1.0, effect) == 1.0

    def test_min_duration_clamp(self) -> None:
        """
        title: Clamp to effect min_duration with a warning
        """
        effect = FadeEffect()
        effect.min_duration = 2.0
        with pytest.warns(UserWarning, match="below the minimum"):
            result = resolve_duration(0.5, effect)
        assert result == 2.0

    def test_sound_duration_override(self, sample_sound: Path) -> None:
        """
        title: Sound duration overrides when longer than requested
        parameters:
          sample_sound:
            type: Path
        """
        effect = FadeEffect()
        with pytest.warns(UserWarning, match="shorter than the sound"):
            result = resolve_duration(0.5, effect, sound_path=sample_sound)
        assert result >= 1.9  # ~2 seconds

    def test_no_warning_when_duration_exceeds_sound(
        self, sample_sound: Path
    ) -> None:
        """
        title: No warning when requested duration >= sound duration
        parameters:
          sample_sound:
            type: Path
        """
        effect = FadeEffect()
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            result = resolve_duration(5.0, effect, sound_path=sample_sound)
        assert result == 5.0


# ── Integration: create_transition ───────────────────────────


class TestCreateTransition:
    """
    title: Integration tests for the create_transition API
    """

    @pytest.mark.parametrize("effect_name", ["fade", "dissolve"])
    def test_basic_transition(
        self,
        sample_images: tuple[Path, Path],
        tmp_dir: Path,
        effect_name: str,
    ) -> None:
        """
        title: Basic transition produces a valid video file
        parameters:
          sample_images:
            type: tuple[Path, Path]
          tmp_dir:
            type: Path
          effect_name:
            type: str
        """
        img_from, img_to = sample_images
        out = tmp_dir / f"out_{effect_name}.mp4"
        result = create_transition(
            img_from, img_to, effect_name, out, duration=0.5, fps=10
        )
        assert result.exists()
        assert result.stat().st_size > 0

    @pytest.mark.parametrize(
        "effect_name,kwargs",
        [
            ("wipe", {"direction": "left"}),
            ("wipe", {"direction": "right"}),
            ("push", {"direction": "left"}),
            ("push", {"direction": "up"}),
        ],
    )
    def test_directional_transitions(
        self,
        sample_images: tuple[Path, Path],
        tmp_dir: Path,
        effect_name: str,
        kwargs: dict,
    ) -> None:
        """
        title: Directional effects produce valid video files
        parameters:
          sample_images:
            type: tuple[Path, Path]
          tmp_dir:
            type: Path
          effect_name:
            type: str
          kwargs:
            type: dict
        """
        img_from, img_to = sample_images
        direction = kwargs["direction"]
        out = tmp_dir / f"out_{effect_name}_{direction}.mp4"
        result = create_transition(
            img_from,
            img_to,
            effect_name,
            out,
            duration=0.5,
            fps=10,
            **kwargs,
        )
        assert result.exists()
        assert result.stat().st_size > 0

    def test_transition_with_sound(
        self,
        sample_images: tuple[Path, Path],
        sample_sound: Path,
        tmp_dir: Path,
    ) -> None:
        """
        title: Transition with sound produces a video
        parameters:
          sample_images:
            type: tuple[Path, Path]
          sample_sound:
            type: Path
          tmp_dir:
            type: Path
        """
        img_from, img_to = sample_images
        out = tmp_dir / "out_sound.mp4"
        result = create_transition(
            img_from,
            img_to,
            "fade",
            out,
            sound=sample_sound,
            fps=10,
        )
        assert result.exists()
        assert result.stat().st_size > 0

    def test_unknown_effect_raises(
        self,
        sample_images: tuple[Path, Path],
        tmp_dir: Path,
    ) -> None:
        """
        title: Unknown effect name raises ValueError
        parameters:
          sample_images:
            type: tuple[Path, Path]
          tmp_dir:
            type: Path
        """
        img_from, img_to = sample_images
        with pytest.raises(ValueError, match="Unknown effect"):
            create_transition(
                img_from,
                img_to,
                "nonexistent",
                tmp_dir / "out.mp4",
            )
