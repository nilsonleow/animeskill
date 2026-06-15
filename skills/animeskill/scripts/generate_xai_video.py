#!/usr/bin/env python3
"""Generate short chroma-key image-to-video clips with xAI Grok Imagine."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


PRICES = {
    "480x480": {"resolution": "480p", "per_second": 0.05},
    "720x720": {"resolution": "720p", "per_second": 0.07},
}
IMAGE_INPUT_COST = 0.002
CHROMA_VALUES = {"#00FF00", "#FF00FF"}
CONFIG_ENV = "ANIMESKILL_CONFIG"
DEFAULT_CONFIG = Path.home() / ".animeskill" / "config.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an xAI Grok Imagine image-to-video clip.")
    parser.add_argument("--image", required=True, help="Local PNG/JPG character image.")
    parser.add_argument("--action", required=True, help="Animation action, e.g. 'walk cycle, side view'.")
    parser.add_argument("--duration", required=True, type=int, choices=[1, 2, 3])
    parser.add_argument("--size", required=True, choices=sorted(PRICES))
    parser.add_argument("--chroma", required=True, choices=sorted(CHROMA_VALUES))
    parser.add_argument("--output", required=True, help="Output MP4 path.")
    parser.add_argument("--model", default="grok-imagine-video")
    parser.add_argument("--dry-run", action="store_true", help="Print request details without calling xAI.")
    parser.add_argument("--yes", action="store_true", help="Skip interactive cost confirmation.")
    parser.add_argument("--poll-interval", type=float, default=5.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    return parser.parse_args()


def estimate_cost(size: str, duration: int) -> float:
    return PRICES[size]["per_second"] * duration + IMAGE_INPUT_COST


def image_to_data_uri(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"Image not found: {path}")
    mime, _ = mimetypes.guess_type(str(path))
    if mime not in {"image/png", "image/jpeg"}:
        raise SystemExit("Input image must be PNG or JPEG.")
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_prompt(action: str, duration: int, chroma: str) -> str:
    return (
        f"Animate the provided character image into a {duration}-second {action} animation "
        "for a 2D game sprite sheet. Preserve the exact character identity, outfit, colors, "
        "proportions, and silhouette from the source image. Keep the full body centered and visible. "
        f"Use a perfectly flat solid {chroma} chroma-key background only. The background must be "
        "absolutely clean: no contact shadows, ambient shadows, cast shadows, reflections, glow, "
        "outlines, ground plane, horizon line, texture, particles, lighting falloff, noise, gradients, "
        "or color variation. No camera movement, no zoom, no scene cuts, no text, no extra characters, no props. "
        "Clean readable motion, loop-friendly timing."
    )


def request_json(url: str, method: str, api_key: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Authorization": f"Bearer {api_key}"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"xAI API error {exc.code}: {details}") from exc


def download(url: str, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response:
        output.write_bytes(response.read())


def config_path() -> Path:
    configured = os.environ.get(CONFIG_ENV)
    return Path(configured).expanduser() if configured else DEFAULT_CONFIG


def load_api_key() -> tuple[str | None, str]:
    env_key = os.environ.get("XAI_API_KEY")
    if env_key:
        return env_key, "XAI_API_KEY"

    path = config_path()
    if not path.is_file():
        return None, str(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid Animeskill config JSON at {path}: {exc}") from exc

    key = data.get("xai_api_key")
    if isinstance(key, str) and key.strip():
        return key.strip(), str(path)
    return None, str(path)


def main() -> int:
    args = parse_args()
    image_path = Path(args.image)
    output_path = Path(args.output)
    prompt = build_prompt(args.action, args.duration, args.chroma)
    cost = estimate_cost(args.size, args.duration)

    payload = {
        "model": args.model,
        "prompt": prompt,
        "image": {"url": image_to_data_uri(image_path)},
        "duration": args.duration,
        "aspect_ratio": "1:1",
        "resolution": PRICES[args.size]["resolution"],
    }

    summary = {
        "model": args.model,
        "duration": args.duration,
        "size": args.size,
        "resolution": payload["resolution"],
        "estimated_cost_usd": round(cost, 4),
        "output": str(output_path),
        "prompt": prompt,
    }
    print(json.dumps(summary, indent=2))

    if args.dry_run:
        return 0

    if not args.yes:
        answer = input(f"Estimated xAI cost is about ${cost:.3f}. Continue? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            print("Cancelled.")
            return 1

    api_key, api_key_source = load_api_key()
    if not api_key:
        raise SystemExit(
            "No xAI API key found. Set XAI_API_KEY or run "
            "`python <skill>/scripts/configure_xai_key.py` to save one in "
            f"{api_key_source}."
        )
    print(f"Using xAI API key from {api_key_source}.")

    start = request_json("https://api.x.ai/v1/videos/generations", "POST", api_key, payload)
    request_id = start.get("request_id")
    if not request_id:
        raise SystemExit(f"Missing request_id in response: {start}")

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        result = request_json(f"https://api.x.ai/v1/videos/{request_id}", "GET", api_key)
        status = result.get("status")
        if status == "done":
            video_url = result["video"]["url"]
            download(video_url, output_path)
            print(f"Saved {output_path}")
            return 0
        if status in {"failed", "expired"}:
            raise SystemExit(json.dumps(result, indent=2))
        print(f"Status: {status or 'unknown'}")
        time.sleep(args.poll_interval)

    raise SystemExit(f"Timed out waiting for request {request_id}")


if __name__ == "__main__":
    raise SystemExit(main())
