"""
title: BaseEffect abstract base class for transition effects
summary: |
    Provides the abstract interface all effects must implement,
    plus a concrete ``build_clip`` helper that turns per-frame
    rendering into a moviepy VideoClip.
"""

from __future__ import annotations

import warnings

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import numpy as np

from moviepy import AudioFileClip, VideoClip
from PIL import Image


class BaseEffect(ABC):
    """
    title: Abstract base class for all transition effects
    attributes:
        name: Human-readable name used in the effect registry
        min_duration: >
            Optional minimum duration in seconds.
            If set, durations below this are clamped with a warning.
    """

    name: str = ""
    min_duration: float | None = None

    def __init__(self, **kwargs: Any) -> None:
        """
        title: Initialize the effect with optional keyword arguments
        parameters:
            kwargs: Effect-specific keyword arguments
        """

    @abstractmethod
    def render_frame(
        self,
        img_from: np.ndarray,
        img_to: np.ndarray,
        progress: float,
    ) -> np.ndarray:
        """
        title: Render a single transition frame
        parameters:
            img_from: Source image as a NumPy RGB array
            img_to: Destination image as a NumPy RGB array
            progress: >
                Transition progress from 0.0 (fully source)
                to 1.0 (fully destination)
        returns: Blended frame as a NumPy RGB uint8 array
        """

    def build_clip(
        self,
        img_from: np.ndarray,
        img_to: np.ndarray,
        duration: float,
        fps: int = 30,
    ) -> VideoClip:
        """
        title: Build a moviepy VideoClip from the effect
        parameters:
            img_from: Source image as a NumPy RGB array
            img_to: Destination image as a NumPy RGB array
            duration: Duration of the clip in seconds
            fps: Frames per second
        returns: A moviepy VideoClip with the transition
        """

        def make_frame(t: float) -> np.ndarray:
            progress = t / duration if duration > 0 else 1.0
            progress = max(0.0, min(1.0, progress))
            return self.render_frame(img_from, img_to, progress)

        clip = VideoClip(make_frame, duration=duration)
        clip = clip.with_fps(fps)
        return clip


def resolve_duration(
    duration: float,
    effect: BaseEffect,
    sound_path: str | Path | None = None,
) -> float:
    """
    title: Resolve the final duration for a transition
    summary: |
        Applies the duration resolution logic:
        1. Clamp to effect min_duration if needed (with warning).
        2. Extend to sound duration if sound is longer (with warning).
    parameters:
        duration: Requested duration in seconds
        effect: The effect instance (may define min_duration)
        sound_path: Optional path to an audio file
    returns: Resolved duration in seconds
    """
    final = duration

    if effect.min_duration is not None and final < effect.min_duration:
        warnings.warn(
            f"Requested duration {final}s is below the minimum "
            f"({effect.min_duration}s) for effect '{effect.name}'. "
            f"Using {effect.min_duration}s.",
            stacklevel=2,
        )
        final = effect.min_duration

    if sound_path is not None:
        audio = AudioFileClip(str(sound_path))
        sound_dur = audio.duration
        audio.close()
        if final < sound_dur:
            warnings.warn(
                f"Requested duration {final}s is shorter than the "
                f"sound duration ({sound_dur:.2f}s). "
                f"Using sound duration.",
                stacklevel=2,
            )
            final = sound_dur

    return final


def load_image(path: str | Path) -> np.ndarray:
    """
    title: Load an image file as a NumPy RGB array
    parameters:
        path: Path to the image file
    returns: NumPy array of shape (H, W, 3) with dtype uint8
    """
    img = Image.open(path).convert("RGB")
    return np.array(img)


def resize_to_match(
    img_a: np.ndarray,
    img_b: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    title: Resize two images to the same dimensions
    summary: |
        Uses the maximum width and height from both images.
        Images are resized with Lanczos resampling.
    parameters:
        img_a: First image array
        img_b: Second image array
    returns: Tuple of resized image arrays with matching dimensions
    """
    h = max(img_a.shape[0], img_b.shape[0])
    w = max(img_a.shape[1], img_b.shape[1])

    def _resize(arr: np.ndarray) -> np.ndarray:
        if arr.shape[0] == h and arr.shape[1] == w:
            return arr
        pil = Image.fromarray(arr)
        pil = pil.resize((w, h), Image.Resampling.LANCZOS)
        return np.array(pil)

    return _resize(img_a), _resize(img_b)
