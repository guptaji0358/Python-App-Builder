import os

# Relative to the working directory (not derived from __file__) - matches
# the fix already applied to theme.py: __file__ resolves into PyInstaller's
# temp extraction folder in a --onefile build, which is wiped every run.
# A relative path stays next to the .exe in both --onefile and --onedir
# builds, since Explorer sets the working directory to the exe's own folder.
USER_DATA_DIR = "user-data"
DB_DIR = os.path.join(USER_DATA_DIR,"db")


def UserDataPath(FileName):
    return os.path.join(USER_DATA_DIR,FileName)


def DbPath(FileName):
    return os.path.join(DB_DIR,FileName)


def EnsureUserDataDirs():
    os.makedirs(DB_DIR,exist_ok=True)
