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
| `customization.py` | `CustomizationManager` — persists default build preferences (build type, console mode, shortcut/command checkboxes, open-folder-after-build, Start Menu path) to `customization.txt`, same flat `key=value` format as `shortcuts.py`. |
| `user_data.py` | `UserDataPath()`/`DbPath()`/`EnsureUserDataDirs()` — the single source of truth for where per-machine state lives (`user-data/`, `user-data/db/`). Every other persistence module builds its file path from this. |
| `build_history.py` | `BuildHistory` — SQLite log of every successful build (`user-data/db/builds.db`), recorded from `BuildCompletedWindow`. |
| `file_index_db.py` | `PyFileIndexDatabase` / `IconFileIndexDatabase` — separate SQLite caches (`user-data/db/py_index.db`, `icon_index.db`) of the `.py` / `.ico` search indexes, so autocomplete has data instantly on startup instead of waiting on a fresh full-disk scan. |
| `assets_path.py` | Resolves paths into `Assets/` (handles dev vs. frozen/PyInstaller-bundled paths via `AssetPath` / `AssetsPath`). |

### Theming

`scripts/Styles/` holds one module per theme — `light.py`, `dark.py`, `developer.py` — and each is **fully self-contained**: its own small `PALETTE` dict (a handful of swatch colors, used only by the mini theme-preview mockups) and its own `Build()` function returning every ready-made Qt stylesheet string the app uses (`MainWindowStyle`, `ButtonStyle`, `DialogStyle`, ...). Nothing is derived from a shared formula or shared constant across theme files — editing Light's button color, tab style, or anything else can only ever change Light. This is deliberate: an earlier version computed all three themes from one shared `PALETTE`-plus-`AccentAlpha` formula, and a contrast fix aimed at Light ended up changing Dark and Developer's look too. If you need a value to vary by theme, put the literal value in each theme's own `Build()` — don't reintroduce a shared knob.

`Styles/__init__.py` collects the three into `PALETTES = {"Light": ..., "Dark": ..., "Developer": ...}`, `THEMES = {"Light": ..., "Dark": ..., "Developer": ...}` (the built stylesheets), and `MODES`. **To add a new theme**: create `scripts/Styles/your_theme.py` with a `PALETTE` dict and a `Build()` function (copy an existing file as a starting point — every key in `Build()`'s return dict must be present), then register it in `Styles/__init__.py`'s import and both dicts — nothing else needs to change; `style.py`, the Settings **Theme** tab, and the first-run picker all read the registry, not a hardcoded list.

`style.py` is a thin loader: `Style.ApplyTheme(mode)` looks up `THEMES[mode]` and copies every key onto the `Style` class as an attribute (`Style.MainWindowStyle`, `Style.ButtonStyle`, `Style.WindowOpacity`, ...). `"Developer"` is the app's original hand-tuned look, kept byte-for-byte; `"Dark"` is a distinct slate-navy theme with its own (still translucent) accent buttons; `"Light"` uses its own muted "office blue" (`rgb(43,92,138)`) accent and dark-safe check/radio icons (`AssetsPath.CheckedOnLight` / `UncheckedOnLight`) rather than reusing Dark's neon `rgba(0,170,255,...)` at higher opacity or a more saturated blue — both read as harsh/uncomfortable on a white background. `"System"` is not a theme itself — `ThemeManager.Resolve()` maps it to `"Light"`/`"Dark"` via the Windows registry (`AppsUseLightTheme`) before `Style.ApplyTheme` ever sees it.

`ConvertPyToExe.__init__` calls `Style.ApplyTheme(ThemeManager.Resolve(...))` before building any widgets. Startup dialogs are sequential, one at a time: splash → registration (if `verification.txt` is missing or incomplete; has a "Not Now" button that accepts without saving, so it just re-asks next launch) → splash updates to `"Welcome, {AuthorName}!"` → first-run theme picker (`ShowFirstRunThemeDialog`, only if no `theme.txt` yet; has a "Skip" button that reverts any live preview back to the current mode before closing, so an unconfirmed preview never leaks into the launched app). The Settings dialog's **Theme** tab (labeled "Theme"; radio buttons: Light/Dark/System/Developer, each paired with a live `BuildThemeSwatch` preview) live-previews via `PreviewTheme`, and both it and `SaveThemeSettings` route through `AnimateThemeChange`, which crossfades `self.MainWindow` with a `QGraphicsOpacityEffect` + `QPropertyAnimation` pair while the palette swaps underneath.

`RethemeWidgetTree(Root, OldSnapshot)` is the generic version of this snapshot-and-swap trick — it takes any widget tree, not just `self.MainWindow`. `RethemeAllWidgets` is a thin wrapper calling it with `self.MainWindow`; the first-run theme picker's `PreviewSelection` calls it directly with the picker's own `Dialog` (which isn't parented to `self.MainWindow` — it exists before `self.MainWindow` does). Previously that preview only manually re-styled the dialog background, title, and radios, silently leaving the "Continue" button stuck on whatever theme was active when the dialog opened — looking like the whole picker "wasn't updating." Route any new widget in either dialog through the shared `Style.*` attributes so it participates in this automatically.

`BuildThemeSwatch(Mode)` renders a small VS-style mockup (title bar strip, card, sample text) built directly from `PALETTES[...]`, independent of the app's currently-applied `Style` — this is what lets every radio option preview correctly even while a different theme is actually applied. It's used both in the Settings **Theme** tab and in `ShowFirstRunThemeDialog`; reuse it for any future theme-picker UI rather than hand-rolling another preview.

`CardStyle` has no border in any theme (background tint + rounded corners only) — a deliberate "clean, borderless" look used by the About tab's highlights card and the Customize tab's section cards; don't reintroduce a border there. The Customize tab's Build Type / Console Mode pickers are checkable `QPushButton`s styled with `Style.ToggleButtonStyle` (a segmented-toggle look), not `QRadioButton` — built via the local `CustomizeTogglePair()` helper in `ShowSettingsWindow`.

`Style.WindowOpacity` (from each theme's `Build()`) is `1.0` for Light/Dark and `0.76` for Developer — Light and Dark render on a fully opaque, static background, while Developer keeps the original translucent glass window. Every place that sets the theme must also call `self.MainWindow.setWindowOpacity(Style.WindowOpacity)` after `Style.ApplyTheme`, or the window opacity will silently keep the previous mode's value.

**Live re-theming:** every themed widget's stylesheet was baked in at construction time (e.g. `button.setStyleSheet(Style.ButtonStyle)`), so simply reassigning `Style.ButtonStyle` on `Style.ApplyTheme` doesn't touch already-built widgets. `SnapshotStyle()`/`RethemeAllWidgets()` fix this without editing the ~110 individual `setStyleSheet(Style.X)` call sites: `SnapshotStyle()` captures every current `Style.*` string keyed by attribute name; after `Style.ApplyTheme(newMode)` rebuilds them, `RethemeAllWidgets(oldSnapshot)` walks every live widget under `self.MainWindow` (`findChildren(QWidget)` — this also reaches any open `QDialog`, since dialogs are parented to `self.MainWindow` even though they're separate top-level windows), matches each widget's *current* stylesheet text against the old snapshot to find which attribute it came from, and reassigns the new value for that same attribute. `PreviewTheme`/`SaveThemeSettings` both snapshot before calling `Style.ApplyTheme` and retheme after, inside the `AnimateThemeChange` crossfade. When adding a new stylesheet key, add it inside each theme's `Build()` with a distinct value — a key present in one theme but missing in another will simply not exist on `Style` after switching to that theme, and two attributes that happen to share an identical string would be indistinguishable to the matcher. This bit hard once already: `NormalInputStyle` (used by every input-field validity check to reset back to the normal look) was referenced throughout `convert_py_to_exe.py` but got dropped when `style.py` was split into `Styles/`, so it was simply undefined on `Style` — any code path that touched it (typing in almost any input field) raised `AttributeError`. Each theme's `Build()` now sets `Result["NormalInputStyle"] = Result["InputStyle"]` before returning. If a similar "alias" key is ever needed again, add it the same way in every theme file, not just one.

**Splash screen:** `ShowSplashScreen()` shows a frameless themed window (icon, title, `LOADER.gif`, status text) immediately after the theme is resolved; `UpdateSplash(text)` updates the status line at each startup stage. `CloseSplash()` enforces a minimum visible duration (`self.SplashMinDurationMs`, currently 1400ms) via a local `QEventLoop` + `QTimer.singleShot` before closing — startup (settings load + file indexing) is fast enough that without this the splash would flash and disappear before being seen.

**Persistence gotcha:** `user_data.py`'s `USER_DATA_DIR` must stay a bare relative path (`"user-data"`). It was previously per-file and derived from `__file__` (e.g. `theme.py`'s old `THEME_FILE`), which resolves into PyInstaller's `_MEIPASS` folder in a frozen `.exe` — in a `--onefile` build that's a temp folder wiped after every run, so the saved theme (and the first-run picker) would silently reset on every launch. A relative path instead resolves against the working directory, which Explorer sets to the `.exe`'s own folder — this also means `user-data/` lands next to `PythonAppBuilder.exe`, not inside `--onedir`'s `_internal/`, so it survives even if `_internal/` is replaced by a future build. Don't reintroduce a `__file__`-based path for any new per-machine config file.

`Assets/` holds UI images/icons/gifs referenced via `assets_path.py` — this indirection matters because paths differ between running from source and running from a frozen `.exe` (PyInstaller `sys._MEIPASS`).

**Build defaults vs. Reset:** `CustomizationManager` values only seed the main window's build-type/console-mode radios and checkboxes once, at construction (`ConvertPyToExe.__init__`, right after they're created). `ResetTheApp()` deliberately clears all of them back to fully unchecked regardless of the saved defaults — that's existing, intentional behavior (a full reset, not "back to my defaults"); don't wire `CustomizationManager` into `ResetTheApp()`. The Customize tab's own `Default*` radios/checkboxes are a separate set of widgets that only edit the saved preference (via `SaveCustomizationDefaults`) and never reflect or affect the main window's current in-session choices.

**Bundling gotcha:** `AssetsPath.ApplicationIcon` points at `APP_BUILDER_ICON.ico` in the project root, not inside `Assets/`. `--icon` at build time only embeds it as the `.exe` file's own Explorer/taskbar-pin icon — it does **not** put the file inside the frozen app's data, so `QIcon(AssetsPath.ApplicationIcon)` silently returned a null icon at runtime (window/dialog/taskbar icon while running) until a second `--add-data "APP_BUILDER_ICON.ico;."` was added to bundle it too (also present in `PythonAppBuilder.spec`'s `datas`). Any asset referenced outside `Assets/` needs the same treatment — bundled explicitly, not assumed to come along with `--icon` or any other single-purpose flag.

## Local/runtime config (not tracked in git)

Everything the app persists about itself lives under `user-data/` (see `scripts/user_data.py` — `UserDataPath()`/`DbPath()`/`EnsureUserDataDirs()`), a plain relative path so it always resolves next to the running script or `.exe`, never into a PyInstaller temp/internal folder:

- `user-data/verification.txt` — Company/Author/Copyright/Trademark, used as default PyInstaller version metadata.
- `user-data/shortcuts.txt` — user's custom keyboard shortcut bindings.
- `user-data/theme.txt` — selected theme mode (`Light` / `Dark` / `System` / `Developer`).
- `user-data/customization.txt` — default build preferences from *Settings → Customize* (build type, console mode, shortcut/show-command checkboxes, open-folder-after-build, Start Menu path).
- `user-data/db/builds.db` — SQLite log of every successful build (`scripts/build_history.py`'s `BuildHistory`), recorded from `BuildCompletedWindow`.
- `user-data/db/py_index.db`, `user-data/db/icon_index.db` — cached `.py` / `.ico` file search indexes (`scripts/file_index_db.py`). Loaded on startup before `FileIndexerThread`/`IconIndexerThread` even start, and merged (not replaced — `{**old, **new}`, then `DELETE FROM files` + bulk insert) each time a background scan finishes (`StoreFileIndex`/`StoreIconIndex`). Merging matters: a rescan that happens to miss a folder it previously covered must not erase an entry the user already validated against. Both handlers also re-run validation on whatever's currently typed (`ValidatePythonFile`/`ValidateIconFile`, guarded by `hasattr` since the scan can finish before those widgets exist) — otherwise a field that went red only because the scan hadn't finished yet would stay red forever even after the index gained the entry.

`version_info.txt` is the one exception — it's a temporary PyInstaller version resource written next to the *target script being converted* (not this app's own data) and deleted after each build.

`ConvertPyToExe.__init__` calls `EnsureUserDataDirs()` before constructing anything that reads/writes these files. Don't assume they exist beyond that; the app prompts for `verification.txt` contents on first run.

## Build/dev commands

Run from source:
```bash
python PYTHON_APP_BUILDER.py
```

Build the distributable exe (see `PythonAppBuilder.spec` for the maintained spec):
```bash
python -m PyInstaller --noconfirm --onedir --windowed --name "PythonAppBuilder" --icon "APP_BUILDER_ICON.ico" --add-data "Assets;Assets" --add-data "APP_BUILDER_ICON.ico;." --distpath "out" --workpath "build" PYTHON_APP_BUILDER.py
```

`build/` and `out/` are PyInstaller artifacts — never commit them.

## Conventions

- No test suite exists yet — verify UI changes by actually running the app (`python PYTHON_APP_BUILDER.py`) and exercising the affected flow, since this is a GUI-heavy project where type checks don't catch UI regressions.
- Keep the dev-vs-frozen path distinction in mind: any new asset access should go through `assets_path.py`, not raw relative paths, or it will break in the built `.exe`.
- This project previously had bugs around build freezes, `ModuleNotFoundError` in the frozen exe, and missing bundled assets (see git history) — when touching `threads.py`'s `BuildThread` or the PyInstaller invocation/spec, double-check the frozen build still launches, not just that it compiles.

---

**Author:** Robin Gupta
**Assisted by:** Claude Code
