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


def check_collision(items, item) -> bool:
    for i in items:
        if item[0] + 70 >= i.x and item[1] + 15 >= i.y:
            return True
    return False
