# emoji-lexicon

![Tests](https://github.com/kimikato/emoji-lexicon/actions/workflows/tests.yml/badge.svg?branch=main)
[![coverage](https://img.shields.io/codecov/c/github/kimikato/emoji-lexicon/main?label=coverage&logo=codecov)](https://codecov.io/gh/kimikato/emoji-lexicon)
[![PyPI version](https://img.shields.io/pypi/v/emoji-lexicon.svg)](https://pypi.org/project/emoji-lexicon/)
[![Python](https://img.shields.io/pypi/pyversions/emoji-lexicon.svg)](https://pypi.org/project/emoji-lexicon/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

emoji-lexicon is a build-time generated emoji lexicon for Python,
designed for fast and reliable emoji lookup.

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

```Python
from emoji_lexicon import get_catalog

catalog = get_catalog()

catalog.get("smile")        # lookup by short name or alias
catalog.get_by_char("😁")   # lookup by emoji character
catalog.search("happy")     # full-text search (alias / tag)
len(catalog)                # total emoji count
catalog.groups()            # available emoji groups
catalog.subgroups()         # available emoji subgroups
```
