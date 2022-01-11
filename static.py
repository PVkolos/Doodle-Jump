import json
import os


def results_saver(results: dict):
    wd = os.getcwd()
    with open(f'{wd}/results.json', 'w') as f:
        f.write(json.dumps(results))


def results_loader() -> dict:
    wd = os.getcwd()
    if os.path.exists(f'{wd}/results.json'):
        with open(f'{wd}/results.json') as f:
            return json.load(f)
    return {}
