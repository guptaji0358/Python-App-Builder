# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Python App Builder — a PySide6 desktop app that wraps PyInstaller in a GUI, letting users convert `.py` scripts into Windows `.exe` files without hand-writing PyInstaller commands.

- **Entry point:** [PYTHON_APP_BUILDER.py](PYTHON_APP_BUILDER.py) — just instantiates `ConvertPyToExe()` from `scripts/convert_py_to_exe.py`.
- **Platform:** Windows only (uses `pywin32` for Start Menu shortcuts, builds `.exe` output).
- **UI framework:** PySide6 (Qt for Python).

## Architecture

All source lives under `scripts/`:

| File | Role |
|---|---|
| `convert_py_to_exe.py` | Main window and app logic — `ConvertPyToExe` class. This is the largest file and owns most UI wiring. |
| `threads.py` | Background `QThread` workers: `FileIndexerThread`, `IconIndexerThread`, `BuildThread` (runs PyInstaller and streams progress). |
| `style.py` | Qt stylesheets (`Style` class) and visual effects — no logic. Builds every constant from `Styles/`'s `PALETTES`. |
| `Styles/` | One file per theme (see below) plus a registry — this is what "switching themes" actually means. |
| `messages.py` | Shared `QMessageBox` dialog helpers (`Messages` class). |
| `shortcuts.py` | `ShortcutManager` — editable keyboard shortcuts, persisted to `shortcuts.txt`. |
| `theme.py` | `ThemeManager` — persists the Light/Dark/System/Developer theme choice to `theme.txt` and resolves `System` via the Windows registry (`AppsUseLightTheme`). |
| `assets_path.py` | Resolves paths into `Assets/` (handles dev vs. frozen/PyInstaller-bundled paths via `AssetPath` / `AssetsPath`). |

### Theming

`scripts/Styles/` holds one module per theme — `light.py`, `dark.py`, `developer.py` — each exporting a single `PALETTE` dict (colors plus the per-theme knobs `WindowOpacity`, `IsLight`, `AccentAlpha`/`AccentHoverAlpha`/`AccentPressedAlpha`). `Styles/__init__.py` collects them into `PALETTES = {"Light": ..., "Dark": ..., "Developer": ...}` and `MODES`. **To add a new theme**: create `scripts/Styles/your_theme.py` with a `PALETTE` dict (copy an existing file for the required keys), then add one line to `Styles/__init__.py`'s import and `PALETTES` dict — nothing else needs to change; `style.py`, the Settings **Developer** tab, and the first-run picker all read the registry, not a hardcoded list.

`style.py` builds every stylesheet constant (`Style.MainWindowStyle`, `Style.InputStyle`, etc.) from the palette for the current mode via `Style.ApplyTheme(mode)`, which rebinds the class attributes at runtime. `"Developer"` is the app's original hand-tuned palette, kept byte-for-byte; `"Dark"` is a distinct, newer slate-navy palette. `"System"` is not a palette itself — `ThemeManager.Resolve()` maps it to `"Light"`/`"Dark"` via the Windows registry (`AppsUseLightTheme`) before `Style.ApplyTheme` ever sees it.

`ConvertPyToExe.__init__` calls `Style.ApplyTheme(ThemeManager.Resolve(...))` before building any widgets, and — on first run only (no `theme.txt` yet) — shows a one-time theme-picker dialog (`ShowFirstRunThemeDialog`) before the registration dialog. The Settings dialog's **Developer** tab (radio buttons: Light/Dark/System/Developer, each paired with a live `BuildThemeSwatch` preview) live-previews via `PreviewTheme`, and both it and `SaveThemeSettings` route through `AnimateThemeChange`, which crossfades `self.MainWindow` with a `QGraphicsOpacityEffect` + `QPropertyAnimation` pair while the palette swaps underneath.

`BuildThemeSwatch(Mode)` renders a small VS-style mockup (title bar strip, card, sample text) built directly from `PALETTES[...]`, independent of the app's currently-applied `Style` — this is what lets every radio option preview correctly even while a different theme is actually applied. It's used both in the Settings **Developer** tab and in `ShowFirstRunThemeDialog`; reuse it for any future theme-picker UI rather than hand-rolling another preview.

`Style.ApplyTheme` also sets `Style.WindowOpacity` (`1.0` for Light/Dark, `0.76` for Developer) — Light and Dark render on a fully opaque, static background, while Developer keeps the original translucent glass window. Every place that sets the theme must also call `self.MainWindow.setWindowOpacity(Style.WindowOpacity)` after `Style.ApplyTheme`, or the window opacity will silently keep the previous mode's value.

**Contrast on Light:** most icons/text/accent overlays in this app were originally tuned to sit on a near-black background — `white` text, near-white check/radio glyphs, and very low-alpha accent fills that read fine as pale highlights on dark, but wash out or vanish on Light. Each theme's `PALETTE["IsLight"]` and `PALETTE["AccentAlpha"/"AccentHoverAlpha"/"AccentPressedAlpha"]` exist specifically to compensate — `Style.ApplyTheme` reads them to pick a `CheckedIcon`/`UncheckedIcon` pair and to set the accent-button opacity. `ButtonStyle`/`AddAssetButtonStyle`/tab-bar hover/selected all render near-opaque on Light instead of translucent, and the check/radio indicators swap to `AssetsPath.CheckedOnLight` / `AssetsPath.UncheckedOnLight` (dark-stroke variants of `Check.png` / `RADIO_BUTTON_UNCHECKED.svg`, generated once and committed to `Assets/`) whenever `IsLight` is `True`. A new theme file just needs to pick sane values for these four keys — no code changes required. `QTabWidget`/`QTabBar` in `DialogStyle` is themed too (it previously had no stylesheet at all and silently fell back to unreadable default OS colors on the Settings dialog). `ProgressBarStyle` deliberately stays a fixed dark chip (not palette-driven) so its white percentage text is always legible under the rainbow gradient regardless of theme.

Only the top-level window stylesheet is guaranteed to repaint live — most child widgets (buttons, inputs, cards) had their stylesheet strings baked in at construction time and only pick up a new palette on the next app launch. When adding a new themed constant to `style.py`, add it inside `Style.ApplyTheme`, not as a bare class attribute, or it won't respond to theme changes at all.

**Persistence gotcha:** `theme.py`'s `THEME_FILE` must stay a bare relative path (`"theme.txt"`), matching `verification.txt`/`shortcuts.txt`. It was previously derived from `__file__`, which resolves into PyInstaller's temp extraction folder in a frozen `.exe` — that folder is wiped after every run, so the saved theme (and the first-run picker) would silently reset on every launch of the built exe. Don't reintroduce a `__file__`-based path for any new per-machine config file.

`Assets/` holds UI images/icons/gifs referenced via `assets_path.py` — this indirection matters because paths differ between running from source and running from a frozen `.exe` (PyInstaller `sys._MEIPASS`).

**Bundling gotcha:** `AssetsPath.ApplicationIcon` points at `APP_BUILDER_ICON.ico` in the project root, not inside `Assets/`. `--icon` at build time only embeds it as the `.exe` file's own Explorer/taskbar-pin icon — it does **not** put the file inside the frozen app's data, so `QIcon(AssetsPath.ApplicationIcon)` silently returned a null icon at runtime (window/dialog/taskbar icon while running) until a second `--add-data "APP_BUILDER_ICON.ico;."` was added to bundle it too (also present in `PythonAppBuilder.spec`'s `datas`). Any asset referenced outside `Assets/` needs the same treatment — bundled explicitly, not assumed to come along with `--icon` or any other single-purpose flag.

## Local/runtime config (not tracked in git)

- `verification.txt` — Company/Author/Copyright/Trademark, used as default PyInstaller version metadata.
- `shortcuts.txt` — user's custom keyboard shortcut bindings.
- `theme.txt` — selected theme mode (`Light` / `Dark` / `System`).
- `version_info.txt` — temporary PyInstaller version resource, written next to the target script and deleted after each build.

Don't assume these files exist; the app prompts for `verification.txt` contents on first run.

## Build/dev commands

Run from source:
```bash
python PYTHON_APP_BUILDER.py
```

Build the distributable exe (see `PythonAppBuilder.spec` for the maintained spec):
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "PythonAppBuilder" --icon "APP_BUILDER_ICON.ico" --add-data "Assets;Assets" --add-data "APP_BUILDER_ICON.ico;." --distpath "out" --workpath "build" PYTHON_APP_BUILDER.py
```

`build/` and `out/` are PyInstaller artifacts — never commit them.

## Conventions

- No test suite exists yet — verify UI changes by actually running the app (`python PYTHON_APP_BUILDER.py`) and exercising the affected flow, since this is a GUI-heavy project where type checks don't catch UI regressions.
- Keep the dev-vs-frozen path distinction in mind: any new asset access should go through `assets_path.py`, not raw relative paths, or it will break in the built `.exe`.
- This project previously had bugs around build freezes, `ModuleNotFoundError` in the frozen exe, and missing bundled assets (see git history) — when touching `threads.py`'s `BuildThread` or the PyInstaller invocation/spec, double-check the frozen build still launches, not just that it compiles.

---

**Author:** Robin Gupta
**Assisted by:** Claude Code
