import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import srsly  # type: ignore
from environs import Env
from sqlite_utils import Database

# where to source lines
env = Env()
env.read_env()
db_file = Path(env.str("DATA_PATH"))
db_file.exists()
src_db = Database(db_file)
tbl = src_db["opinion_segments"]

assets_dir = Path(env.str("ASSET_PATH"))


def extract_txts(path: Path) -> Iterator[dict[str, str]]:
    for txt_file in path.glob("**/q.txt"):
        for line in txt_file.read_text().splitlines():
            if line:
                yield {
                    "label": "concept",
                    "pattern": line,
                    "id": f"{txt_file.parent.parent.stem}/{txt_file.parent.stem}",
                }


def extract_jsonl(path: Path) -> Iterator[dict[str, str | list[dict[str, Any]]]]:
    for json_file in path.glob("**/patterns.json"):
        matchers = srsly.read_json(json_file)
        if matchers and isinstance(matchers, list):
            for matcher_pattern in matchers:
                yield {
                    "label": "concept",
                    "pattern": matcher_pattern,
                    "id": f"{json_file.parent.parent.stem}/{json_file.parent.stem}",
                }


def create_patterns(path: str):
    return list(extract_jsonl(Path(path))) + list(extract_txts(Path(path)))


def load_from_query(fts_query: str, limit: int = 5000) -> set[str]:
    rows = tbl.search(q=fts_query, limit=limit)  # type: ignore
    texts = set()
    for row in rows:  # type: ignore
        texts.add(row["text"])
    return texts


def get_segments(path: Path, limit: int = 5000) -> Iterator[str]:
    """Each q.txt file in the path is collected and each line in that
    file is used as part of an fts query string to a database declared
    in the env variable `DATA_PATH`. The results of the fts query are returned
    as an iterator of strings."""
    files = path.glob("**/q.txt")
    queries = iter({line for f in files for line in f.read_text().splitlines() if line})
    fts_expr = " OR ".join([f'"{q}"' for q in queries])
    results = iter(load_from_query(fts_expr, limit=limit))
    return results


def fts(q: str, limit: int = 50):
    for line in load_from_query(fts_query=q, limit=limit):
        task = {"text": line}
        print(json.dumps(task))
