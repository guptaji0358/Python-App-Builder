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
| `style.py` | Qt stylesheets (`Style` class) and visual effects — no logic. |
| `messages.py` | Shared `QMessageBox` dialog helpers (`Messages` class). |
| `shortcuts.py` | `ShortcutManager` — editable keyboard shortcuts, persisted to `shortcuts.txt`. |
| `assets_path.py` | Resolves paths into `Assets/` (handles dev vs. frozen/PyInstaller-bundled paths via `AssetPath` / `AssetsPath`). |

`Assets/` holds UI images/icons/gifs referenced via `assets_path.py` — this indirection matters because paths differ between running from source and running from a frozen `.exe` (PyInstaller `sys._MEIPASS`).

## Local/runtime config (not tracked in git)

- `verification.txt` — Company/Author/Copyright/Trademark, used as default PyInstaller version metadata.
- `shortcuts.txt` — user's custom keyboard shortcut bindings.
- `version_info.txt` — temporary PyInstaller version resource, written next to the target script and deleted after each build.

Don't assume these files exist; the app prompts for `verification.txt` contents on first run.

## Build/dev commands

Run from source:
```bash
python PYTHON_APP_BUILDER.py
```

Build the distributable exe (see `PythonAppBuilder.spec` for the maintained spec):
```bash
python -m PyInstaller --noconfirm --onefile --windowed --name "PythonAppBuilder" --icon "APP_BUILDER_ICON.ico" --add-data "Assets;Assets" --distpath "out" --workpath "build" PYTHON_APP_BUILDER.py
```

`build/` and `out/` are PyInstaller artifacts — never commit them.

## Conventions

- No test suite exists yet — verify UI changes by actually running the app (`python PYTHON_APP_BUILDER.py`) and exercising the affected flow, since this is a GUI-heavy project where type checks don't catch UI regressions.
- Keep the dev-vs-frozen path distinction in mind: any new asset access should go through `assets_path.py`, not raw relative paths, or it will break in the built `.exe`.
- This project previously had bugs around build freezes, `ModuleNotFoundError` in the frozen exe, and missing bundled assets (see git history) — when touching `threads.py`'s `BuildThread` or the PyInstaller invocation/spec, double-check the frozen build still launches, not just that it compiles.

---

**Author:** Robin Gupta
**Assisted by:** Claude Code
