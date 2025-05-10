from pathlib import Path


is_snow = False

BASE_PATH = Path("data")
BASE_IMAGE_PATH = BASE_PATH / Path("images")
BASE_SFX_PATH = BASE_PATH / Path("sfx")
BASE_FONT_PATH = BASE_PATH / Path("fonts")


def get_image(image: str):
    theme_file_path = BASE_IMAGE_PATH / Path("classic") / image
    if is_snow:
        theme_file_path = BASE_IMAGE_PATH / Path("ice") / image
    theme_path = Path(__file__).parent / theme_file_path
    if theme_path.exists():
        return theme_path
    path = Path(__file__).parent / BASE_IMAGE_PATH / image
    if path.exists():
        return path
    raise FileNotFoundError(f"File '{image}' not found")


def get_sound(sound: str):
    file_path = BASE_SFX_PATH / sound
    path = Path(__file__).parent / file_path
    if not path.exists():
        raise FileNotFoundError(f"File '{sound}' not found")
    return path


def get_font(font: str):
    file_path = BASE_FONT_PATH / font
    path = Path(__file__).parent / file_path
    if not path.exists():
        raise FileNotFoundError(f"File '{file_path}' not found")
    return path


def change_theme() -> None:
    global is_snow
    is_snow = not is_snow


def set_snow(value: bool):
    global is_snow
    is_snow = value


def get_snow() -> bool:
    return is_snow


__all__ = [
    "change_theme",
    "get_snow",
    "get_image",
    "get_sound",
    "get_font",
]
