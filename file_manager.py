import os
from pathlib import Path


is_snow = False


def get_image(image: str):
    if is_snow:
        path = f'images/ice/{image}'
    else:
        path = f'images/classic/{image}'
    path = os.path.join(Path(__file__).parent, path)
    if os.path.exists(path):
        return path
    path = os.path.join(Path(__file__).parent, f'images/{image}')
    if os.path.exists(path):
        return path


def get_sound(sound: str):
    path = f'sfx/{sound}'
    path = os.path.join(Path(__file__).parent, path)
    if os.path.exists(path):
        return path


def get_path(file: str) -> str:
    return os.path.join(Path(__file__).parent, file)


def change_theme():
    global is_snow
    is_snow = not is_snow


def set_snow(a: bool):
    global is_snow
    is_snow = a


def get_snow() -> bool:
    global is_snow
    return is_snow
