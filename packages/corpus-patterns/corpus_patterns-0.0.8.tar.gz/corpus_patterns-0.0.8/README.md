# corpus-patterns

![Github CI](https://github.com/justmars/corpus-patterns/actions/workflows/main.yml/badge.svg)

A preparatory utils library.

## Create a custom tokenizer

```py
from corpus_patterns import set_tokenizer

nlp = spacy.blank("en")
nlp.tokenizer = set_tokenizer(nlp)
```

The tokenizer:

1. Removes dashes from infixes
2. Adds prefix/suffix rules for parenthesis/brackets
3. Adds special exceptions to treat dotted text as a single token

## Add .jsonl files to directory

Each file will contain lines of spacy matcher patterns.

```py
from corpus_patterns import create_rules
from pathlib import Path

create_rules(folder=Path("location-here"))  # check directory
```

## Extract contents from txt files and jsonl files

This should be folder structure of ASSETS_DIR

```yml
- patterns:
  - political: # main subject category
    - bill_of_rights: # sub-topic
      - patterns.json # contains matcher files
      - q.txt # contains lines which can be used to query the database
```

Based on this can run `extract_txts()` and `extract_jsonl()` to get patterns having the spacy matcher format:

```py
{"label": "concept", "pattern" <applicable pattern>, "id": <political/bill_of_rights>}
```

A convenience `create_patterns()` is the combination of the `extract_txts()` and  `extract_jsonl()`

## Search database for text fragments

Assuming DATA_PATH is declared in the .env:

```py
from corpus_patterns import get_segments, load_from_query

load_from_query('<fts-5-query>', limit=5) # returns first 5 results
```

If ASSETS_DIR contains q.txt files:

```py
get_segments(path=Path("location-here")) # returns iterator of string matches based on queries found in the location's q.txt files```

## Custom loader for main database queries (for prodigy)

See purpose in [prodigy docs](https://prodi.gy/docs/api-loaders):

```py
from corpus_patterns import fts
fts('"police power"', limit=10) # note the FTS search expression
```

## Utils

1. `annotate_fragments()` - given an nlp object and some `*.txt` files, create a single annotation `*.jsonl` file
2. `extract_lines_from_txt_files()` - accepts an iterator of `*.txt` files and yields each line (after sorting the same and ensuring uniqueness of content).
3. `split_data()` - given a list of text strings, split the same into two groups and return a dictionary containing these groups based on the ratio provided (defaults to 0.80)
