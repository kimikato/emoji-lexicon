# tools/build-data.py
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

from pathlib import Path
from typing import Any

import msgpack

from tools.unicode.emoji_test_parser import parse_emoji_test

OUTPUT_DIR = Path("src/emoji_lexicon/data")
OUTPUT_FILE = OUTPUT_DIR / "emoji.msgpack"


def normalize_name(name: str) -> str:
    """
    Return short name normalized to snake case

    Parameters:
    ------------

    name:
        short name

    Examples:
        "grinning face" -> "grinning_face"
    """
    return name.lower().replace(" ", "_")


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    emojis: list[dict[str, Any]] = []
    by_id: dict[str, int] = {}
    by_short_name: dict[str, int] = {}
    by_alias: dict[str, int] = {}
    by_char: dict[str, int] = {}

    emoji_id: int = 0

    emoji_test_path = Path("tools/data/emoji-test.txt")

    for entry in parse_emoji_test(emoji_test_path):
        # Process only data with a qualification that matches "fully-qualified"
        if entry.qualification != "fully-qualified":
            continue

        # Normalized name
        short_name = normalize_name(entry.name)

        emoji: dict[str, Any] = {
            "id": emoji_id,
            "char": entry.char,
            "short_name": short_name,
            "aliases": [],
            "group": entry.group,
            "subgroup": entry.subgroup,
            "tags": [],
            "unicode_version": entry.unicode_version,
            "base_id": None,
        }

        emojis.append(emoji)
        by_id[str(emoji_id)] = emoji_id
        by_short_name[short_name] = emoji_id
        by_char[entry.char] = emoji_id

        emoji_id += 1

    payload: dict[str, Any] = {
        "meta": {"version": "0.1.0"},
        "emojis": emojis,
        "indexes": {
            "by_id": by_id,
            "by_short_name": by_short_name,
            "by_alias": by_alias,
            "by_char": by_char,
        },
    }

    with OUTPUT_FILE.open("wb") as f:
        msgpack.pack(payload, f, use_bin_type=True)

    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
