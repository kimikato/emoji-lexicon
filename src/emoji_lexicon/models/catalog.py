# src/emoji_lexicon/models/catalog.py

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Mapping

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
        self._emojis = tuple(emojis)
        self._by_id = dict(by_id)
        self._by_short_name = dict(by_short_name)
        self._by_alias = {k: tuple(v) for k, v in by_alias.items()}
        self._by_char = dict(by_char)

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
        raise NotImplementedError

    # ----------------------------------------
    # Basic accessors
    # ----------------------------------------
    def __len__(self) -> int:
        return len(self._emojis)

    def __iter__(self) -> Iterable[Emoji]:
        return iter(self._emojis)

    def get_by_id(self, emoji_id: int) -> Emoji | None:
        return self._by_id.get(emoji_id)

    def get(self, name: str) -> Emoji | None:
        """
        Lookup emoji by short name or alias.

        Parameters:
        ------------
        name:
            short name or alias
        """
        name = name.strip(":")
        if name in self._by_short_name:
            return self._by_short_name[name]
        aliases = self._by_alias.get(name)
        if aliases:
            return aliases[0]
        return None

    def get_by_char(self, char: str) -> Emoji | None:
        return self._by_char.get(char)

    # ----------------------------------------
    # Search
    # ----------------------------------------
    def search(self, query: str) -> Iterable[Emoji]:
        """
        Search emojis by short name, alias, or tag.

        Parameters:
        ------------
        query:
            short name, alias, or tag
        """
        raise NotImplementedError
