#!/usr/bin/env python3
"""Generate isometric icons using OpenAI's image API."""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error


def load_base_prompt():
    """Read and strip contents of prompt.txt."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(script_dir, "prompt.txt")
    with open(prompt_path, "r") as f:
        return f.read().strip()


def load_image_as_data_uri(path):
    """Read image file, return as base64 data URI."""
    with open(path, "rb") as f:
        image_data = f.read()
    b64_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:image/png;base64,{b64_data}"


def generate_image(prompt, api_key, image_uri=None):
    """Build JSON payload, call appropriate API endpoint, return base64 image data."""
    if image_uri:
        url = "https://api.openai.com/v1/images/edits"
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "output_format": "png",
            "background": "transparent",
            "images": [{"image_url": image_uri}],
        }
    else:
        url = "https://api.openai.com/v1/images/generations"
        payload = {
            "model": "gpt-image-1",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "output_format": "png",
            "background": "transparent",
        }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["data"][0]["b64_json"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API error (HTTP {e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)


def save_image(b64_data, output_path):
    """Decode base64 and write PNG to file."""
    image_data = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(image_data)


def convert_to_svg(png_path, svg_path):
    """Convert PNG to SVG using vtracer."""
    import subprocess
    result = subprocess.run(
        [
            "vtracer",
            "--input", png_path,
            "--output", svg_path,
            "--mode", "polygon",          # Sharp edges instead of splines
            "--filter_speckle", "8",      # Remove small artifacts
            "--color_precision", "4",     # Fewer color buckets (5 colors)
            "--corner_threshold", "45",   # Preserve sharp corners
            "--segment_length", "4",      # Shorter segments for precision
            "--splice_threshold", "45",   # Join paths at sharp angles
        ],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Warning: vtracer failed: {result.stderr}", file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate isometric icons using OpenAI's image API"
    )
    parser.add_argument("prompt", help="Description of what to create")
    parser.add_argument("basename", help="Base name for output file (without extension)")
    parser.add_argument(
        "-f", "--force", action="store_true", help="Overwrite existing file"
    )
    parser.add_argument(
        "-i", "--image", help="Optional reference image to guide the style"
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(script_dir, "out")
    output_path = os.path.join(out_dir, f"{args.basename}.png")
    svg_path = os.path.join(out_dir, f"{args.basename}.svg")

    if not args.force:
        if os.path.exists(output_path):
            print(
                f"Error: {output_path} already exists. Use -f to overwrite.",
                file=sys.stderr,
            )
            sys.exit(1)
        if os.path.exists(svg_path):
            print(
                f"Error: {svg_path} already exists. Use -f to overwrite.",
                file=sys.stderr,
            )
            sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    base_prompt = load_base_prompt()
    combined_prompt = f"{base_prompt} {args.prompt}"

    image_uri = None
    if args.image:
        image_uri = load_image_as_data_uri(args.image)

    print(f"Generating image for: {args.prompt}")
    b64_data = generate_image(combined_prompt, api_key, image_uri)

    save_image(b64_data, output_path)
    print(f"Saved to: {output_path}")

    if convert_to_svg(output_path, svg_path):
        print(f"Saved to: {svg_path}")


if __name__ == "__main__":
    main()
