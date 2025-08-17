# Material Palette Generator
![Palette Preview](https://github.com/blacksteel3/material-palette-generator/blob/cca45b190f0716f29117561e5771d20fe07f66bf/preview.png)

A Python port of the [Official Material Palette Generator](https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors).  
This project reverse-engineers and refactors Google’s original algorithm to generate palette (extracted by [edelstone/material-palette-generator](https://github.com/edelstone/material-palette-generator)) into clean, reusable Python code.

## Features
- Generate full Material Design palettes from a single base hex color
- Produces primary, complementary, analogous and triadic variations
- Shows palette preview in image (`pillow` library required)
- CLI support (`mpg` command)
- MIT Licensed
- No dependencies (pure Python)

## Installation
Clone the repository:
```bash
git clone https://github.com/blacksteel3/material-palette-generator.git
cd material-palette-generator
```

Or install via `pip`:
```bash
pip install material-palettes-generator
```

## Usage
```py
import material_palette_generator as mpg

# generate palette from generic method
palettes = mpg.get_palettes("#E91E63")  # optional `types` parameter to specify color types

print(palettes['Primary'])
print(palettes['Complementary'])
print(palettes['Analogous-1'])
print(palettes['Analogous-2'])
print(palettes['Triadic-1'])
print(palettes['Triadic-2'])

# or use specific method for specific type
primary_palette = mpg.get_primary_palette("#E91E63")
print(primary_palette)

# preview any palette (`pillow` library must be installed)
mpg.preview_palettes(primary_palette)
```

## Command Line Interface (CLI)
After installing, you can use the mpg command directly from your terminal:
```bash
# Generate the primary palette
mpg "#3f51b5"

# Output as JSON
mpg "#3f51b5" --json

# Output as CSS
mpg "#3f51b5" --css

# Generate specific types
mpg "#3f51b5" --primary
mpg "#3f51b5" --complementary
mpg "#3f51b5" --analogous
mpg "#3f51b5" --triadic

# Combine multiple flags
mpg "#3f51b5" -p -t --json

# Or get all palettes
mpg "#3f51b5" --all

# Preview palette
mpg "#3f51b5" --show

# See all commands
mpg --help
```

## Credits
- **[Google](www.google.com)** — for creating the Material Design color algorithm
- **[Michael Edelstone](https://github.com/edelstone)** — for extracting the obfuscated JavaScript runtime code
- **[Black Steel](https://github.com/blacksteel3)** — for reverse-engineering, renaming, and porting the algorithm to Python
