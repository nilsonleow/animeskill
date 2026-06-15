#!/usr/bin/env python3
"""Store an xAI API key for Animeskill without committing it to a project."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import stat
from pathlib import Path


CONFIG_ENV = "ANIMESKILL_CONFIG"
DEFAULT_CONFIG = Path.home() / ".animeskill" / "config.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configure the xAI API key used by Animeskill.")
    parser.add_argument("--config", help="Config file path. Defaults to ANIMESKILL_CONFIG or ~/.animeskill/config.json.")
    parser.add_argument("--show-path", action="store_true", help="Print the config path and exit.")
    return parser.parse_args()


def config_path(args: argparse.Namespace) -> Path:
    raw_path = args.config or os.environ.get(CONFIG_ENV)
    return Path(raw_path).expanduser() if raw_path else DEFAULT_CONFIG


def main() -> int:
    args = parse_args()
    path = config_path(args)
    if args.show_path:
        print(path)
        return 0

    key = getpass.getpass("xAI API key: ").strip()
    if not key:
        raise SystemExit("No key entered; config was not changed.")
    if not key.startswith("xai-"):
        answer = input("The key does not start with 'xai-'. Save it anyway? [y/N] ").strip().lower()
        if answer not in {"y", "yes"}:
            raise SystemExit("Cancelled.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"xai_api_key": key}, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass

    print(f"Saved xAI API key config at {path}")
    print("Do not commit this file. Animeskill will read it when XAI_API_KEY is not set.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
