"""Theme registry - each theme lives in its own file (light.py, dark.py,
developer.py), fully self-contained: its own PALETTE (a few swatch colors,
used only for the small theme-preview mockups) and its own Build() function
returning every ready-made Qt stylesheet the app uses. Nothing is shared or
derived across theme files, so tuning one theme can never change another.

To add a new theme: drop a new module in this folder with a PALETTE dict
and a Build() function (copy an existing file as a starting point), then
register it below - nothing else in the app needs to change.
"""

from . import developer, dark, light

PALETTES = {
    "Developer": developer.PALETTE,
    "Dark": dark.PALETTE,
    "Light": light.PALETTE,
}

THEMES = {
    "Developer": developer.Build(),
    "Dark": dark.Build(),
    "Light": light.Build(),
}

MODES = tuple(PALETTES.keys())
