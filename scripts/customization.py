import os

from .user_data import UserDataPath

CUSTOMIZATION_FILE = UserDataPath("customization.txt")

DEFAULTS = {
    "DefaultBuildType": "OneFile",
    "DefaultConsoleMode": "NoConsole",
    "DefaultCreateShortcut": "False",
    "DefaultShowCommand": "False",
    "OpenFolderAfterBuild": "False",
    "StartMenuPath": "",
}


class CustomizationManager:
    """Persists default build preferences (build type, console mode, Start
    Menu shortcut path, etc.) that seed the main window on the next launch,
    plus a couple of always-on build behaviors like auto-opening the output
    folder. Stored the same way as ShortcutManager - flat key=value lines."""

    def __init__(self):
        self.Values = dict(DEFAULTS)
        self.Load()

    def Load(self):
        if not os.path.exists(CUSTOMIZATION_FILE):
            return

        try:
            with open(CUSTOMIZATION_FILE,"r",encoding="utf-8") as File:
                for Line in File:
                    if "=" not in Line:
                        continue

                    Key,Value = Line.strip().split("=",1)

                    if Key in self.Values:
                        self.Values[Key] = Value
        except Exception:
            pass

    def Save(self):
        with open(CUSTOMIZATION_FILE,"w",encoding="utf-8") as File:
            for Key,Value in self.Values.items():
                File.write(f"{Key}={Value}\n")

    def Get(self,Name):
        return self.Values.get(Name,DEFAULTS.get(Name,""))

    def GetBool(self,Name):
        return self.Get(Name) == "True"

    def Set(self,Name,Value):
        self.Values[Name] = str(Value)
