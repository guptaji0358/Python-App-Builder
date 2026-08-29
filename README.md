<div align="center">

# 🛠️ Python App Builder

**Convert Python scripts into standalone Windows executables — without touching a terminal.**

A PySide6 desktop tool that wraps [PyInstaller](https://pyinstaller.org/) in a clean, guided UI so you never have to hand-write a build command again.

[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)](#requirements)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](#requirements)
[![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/license-Unlicensed-lightgrey)](#license)

</div>

---

## ✨ Features

| | |
|---|---|
| 📦 **One-File / One-Dir builds** | Convert any `.py` file into a single `.exe` or a folder distribution |
| 🎨 **Custom branding** | Set a custom app icon, name, version, and description |
| 🖼️ **Bundle extra assets** | Images, fonts, audio, and other files get packed into the build and copied next to the output `.exe` |
| 🖥️ **Console / windowed toggle** | Choose whether the built app shows a console window |
| 📊 **Live build progress** | Real-time output with cancel support mid-build |
| 🔍 **Command preview** | Inspect (and edit) the generated PyInstaller command before it runs |
| 🔗 **Start Menu shortcuts** | Optionally create a shortcut for the built app |
| 🪪 **Editable version metadata** | Company, Author, Copyright, and Trademark are saved once and reused for every build (*Settings → Verify*) |
| ⌨️ **Editable keyboard shortcuts** | Rebind shortcuts from *Settings → Shortcut*, including `Ctrl+Shift+Enter` to jump to the next input field |

---

## 📁 Project Structure

```
App Builder/
├── PYTHON_APP_BUILDER.py     # Entry point — launches the app
├── APP_BUILDER_ICON.ico      # App icon
├── Assets/                   # All .svg / .png / .gif UI assets
├── scripts/                  # Application source, split into modules
│   ├── convert_py_to_exe.py  #   Main window / app logic (ConvertPyToExe)
│   ├── threads.py            #   Background QThreads (file indexing, icon indexing, build)
│   ├── style.py               #   Qt stylesheets and visual effects
│   ├── messages.py            #   Shared QMessageBox dialogs
│   ├── shortcuts.py           #   Editable keyboard shortcut manager
│   └── assets_path.py         #   Resolves paths to files in Assets/
└── out/                       # Compiled .exe output (generated, not tracked)
```

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- [PySide6](https://pypi.org/project/PySide6/)
- [pywin32](https://pypi.org/project/pywin32/) — needed for Start Menu shortcut creation
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
python -m PyInstaller --noconfirm --onefile --windowed ^
  --name "PythonAppBuilder" ^
  --icon "APP_BUILDER_ICON.ico" ^
  --add-data "Assets;Assets" ^
  --distpath "out" ^
  --workpath "build" ^
  PYTHON_APP_BUILDER.py
```

The resulting `PythonAppBuilder.exe` will be in `out/`.

---

## ⚙️ Local Config Files

Generated at runtime, per-machine, and **not tracked in git**:

| File | Purpose |
|---|---|
| `verification.txt` | Company / Author / Copyright / Trademark |
| `shortcuts.txt` | Custom keyboard shortcuts |
| `version_info.txt` | Temporary PyInstaller version resource file — written next to the script being converted, cleaned up after each build |

---

## 📄 License

No license specified yet.

---

<div align="center">

**Author:** Robin Gupta · **Assisted by:** Claude Code

</div>
