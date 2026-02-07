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

## License

Copyright 2026 Andreas Gohr

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
