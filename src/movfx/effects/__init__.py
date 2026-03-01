"""
title: Effects package for movfx
summary: |
    Exposes the effect registry and all built-in effect classes.
"""

from __future__ import annotations

from typing import Dict, Type

from movfx.effects.base import BaseEffect
from movfx.effects.dissolve import DissolveEffect
from movfx.effects.fade import FadeEffect
from movfx.effects.push import PushEffect
from movfx.effects.wipe import WipeEffect

EFFECTS: Dict[str, Type[BaseEffect]] = {
    "fade": FadeEffect,
    "dissolve": DissolveEffect,
    "wipe": WipeEffect,
    "push": PushEffect,
}

__all__ = [
    "EFFECTS",
    "BaseEffect",
    "DissolveEffect",
    "FadeEffect",
    "PushEffect",
    "WipeEffect",
]
