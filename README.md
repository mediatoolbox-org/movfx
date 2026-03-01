# MovFX

MovFX provides transition effects between images with optional sound.

## Features

- Transition effects between two images for a specified duration
- Optional sound overlay during transitions
- Video output generation

## Installation

```bash
pip install movfx
```

## Development

```bash
# Clone the repository
git clone https://github.com/mediatoolbox-org/movfx.git
cd movfx

# Create conda environment
conda env create -f conda/dev.yaml
conda activate movfx

# Install dependencies
poetry install

# Run tests
makim tests.unittest
```

## License

BSD-3-Clause
