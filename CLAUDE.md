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

`scripts/Styles/` holds one module per theme — `light.py`, `dark.py`, `developer.py` — and each is **fully self-contained**: its own small `PALETTE` dict (a handful of swatch colors, used only by the mini theme-preview mockups) and its own `Build()` function returning every ready-made Qt stylesheet string the app uses (`MainWindowStyle`, `ButtonStyle`, `DialogStyle`, ...). Nothing is derived from a shared formula or shared constant across theme files — editing Light's button color, tab style, or anything else can only ever change Light. This is deliberate: an earlier version computed all three themes from one shared `PALETTE`-plus-`AccentAlpha` formula, and a contrast fix aimed at Light ended up changing Dark and Developer's look too. If you need a value to vary by theme, put the literal value in each theme's own `Build()` — don't reintroduce a shared knob.

`Styles/__init__.py` collects the three into `PALETTES = {"Light": ..., "Dark": ..., "Developer": ...}`, `THEMES = {"Light": ..., "Dark": ..., "Developer": ...}` (the built stylesheets), and `MODES`. **To add a new theme**: create `scripts/Styles/your_theme.py` with a `PALETTE` dict and a `Build()` function (copy an existing file as a starting point — every key in `Build()`'s return dict must be present), then register it in `Styles/__init__.py`'s import and both dicts — nothing else needs to change; `style.py`, the Settings **Developer** tab, and the first-run picker all read the registry, not a hardcoded list.

`style.py` is a thin loader: `Style.ApplyTheme(mode)` looks up `THEMES[mode]` and copies every key onto the `Style` class as an attribute (`Style.MainWindowStyle`, `Style.ButtonStyle`, `Style.WindowOpacity`, ...). `"Developer"` is the app's original hand-tuned look, kept byte-for-byte; `"Dark"` is a distinct slate-navy theme with its own (still translucent) accent buttons; `"Light"` uses its own solid "office blue" (`rgb(0,103,192)`) accent and dark-safe check/radio icons (`AssetsPath.CheckedOnLight` / `UncheckedOnLight`) rather than reusing Dark's neon `rgba(0,170,255,...)` at higher opacity — that read as harsh on a white background. `"System"` is not a theme itself — `ThemeManager.Resolve()` maps it to `"Light"`/`"Dark"` via the Windows registry (`AppsUseLightTheme`) before `Style.ApplyTheme` ever sees it.

`ConvertPyToExe.__init__` calls `Style.ApplyTheme(ThemeManager.Resolve(...))` before building any widgets, and — on first run only (no `theme.txt` yet) — shows a one-time theme-picker dialog (`ShowFirstRunThemeDialog`) before the registration dialog. The Settings dialog's **Developer** tab (radio buttons: Light/Dark/System/Developer, each paired with a live `BuildThemeSwatch` preview) live-previews via `PreviewTheme`, and both it and `SaveThemeSettings` route through `AnimateThemeChange`, which crossfades `self.MainWindow` with a `QGraphicsOpacityEffect` + `QPropertyAnimation` pair while the palette swaps underneath.

`BuildThemeSwatch(Mode)` renders a small VS-style mockup (title bar strip, card, sample text) built directly from `PALETTES[...]`, independent of the app's currently-applied `Style` — this is what lets every radio option preview correctly even while a different theme is actually applied. It's used both in the Settings **Developer** tab and in `ShowFirstRunThemeDialog`; reuse it for any future theme-picker UI rather than hand-rolling another preview.

`Style.WindowOpacity` (from each theme's `Build()`) is `1.0` for Light/Dark and `0.76` for Developer — Light and Dark render on a fully opaque, static background, while Developer keeps the original translucent glass window. Every place that sets the theme must also call `self.MainWindow.setWindowOpacity(Style.WindowOpacity)` after `Style.ApplyTheme`, or the window opacity will silently keep the previous mode's value.

Only the top-level window stylesheet is guaranteed to repaint live — most child widgets (buttons, inputs, cards) had their stylesheet strings baked in at construction time and only pick up a new palette on the next app launch. When adding a new stylesheet key, add it inside each theme's `Build()` — a key present in one theme but missing in another will simply not exist on `Style` after switching to that theme.

**Splash screen:** `ShowSplashScreen()` shows a frameless themed window (icon, title, `LOADER.gif`, status text) immediately after the theme is resolved; `UpdateSplash(text)` updates the status line at each startup stage. `CloseSplash()` enforces a minimum visible duration (`self.SplashMinDurationMs`, currently 1400ms) via a local `QEventLoop` + `QTimer.singleShot` before closing — startup (settings load + file indexing) is fast enough that without this the splash would flash and disappear before being seen.

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
