# emoji-lexicon

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

---

## Usage

```Python
from emoji_lexicon import get_catalog

catalog = get_catalog()

catalog.get("smile")		# lookup by short name or alias
catalog.get_by_char("😁")	# lookup by emoji character
catalog.search("happy")		# full-text search (alias / tag)
len(catalog)				# total emoji count
```
