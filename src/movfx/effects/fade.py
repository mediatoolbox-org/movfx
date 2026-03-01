"""
title: Fade transition effect
summary: |
    Linear alpha crossfade between two images.
"""

from __future__ import annotations

import numpy as np

from movfx.effects.base import BaseEffect


class FadeEffect(BaseEffect):
    """
    title: Linear crossfade transition
    summary: |
        Blends source and destination with a linear alpha ramp.
        Frame at progress *t* is ``(1-t)*A + t*B``.
    """

    name: str = "fade"

    def render_frame(
        self,
        img_from: np.ndarray,
        img_to: np.ndarray,
        progress: float,
    ) -> np.ndarray:
        """
        title: Render a fade frame
        parameters:
            img_from: Source image array
            img_to: Destination image array
            progress: Blend factor from 0.0 to 1.0
        returns: Blended frame as uint8 array
        """
        blended = (1.0 - progress) * img_from + progress * img_to
        return blended.astype(np.uint8)
