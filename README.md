# isoico

A CLI tool for generating isometric icons using OpenAI's image generation API. Designed for creating icons to be used with [FossFLOW](https://github.com/stan-smith/FossFLOW).

## What it does

isoico generates isometric icons with a fixed color palette and style from a given prompt. The icon is then converted into an SVG file using [vtracer](https://github.com/visioncortex/vtracer)

## Requirements

- Python 3 (no external dependencies)
- `OPENAI_API_KEY` environment variable, `gpt-image-1` model access, and sufficient quota
- Optional: `vtracer` installed for SVG conversion (not required for PNG output)

## Usage

```bash
python3 isoico.py <prompt> [basename] [-f]
```

**Arguments:**
- `prompt` - Subject description (e.g., "a laptop computer")
- `basename` - (optional) Output file base path without extension. Defaults to a random 8-character name.
- `-f, --force` - Overwrite existing files

**Examples:**

```bash
# Generate with random filename
python3 isoico.py "a coffee mug"

# Generate with specific name
python3 isoico.py "a laptop computer" laptop

# Generate in a subdirectory
python3 isoico.py "a gear" icons/gear

# Overwrite existing file
python3 isoico.py "a book" book -f
```
