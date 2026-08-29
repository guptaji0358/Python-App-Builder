<div align="center">

# 🛠️ Python App Builder

**Convert Python scripts into standalone Windows executables — without touching a terminal.**

A PySide6 desktop tool that wraps [PyInstaller](https://pyinstaller.org/) in a clean, guided UI so you never have to hand-write a build command again.

[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)](#-requirements)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#-requirements)
[![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
[![PyInstaller](https://img.shields.io/badge/powered%20by-PyInstaller-FFD43B?logo=python&logoColor=black)](https://pyinstaller.org/)
[![Theme](https://img.shields.io/badge/theme-Light%20%7C%20Dark%20%7C%20System%20%7C%20Developer-8A2BE2)](#-theming)
[![License](https://img.shields.io/badge/license-Unlicensed-lightgrey)](#-license)

<sub>Author **Robin Gupta** · Assisted by **Claude Code**</sub>

</div>

<br>

## 📚 Table of Contents

- [Features](#-features)
- [Theming](#-theming)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Settings Reference](#-settings-reference)
- [Local Config Files](#-local-config-files)
- [Roadmap](#-roadmap)
- [License](#-license)

<br>

## ✨ Features

<table>
<tr><td>📦</td><td><b>One-File / One-Dir builds</b></td><td>Convert any <code>.py</code> file into a single <code>.exe</code> or a folder distribution</td></tr>
<tr><td>🎨</td><td><b>Custom branding</b></td><td>Set a custom app icon, name, version, and description</td></tr>
<tr><td>🖼️</td><td><b>Bundle extra assets</b></td><td>Images, fonts, audio, and other files get packed into the build and copied next to the output <code>.exe</code></td></tr>
<tr><td>🖥️</td><td><b>Console / windowed toggle</b></td><td>Choose whether the built app shows a console window</td></tr>
<tr><td>📊</td><td><b>Live build progress</b></td><td>Real-time output with cancel support mid-build</td></tr>
<tr><td>🔍</td><td><b>Command preview</b></td><td>Inspect (and edit) the generated PyInstaller command before it runs</td></tr>
<tr><td>🔗</td><td><b>Start Menu shortcuts</b></td><td>Optionally create a shortcut for the built app, with a customizable install path</td></tr>
<tr><td>🪪</td><td><b>Editable version metadata</b></td><td>Company, Author, Copyright, and Trademark are saved once and reused for every build</td></tr>
<tr><td>⌨️</td><td><b>Editable keyboard shortcuts</b></td><td>Rebind shortcuts from <i>Settings → Shortcut</i>, including <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Enter</kbd> to jump to the next input field and <kbd>Ctrl</kbd>+<kbd>.</kbd> to open Settings</td></tr>
<tr><td>🌗</td><td><b>Light / Dark / System / Developer theme</b></td><td>Switch appearance from <i>Settings → Theme</i>, with an animated crossfade on every change — auto-follows Windows when set to System</td></tr>
<tr><td>👋</td><td><b>First-run theme picker</b></td><td>A one-time dialog lets you pick your theme the very first time the app launches</td></tr>
<tr><td>💫</td><td><b>Splash screen</b></td><td>A themed splash window shows startup progress (settings, file indexing, interface) while the app loads</td></tr>
<tr><td>🧩</td><td><b>Build defaults</b></td><td>Pick a default build type, console mode, shortcut/command checkboxes, and auto-open-output-folder from <i>Settings → Customize</i> — applied on every fresh launch</td></tr>
<tr><td>🗃️</td><td><b>Build history</b></td><td>Every successful build is logged to a local SQLite database (<code>user-data/db/builds.db</code>)</td></tr>
</table>

<br>

## 🌗 Theming

The very first time you launch the app, a **theme picker** appears so you can choose your look before anything else loads — your choice is remembered from then on (`theme.txt`), so it's a one-time ask, not a repeat prompt. Change it later from **Settings → Theme**.

Each option shows a **VS-style live swatch** — a miniature preview of that theme's title bar, card, and text — right next to its radio button, so you see the look before you pick it:

| Mode | Behavior |
|---|---|
| ☀️ **Light** | A clean, bright, fully opaque palette |
| 🌙 **Dark** | A refreshed slate-navy, fully opaque palette *(default)* |
| 🖥️ **System** | Follows the Windows "Choose your mode" setting automatically |
| 🧑‍💻 **Developer** | The app's original hand-tuned look — translucent window included — kept as its own selectable mode |

Light and Dark render on a **static, solid background** (no see-through window); Developer keeps the original translucent glass look. Every switch — in the picker or in Settings — **crossfades** the window instead of snapping instantly.

The panel shows the **currently resolved mode** live (e.g. `System → Dark`) and previews your selection instantly — every button, input, card, and open dialog repaints immediately, no restart needed. Your choice is saved to `theme.txt` and restored on the next launch.

<br>

## 📁 Project Structure

```
App Builder/
├── PYTHON_APP_BUILDER.py     # Entry point — launches the app
├── APP_BUILDER_ICON.ico      # App icon
├── Assets/                   # All .svg / .png / .gif UI assets
├── scripts/                  # Application source, split into modules
│   ├── convert_py_to_exe.py  #   Main window / app logic (ConvertPyToExe)
│   ├── threads.py            #   Background QThreads (file indexing, icon indexing, build)
│   ├── style.py               #   Themeable Qt stylesheets and visual effects
│   ├── Styles/                 #   One file per theme (light.py / dark.py / developer.py) + registry
│   ├── theme.py                #   Light/Dark/System/Developer theme persistence + OS detection
│   ├── customization.py        #   Default build preferences (Settings > Customize), persisted to customization.txt
│   ├── user_data.py            #   Resolves the user-data/ folder every persistence module writes into
│   ├── build_history.py        #   SQLite build history log (user-data/db/builds.db)
│   ├── file_index_db.py        #   Separate SQLite caches for the .py / .ico search indexes
│   ├── messages.py            #   Shared QMessageBox dialogs
│   ├── shortcuts.py           #   Editable keyboard shortcut manager
│   └── assets_path.py         #   Resolves paths to files in Assets/
└── out/                       # Compiled .exe output (generated, not tracked)
```

<br>

## 🚀 Getting Started

### Requirements

- Python 3.10+
- [PySide6](https://pypi.org/project/PySide6/)
- [pywin32](https://pypi.org/project/pywin32/) — needed for Start Menu shortcut creation and System theme detection
- [PyInstaller](https://pypi.org/project/pyinstaller/) — used both to build this app, and by this app to build other apps

```bash
pip install PySide6 pywin32 pyinstaller
```

### Run from source

```bash
python PYTHON_APP_BUILDER.py
```

On first run you'll be asked to fill in **Company Name, Author, Copyright, and Trademark** — these are saved locally to `verification.txt` and used as default version metadata for apps you build.

### Build the executable

```bash
python -m PyInstaller --noconfirm --onedir --windowed ^
  --name "PythonAppBuilder" ^
  --icon "APP_BUILDER_ICON.ico" ^
  --add-data "Assets;Assets" ^
  --add-data "APP_BUILDER_ICON.ico;." ^
  --distpath "out" ^
  --workpath "build" ^
  PYTHON_APP_BUILDER.py
```

This is a **standalone folder build** (`--onedir`), not a single `.exe` — the app ships as `out/PythonAppBuilder/` (containing `PythonAppBuilder.exe` and an `_internal/` folder with its bundled runtime and assets). Distribute the whole folder. `user-data/` is created next to `PythonAppBuilder.exe` on first run, outside `_internal/`, so your settings and build history survive even if `_internal/` gets replaced by a future build.

<br>

## ⚙️ Settings Reference

The gear icon opens a tabbed **Settings** window:

| Tab | Purpose |
|---|---|
| **Verify** | Company Name, Author, Copyright, Trademark used as build metadata |
| **Shortcut** | Rebind every keyboard shortcut in the app |
| **Customize** | Start Menu shortcut path, plus default build type / console mode / shortcut / show-command / open-folder-after-build preferences that seed every new build |
| **Theme** | Light / Dark / System / Developer theme switch, animated on change |
| **About** | App name, version, feature highlights, credits, and links to the GitHub repo / issue tracker |

<br>

## 🗂️ Local Config Files

Generated at runtime, per-machine, and **not tracked in git**. Everything the app owns lives under **`user-data/`**, created next to the running script (or `.exe`) on first launch:

| File | Purpose |
|---|---|
| `user-data/verification.txt` | Company / Author / Copyright / Trademark |
| `user-data/shortcuts.txt` | Custom keyboard shortcuts |
| `user-data/theme.txt` | Selected theme mode (`Light` / `Dark` / `System` / `Developer`) |
| `user-data/customization.txt` | Default build preferences set from *Settings → Customize* |
| `user-data/db/builds.db` | SQLite log of every successful build (app name, output path, size, timestamp) |
| `user-data/db/py_index.db` | Cached `.py` file search index, for instant autocomplete on startup |
| `user-data/db/icon_index.db` | Cached `.ico` file search index, for instant autocomplete on startup |
| `version_info.txt` | Temporary PyInstaller version resource file — written next to the *script being converted*, cleaned up after each build (not part of `user-data/`) |

<br>

## 🧭 Roadmap

- [ ] Recent-builds history panel
- [ ] Per-project build presets

<br>

## 📄 License

No license specified yet.

---

<div align="center">

**Author:** Robin Gupta · **Assisted by:** Claude Code

</div>
