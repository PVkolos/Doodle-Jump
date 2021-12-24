import json
import os


def results_saver(results: dict):
    with open('results.json', 'w') as f:
        f.write(json.dumps(results))


def results_loader() -> dict:
    if os.path.exists('results.json'):
        with open('results.json') as f:
            return json.load(f)
    return {}
