"""CSV and JSON Lines adapters."""
import csv, json
from pathlib import Path
from .models import Telemetry

def read_telemetry(path: str | Path) -> list[Telemetry]:
    path = Path(path)
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle: rows = list(csv.DictReader(handle))
    elif path.suffix.lower() in {".jsonl", ".ndjson"}:
        with path.open(encoding="utf-8") as handle: rows = [json.loads(line) for line in handle if line.strip()]
    elif path.suffix.lower() == ".json":
        with path.open(encoding="utf-8") as handle: value = json.load(handle)
        rows = value if isinstance(value, list) else [value]
    else: raise ValueError("supported input formats: .csv, .json, .jsonl, .ndjson")
    return [Telemetry.from_dict(row) for row in rows]
