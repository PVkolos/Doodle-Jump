is_snow = False


def get_image(image: str):
    if is_snow:
        return f'images/ice/{image}'
    else:
        return f'images/classic/{image}'


def change_theme():
    global is_snow
    is_snow = not is_snow


def set_snow(a: bool):
    global is_snow
    is_snow = a
