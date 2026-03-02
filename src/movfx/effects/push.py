"""
title: Push / Slide transition effect
summary: |
    The new image pushes the old image off-screen,
    sliding both simultaneously.
"""

from __future__ import annotations

from typing import Any, Literal

import numpy as np

from movfx.effects.base import BaseEffect


class PushEffect(BaseEffect):
    """
    title: Push (slide) transition
    summary: |
        The destination image slides in from one edge while
        the source image is pushed out through the opposite edge.
    attributes:
        direction: >
            Direction the new image enters from.
            ``left`` means the new image enters from the right
            and pushes the old image to the left.
    """

    name: str = "push"
    direction: str

    def __init__(
        self,
        *,
        direction: Literal["left", "right", "up", "down"] = "left",
        **kwargs: Any,
    ) -> None:
        """
        title: Initialize push effect
        parameters:
          direction:
            type: Literal[left, right, up, down]
            description: >-
              Direction the old image is pushed towards. Default is ``left``.
          **kwargs:
            type: Any
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
        title: Render a push frame
        parameters:
            img_from: Source image array
            img_to: Destination image array
            progress: Push progress from 0.0 to 1.0
        returns: Composited frame as uint8 array
        """
        h, w = img_from.shape[:2]
        frame = np.zeros_like(img_from)

        if self.direction == "left":
            offset = int(w * progress)
            # Old image slides left
            if w - offset > 0:
                frame[:, : w - offset] = img_from[:, offset:]
            # New image enters from the right
            if offset > 0:
                frame[:, w - offset :] = img_to[:, :offset]
        elif self.direction == "right":
            offset = int(w * progress)
            # Old image slides right
            if w - offset > 0:
                frame[:, offset:] = img_from[:, : w - offset]
            # New image enters from the left
            if offset > 0:
                frame[:, :offset] = img_to[:, w - offset :]
        elif self.direction == "up":
            offset = int(h * progress)
            # Old image slides up
            if h - offset > 0:
                frame[: h - offset, :] = img_from[offset:, :]
            # New image enters from the bottom
            if offset > 0:
                frame[h - offset :, :] = img_to[:offset, :]
        elif self.direction == "down":
            offset = int(h * progress)
            # Old image slides down
            if h - offset > 0:
                frame[offset:, :] = img_from[: h - offset, :]
            # New image enters from the top
            if offset > 0:
                frame[:offset, :] = img_to[h - offset :, :]

        return frame
