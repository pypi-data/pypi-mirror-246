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

# where to source queries
query_dir = assets_dir.joinpath("queries")

# where to create pattern files
txtcat_dir = assets_dir.joinpath("txtcats")

# where to dump jsonl files
target_dir = Path(__file__).parent.parent.joinpath("tmp")


def load_from_query(fts_query: str, limit: int = 5000) -> set[str]:
    rows = tbl.search(q=fts_query, limit=limit)  # type: ignore
    texts = set()
    for row in rows:  # type: ignore
        texts.add(row["text"])
    return texts


def classify_lines(src_file: Path, limit: int = 5000) -> Iterator[dict[str, Any]]:
    expr = " OR ".join([f'"{q}"' for q in src_file.read_text().splitlines()])
    texts = load_from_query(fts_query=expr, limit=limit)
    return ({"label": src_file.stem.lower(), "text": text} for text in iter(texts))


def set_txtcat_jsonl_files(limit: int = 5000) -> Path:
    """There are two directories: (1) `/queries` (consists of .txt) and
    (2) `/txtcats` (consists of .jsonl). Each .txt file becomes a queried
    parameter to an sqlite search query to generate candidate segments
    from a source database. Each generated segment is labeled according
    to the filename of the .txt file.
    """
    for src in query_dir.glob("*.txt"):
        srsly.write_jsonl(
            path=txtcat_dir.joinpath(f"{src.stem}.jsonl"),
            lines=classify_lines(src, limit),
        )
    return txtcat_dir


def fts(q: str, limit: int = 50):
    for line in load_from_query(fts_query=q, limit=limit):
        task = {"text": line}
        print(json.dumps(task))
