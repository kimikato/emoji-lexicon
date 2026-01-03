# tools/build-data.py
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

from pathlib import Path
from typing import Any

import msgpack

OUTPUT_DIR = Path("src/emoji_lexicon/data")
OUTPUT_FILE = OUTPUT_DIR / "emoji.msgpack"


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "meta": {
            "version": "0.1.0",
        },
        "emojis": [
            {
                "id": 0,
                "char": "😄",
                "short_name": "smile",
                "aliases": ["happy"],
                "group": "Smileys & Emotion",
                "subgroup": "face-smiling",
                "tags": ["happy", "smile"],
                "unicode_version": "6.0",
                "base_id": None,
            }
        ],
        "indexes": {
            "by_id": {0: 0},
            "by_short_name": {"smile": 0},
            "by_alias": {"happy": [0]},
            "by_char": {"😄": 0},
        },
    }

    with OUTPUT_FILE.open("wb") as f:
        msgpack.pack(payload, f, use_bin_type=True)

    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
