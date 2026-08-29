import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "Assets")


def AssetPath(FileName):
    return os.path.join(ASSETS_DIR, FileName).replace("\\", "/")


class AssetsPath:
    CopyIcon = AssetPath("COPY ICON.svg")
    RemoveIcon = AssetPath("REMOVE.svg")
    Checked = AssetPath("Check.png")
    CheckedOnLight = AssetPath("CHECK_DARK.png")
    Unchecked = AssetPath("RADIO_BUTTON_UNCHECKED.svg")
    UncheckedOnLight = AssetPath("RADIO_BUTTON_UNCHECKED_DARK.svg")
    RadioChecked = AssetPath("RADIO_BUTTON_CHECKED.svg")
    Loader = AssetPath("LOADER.gif")
    MenuIcon = AssetPath("Menu.svg")
    ApplicationIcon = os.path.join(BASE_DIR, "APP_BUILDER_ICON.ico").replace("\\", "/")
    AddStartMenuShortcutPath = "C:/Users/Lenovo/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/ROBIN Apps"
