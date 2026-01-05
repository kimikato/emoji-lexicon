# tests/test_api.py
# type: ignore

from emoji_lexicon import get_catalog


def test_get_catalog_basic():
    catalog = get_catalog()

    assert len(catalog) > 0


def test_basic_lookup():
    catalog = get_catalog()

    emoji = catalog.get("smile")
    assert emoji is not None
    assert isinstance(emoji.char, str)

    same = catalog.get_by_char(emoji.char)
    assert same == emoji


def test_search_smile():
    catalog = get_catalog()
    results = catalog.search("smile")

    assert isinstance(results, tuple)
    assert len(results) > 0
