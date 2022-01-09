import os


is_snow = False


def get_image(image: str):
    if is_snow:
        path = f'images/ice/{image}'
    else:
        path = f'images/classic/{image}'
    if os.path.exists(path):
        return path
    elif os.path.exists(f'images/{image}'):
        return f'images/{image}'


def change_theme():
    global is_snow
    is_snow = not is_snow


def set_snow(a: bool):
    global is_snow
    is_snow = a
