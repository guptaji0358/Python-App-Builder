"""Theme registry - each theme lives in its own file (light.py, dark.py,
developer.py) as a PALETTE dict. To add a new theme: drop a new module in
this folder with a PALETTE dict (see any existing file for the required
keys), then register it below - nothing else in the app needs to change,
Style.ApplyTheme and every settings/first-run picker pick it up automatically.
"""

from . import developer, dark, light

PALETTES = {
    "Developer": developer.PALETTE,
    "Dark": dark.PALETTE,
    "Light": light.PALETTE,
}

MODES = tuple(PALETTES.keys())
