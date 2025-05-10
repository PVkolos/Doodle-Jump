import json
from pathlib import Path


def load_results() -> dict:
    results_path = Path().cwd() / Path("results.json")
    if not results_path.exists():
        return {}
    with results_path.open() as f:
        return json.load(f)


def save_results(results: dict):
    results_path = Path().cwd() / Path("results.json")
    with results_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(results))


__all__ = [
    "load_results",
    "save_results",
]
