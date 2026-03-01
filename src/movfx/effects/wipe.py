"""
title: Wipe transition effect
summary: |
    A sharp-boundary wipe that sweeps across the frame,
    revealing the destination image.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np

from movfx.effects.base import BaseEffect


class WipeEffect(BaseEffect):
    """
    title: Directional wipe transition
    summary: |
        A hard-edge boundary sweeps across the frame in the
        given direction, progressively revealing the new image.
    attributes:
        direction: >
            Sweep direction. One of ``left``, ``right``,
            ``up``, or ``down``. Default is ``left``
            (i.e. the wipe moves left-to-right).
    """

    name: str = "wipe"
    direction: str

    def __init__(
        self,
        *,
        direction: Literal["left", "right", "up", "down"] = "left",
        **kwargs: Any,
    ) -> None:
        """
        title: Initialize wipe effect
        parameters:
            direction: >
                Direction of the wipe sweep.
                Default is ``left`` (left-to-right reveal).
        """
        super().__init__(**kwargs)
        self.direction = direction

    def render_frame(
        self,
        img_from: np.ndarray,
        img_to: np.ndarray,
        progress: float,
    ) -> np.ndarray:
        """
        title: Render a wipe frame
        parameters:
            img_from: Source image array
            img_to: Destination image array
            progress: Wipe progress from 0.0 to 1.0
        returns: Composited frame as uint8 array
        """
        h, w = img_from.shape[:2]
        frame = img_from.copy()

        if self.direction == "left":
            boundary = int(w * progress)
            frame[:, :boundary] = img_to[:, :boundary]
        elif self.direction == "right":
            boundary = int(w * (1.0 - progress))
            frame[:, boundary:] = img_to[:, boundary:]
        elif self.direction == "up":
            boundary = int(h * progress)
            frame[:boundary, :] = img_to[:boundary, :]
        elif self.direction == "down":
            boundary = int(h * (1.0 - progress))
            frame[boundary:, :] = img_to[boundary:, :]

        return frame
