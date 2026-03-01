"""
title: MovFX core module
summary: |
    Public API for creating image transition videos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from moviepy import AudioFileClip

from movfx.effects import EFFECTS
from movfx.effects.base import load_image, resize_to_match, resolve_duration


def create_transition(
    image_from: str | Path,
    image_to: str | Path,
    effect: str,
    output: str | Path,
    *,
    sound: str | Path | None = None,
    duration: float = 1.0,
    fps: int = 30,
    **effect_kwargs: Any,
) -> Path:
    """
    title: Create a transition video between two images
    summary: |
        Loads both images, applies the named effect to produce
        a transition video, optionally overlays audio, and writes
        the result to disk.
    parameters:
        image_from: Path to the source image
        image_to: Path to the destination image
        effect: >
            Name of the effect (e.g. ``fade``, ``dissolve``,
            ``wipe``, ``push``)
        output: Path for the output video file
        sound: Optional path to an audio file
        duration: >
            Duration in seconds (default 1.0).
            May be overridden by sound length or effect minimum.
        fps: Frames per second (default 30)
        effect_kwargs: Additional keyword arguments for the effect
    returns: Path to the generated video file
    raises:
        ValueError: If the effect name is not recognized
    """
    output = Path(output)

    if effect not in EFFECTS:
        available = ", ".join(sorted(EFFECTS.keys()))
        raise ValueError(
            f"Unknown effect '{effect}'. Available effects: {available}"
        )

    effect_cls = EFFECTS[effect]
    effect_instance = effect_cls(**effect_kwargs)

    img_a = load_image(image_from)
    img_b = load_image(image_to)
    img_a, img_b = resize_to_match(img_a, img_b)

    final_duration = resolve_duration(duration, effect_instance, sound)

    clip = effect_instance.build_clip(img_a, img_b, final_duration, fps)

    if sound is not None:
        audio = AudioFileClip(str(sound))
        if audio.duration > final_duration:
            audio = audio.subclipped(0, final_duration)
        clip = clip.with_audio(audio)

    clip.write_videofile(
        str(output),
        fps=fps,
        codec="libx264",
        audio_codec="aac" if sound else None,
        logger=None,
    )

    return output
