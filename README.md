# emoji-lexicon

emoji-lexicon is a build-time generated emoji lexicon for Python.

## Features

- Fast emoji lookup by short name, alias, or tag
- Unicode / CLDR based canonical data
- Build-time normalization, runtime zero-cost lookup
- Designed for CLI, IME, and dictionary tools
- Optional gemoji-compatible export

## Requirements

- Python 3.12+

## Installation

```bash
pip install emoji-lexicon
```

---

## Basic Usage

```Python
from emoji_lexicon import EmojiCatalog

db = EmojiCatalog.load()
print(db.get("smile"))
```
