"""
title: Dissolve transition effect
summary: |
    Crossfade with per-pixel random noise grain for a
    film-dissolve look.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from movfx.effects.base import BaseEffect


class DissolveEffect(BaseEffect):
    """
    title: Grainy dissolve transition
    summary: |
        Similar to a fade, but adds per-pixel random noise so
        individual pixels transition at slightly different times,
        creating a grainy dissolve look.
    attributes:
        grain_strength: >
            Controls how much randomness is mixed into the
            blend factor. 0.0 = pure fade, 1.0 = maximum grain.
    """

    name: str = "dissolve"
    grain_strength: float

    def __init__(self, *, grain_strength: float = 0.3, **kwargs: Any) -> None:
        """
        title: Initialize dissolve effect
        parameters:
          grain_strength:
            type: float
            description: >-
              Strength of the grain noise (0.0 to 1.0). Default is 0.3.

          **kwargs:
            type: Any
        """
        super().__init__(**kwargs)
        self.grain_strength = max(0.0, min(1.0, grain_strength))

    def render_frame(
        self,
        img_from: np.ndarray,
        img_to: np.ndarray,
        progress: float,
    ) -> np.ndarray:
        """
        title: Render a dissolve frame
        parameters:
            img_from: Source image array
            img_to: Destination image array
            progress: Blend factor from 0.0 to 1.0
        returns: Grainy blended frame as uint8 array
        """
        h, w = img_from.shape[:2]
        noise = np.random.default_rng().uniform(
            -self.grain_strength, self.grain_strength, (h, w, 1)
        )
        per_pixel_progress = np.clip(progress + noise, 0.0, 1.0)
        blended = (1.0 - per_pixel_progress) * img_from + (
            per_pixel_progress * img_to
        )
        return blended.astype(np.uint8)
