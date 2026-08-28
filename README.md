# Python App Builder

A PySide6 desktop tool that converts Python (`.py`) scripts into standalone Windows executables (`.exe`) using [PyInstaller](https://pyinstaller.org/) — without having to write PyInstaller commands by hand.

## Features

- Convert any `.py` file into a One-File or One-Dir executable
- Pick a custom app icon, name, version, and description
- Add extra assets (images, fonts, audio, etc.) that get bundled with the build and copied next to the output `.exe`
- Console / windowed mode toggle
- Live build progress with cancel support
- Preview (and edit) the generated PyInstaller command before building
- Create a Start Menu shortcut for the built app
- **Editable registration details** (Company, Author, Copyright, Trademark) used as the built app's version metadata — required on first run, editable anytime from *Settings → Verify*
- **Editable keyboard shortcuts** from *Settings → Shortcut*, including `Ctrl+Shift+Enter` to jump to the next input field

## Project Structure

```
App Builder/
├── PYTHON_APP_BUILDER.py     # Entry point — launches the app
├── APP_BUILDER_ICON.ico      # App icon
├── Assets/                   # All .svg / .png / .gif UI assets
├── scripts/                  # Application source, split into modules
│   ├── convert_py_to_exe.py  # Main window / app logic (ConvertPyToExe)
│   ├── threads.py            # Background QThreads (file indexing, icon indexing, build)
│   ├── style.py               # Qt stylesheets and visual effects
│   ├── messages.py            # Shared QMessageBox dialogs
│   ├── shortcuts.py           # Editable keyboard shortcut manager
│   └── assets_path.py         # Resolves paths to files in Assets/
└── out/                       # Compiled .exe output (generated, not tracked)
```

## Requirements

- Python 3.10+
- [PySide6](https://pypi.org/project/PySide6/)
- [pywin32](https://pypi.org/project/pywin32/) (for Start Menu shortcut creation)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (used both to build this app, and by this app to build other apps)

Install dependencies:

```bash
pip install PySide6 pywin32 pyinstaller
```

## Running from Source

```bash
python PYTHON_APP_BUILDER.py
```

On first run you'll be asked to fill in Company Name, Author, Copyright, and Trademark — these are saved locally to `verification.txt` and used as default version metadata for apps you build.

## Building the Executable

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

## Local Config Files

These are generated at runtime and are not tracked in git (per-machine settings):

- `verification.txt` — Company/Author/Copyright/Trademark
- `shortcuts.txt` — custom keyboard shortcuts
- `version_info.txt` — temporary PyInstaller version resource file, written next to the script being converted and cleaned up after each build
