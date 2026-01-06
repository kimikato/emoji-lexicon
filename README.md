# emoji-lexicon

![Tests](https://github.com/kimikato/emoji-lexicon/actions/workflows/tests.yml/badge.svg?branch=main)
[![coverage](https://img.shields.io/codecov/c/github/kimikato/emoji-lexicon/main?label=coverage&logo=codecov)](https://codecov.io/gh/kimikato/emoji-lexicon)
[![PyPI version](https://img.shields.io/pypi/v/emoji-lexicon.svg)](https://pypi.org/project/emoji-lexicon/)
[![Python](https://img.shields.io/pypi/pyversions/emoji-lexicon.svg)](https://pypi.org/project/emoji-lexicon/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

🚀 **emoji-lexicon** is a fast, build-time generated emoji lexicon for Python,
powered by Unicode emoji-test and CLDR annotations.

## Features

-   Fast emoji lookup by short name, alias, or tag
-   Designed for CLI, IME, and dictionary tools
-   Unicode / CLDR based canonical data
-   Build-time normalization, runtime zero-cost lookup
-   Optional gemoji-compatible export

## Requirements

-   Python 3.12+

## Installation

```bash
pip install emoji-lexicon
```

## Usage

```python
from emoji_lexicon import get_catalog

catalog = get_catalog()

# lookup by short name or alias
catalog.get("smile")
# -> Emoji | None

# Slack / gemoji style
catalog.get(":smile:")

# lookup by emoji character
catalog.get_by_char("😁")
# -> Emoji | None

# get all emojis
catalog.get_all()

# total emoji count
len(catalog)

# iterator
for emoji in catalog:
	print(emoji.char, emoji.short_name)
```

### `.search()` , `.find()`

```python
# partial match (short_name / alias / tag)
catalog.search("happy")
# -> tuple[Emoji, ...]

# alias of .search()
catalog.find("happy")
# -> tuple[Emoji, ...]
```

`.search()` and `.find()` perform partial matching and return multiple emojis.
`.find()` is a user-facing alias of `.search()`.

### `.groups()`, `.subgroups()`

```python
from emoji_lexicon import get_catalog
catalog = get_catalog()

# available emoji groups
catalog.groups()

# available emoji subgroups
catalog.subgroups()

```

Application examples:

-   Categories UI
-   IME candidate narrowing down
-   emoji picker

## Design philosophy

-   runtime zero-cost
-   immutable catalog
-   Pythonic & typed

## License

MIT License
© 2026 Kiminori Kato
