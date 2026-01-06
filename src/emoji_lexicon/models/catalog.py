# src/emoji_lexicon/models/catalog.py
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

from importlib import resources
from pathlib import Path
from typing import Any, Iterable, Mapping, cast

import msgpack

from .emoji import Emoji


class EmojiCatalog:
    """
    Runtime emoji catalog.

    EmojiCatalog provides read-only access to a build-time generated
    emoji lexicon (emoji.msgpack)
    """

    def __init__(
        self,
        emojis: Iterable[Emoji],
        *,
        by_id: Mapping[int, Emoji],
        by_short_name: Mapping[str, Emoji],
        by_alias: Mapping[str, Iterable[Emoji]],
        by_char: Mapping[str, Emoji],
    ) -> None:
        self._emojis: tuple[Emoji, ...] = tuple(emojis)
        self._by_id: dict[int, Emoji] = dict(by_id)
        self._by_short_name: dict[str, Emoji] = dict(by_short_name)
        self._by_alias: dict[str, tuple[Emoji, ...]] = {
            k: tuple(v) for k, v in by_alias.items()
        }
        self._by_char: dict[str, Emoji] = dict(by_char)

        # ----------------------------------------
        # Inverted index (token -> emojis)
        # ----------------------------------------
        token_map: dict[str, list[Emoji]] = {}

        for e in self._emojis:
            # short_name tokens
            token_map.setdefault(e.short_name, []).append(e)

            # aliases
            for alias in e.aliases:
                token_map.setdefault(alias, []).append(e)

            # tags
            for tag in e.tags:
                token_map.setdefault(tag, []).append(e)

        self._by_token: dict[str, tuple[Emoji, ...]] = {
            k: tuple(sorted(v, key=lambda e: e.id))
            for k, v in token_map.items()
        }

    # ----------------------------------------
    # Factory
    # ----------------------------------------
    @classmethod
    def load(cls, path: str | Path | None = None) -> EmojiCatalog:
        """
        Load emoji catalog from a msgpack file.

        Parameters:
        ------------
        path:
            Optional path to emoji.msgpack.
            If omitted, the bundled default data is used.
        """
        raw_data: Any = {}

        if path is None:
            with (
                resources.files("emoji_lexicon.data")
                .joinpath("emoji.msgpack")
                .open("rb") as f
            ):
                raw_data = msgpack.unpack(f, raw=False)
        else:
            with Path(path).open("rb") as f:
                raw_data = msgpack.unpack(f, raw=False)

        if not isinstance(raw_data, dict):
            raise TypeError(
                "Invalid emoji.msgpack format: expected dict at top level"
            )

        data = cast(dict[str, Any], raw_data)

        emojis: list[Emoji] = []
        by_id: dict[int, Emoji] = {}
        by_short_name: dict[str, Emoji] = {}
        by_alias: dict[str, list[Emoji]] = {}
        by_char: dict[str, Emoji] = {}

        for item in cast(list[dict[str, Any]], data["emojis"]):
            emoji = Emoji(
                id=cast(int, item["id"]),
                char=cast(str, item["char"]),
                short_name=cast(str, item["short_name"]),
                aliases=tuple(cast(list[str], item["aliases"])),
                group=cast(str, item["group"]),
                subgroup=cast(str, item["subgroup"]),
                tags=tuple(cast(list[str], item["tags"])),
                unicode_version=cast(str, item["unicode_version"]),
                base_id=cast(int | None, item.get("base_id")),
            )

            emojis.append(emoji)
            by_id[emoji.id] = emoji
            by_short_name[emoji.short_name] = emoji
            by_char[emoji.char] = emoji

            for alias in emoji.aliases:
                by_alias.setdefault(alias, []).append(emoji)

        return cls(
            emojis,
            by_id=by_id,
            by_short_name=by_short_name,
            by_alias=by_alias,
            by_char=by_char,
        )

    # ----------------------------------------
    # Normalize query
    # ----------------------------------------
    @staticmethod
    def normalize_query(query: str) -> str:
        return query.strip().strip(":").lower()

    # ----------------------------------------
    # Basic accessors
    # ----------------------------------------
    def __len__(self) -> int:
        return len(self._emojis)

    def __iter__(self) -> Iterable[Emoji]:
        return iter(self._emojis)

    def __str__(self) -> str:
        return ""

    def __repr__(self) -> str:
        return (
            f"<EmojiCatalog "
            f"size={len(self._emojis)!r}, "
            f"groups={len(self.groups())!r}>"
        )

    # ----------------------------------------
    # Get
    # ----------------------------------------
    def get(self, name: str) -> Emoji | None:
        """
        Lookup emoji by short name or alias.

        Parameters:
        ------------
        name:
            short name or alias
        """
        q = self.normalize_query(name)

        if q in self._by_short_name:
            return self._by_short_name[q]

        hits = self._by_token.get(q)
        return hits[0] if hits else None

    def get_by_id(self, emoji_id: int) -> Emoji | None:
        return self._by_id.get(emoji_id)

    def get_by_char(self, char: str) -> Emoji | None:
        return self._by_char.get(char)

    def get_all(self) -> tuple[Emoji, ...]:
        """
        Return all emojis in the catalog.
        The returned tuple is immutable and ordered by emoji ID.
        """
        return self._emojis

    # ----------------------------------------
    # Search
    # ----------------------------------------
    def search(self, query: str) -> tuple[Emoji, ...]:
        q = self.normalize_query(query)
        return self._by_token.get(q, ())

    def find(self, query: str) -> tuple[Emoji, ...]:
        """
        Find emojis matching the given query.
        """
        return self.search(query)

    # ----------------------------------------
    # group / subgroup
    # ----------------------------------------
    def groups(self) -> tuple[str, ...]:
        return tuple(sorted({e.group for e in self._emojis}))

    def subgroups(self) -> tuple[str, ...]:
        return tuple(sorted({e.subgroup for e in self._emojis}))
