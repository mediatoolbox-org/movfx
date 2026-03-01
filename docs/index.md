# MovFX

MovFX provides transition effects between images with optional sound.

## Features

- **4 built-in effects**: Fade, Dissolve, Wipe, Push/Slide
- Directional support for Wipe and Push (left, right, up, down)
- Optional sound overlay — audio duration drives the video length
- Smart duration resolution with minimum-duration enforcement
- Simple one-call API: `create_transition()`

## Quick Start

```python
from movfx import create_transition

# Simple fade transition (1 second, no audio)
create_transition("photo_a.png", "photo_b.png", "fade", "output.mp4")

# Wipe with direction and sound
create_transition(
    "photo_a.png",
    "photo_b.png",
    "wipe",
    "output.mp4",
    direction="left",
    sound="music.mp3",
)
```

## Available Effects

| Effect     | Description                                       | Extra Arguments                  |
| ---------- | ------------------------------------------------- | -------------------------------- |
| `fade`     | Linear alpha crossfade                            | —                                |
| `dissolve` | Crossfade with per-pixel grain noise              | `grain_strength` (0.0–1.0)       |
| `wipe`     | Hard-edge boundary sweeps across                  | `direction` (left/right/up/down) |
| `push`     | New image slides in, pushing old image off-screen | `direction` (left/right/up/down) |

## Duration Rules

1. Default duration is **1 second**
2. If the effect defines a minimum duration and the requested duration is
   shorter, the minimum is used (with a warning)
3. If a sound file is provided and its duration exceeds the requested duration,
   the sound duration is used (with a warning)
