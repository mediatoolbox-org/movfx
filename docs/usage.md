# Usage Guide

## Basic Usage

The main entry point is the `create_transition()` function. It takes two images,
an effect name, and an output path to generate a transition video.

```python
from movfx import create_transition

create_transition("photo_a.png", "photo_b.png", "fade", "output.mp4")
```

## Effects

### Fade

A linear crossfade between two images.

```python
create_transition("a.png", "b.png", "fade", "fade.mp4", duration=2.0)
```

### Dissolve

Similar to a fade but with per-pixel random noise for a film-like dissolve look.
The `grain_strength` parameter (0.0–1.0) controls the noise amount.

```python
create_transition("a.png", "b.png", "dissolve", "dissolve.mp4", grain_strength=0.5)
```

### Wipe

A hard-edge boundary sweeps across the frame, revealing the new image. The
`direction` parameter controls the sweep direction.

```python
# Left-to-right wipe (default)
create_transition("a.png", "b.png", "wipe", "wipe.mp4", direction="left")

# Top-to-bottom wipe
create_transition("a.png", "b.png", "wipe", "wipe_down.mp4", direction="down")
```

### Push / Slide

The new image slides in from one edge, pushing the old image off-screen.

```python
# New image pushes old image to the left
create_transition("a.png", "b.png", "push", "push.mp4", direction="left")

# New image pushes old image upward
create_transition("a.png", "b.png", "push", "push_up.mp4", direction="up")
```

## Adding Sound

Pass a `sound` argument to overlay audio on the transition. When sound is
provided, the audio duration determines the video length (if longer than the
requested duration).

```python
create_transition(
    "a.png",
    "b.png",
    "fade",
    "with_sound.mp4",
    sound="background.mp3",
)
```

## Duration Control

The `duration` parameter sets the transition length in seconds (default: 1.0).

```python
create_transition("a.png", "b.png", "fade", "slow.mp4", duration=3.0)
```

**Duration resolution rules:**

1. If the effect defines a minimum duration and the requested value is lower,
   the minimum is used and a warning is emitted.
2. If a sound file is provided and its length exceeds the requested duration,
   the sound duration is used and a warning is emitted.

## Frame Rate

Set the `fps` parameter to control the output frame rate (default: 30).

```python
create_transition("a.png", "b.png", "fade", "smooth.mp4", fps=60)
```

## Listing Available Effects

```python
from movfx import EFFECTS

print(list(EFFECTS.keys()))
# ['dissolve', 'fade', 'push', 'wipe']
```
