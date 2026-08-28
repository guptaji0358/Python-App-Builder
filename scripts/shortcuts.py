import os

SHORTCUTS_FILE = "shortcuts.txt"

DEFAULT_SHORTCUTS = {
    "AddAsset": "Ctrl+Shift+A",
    "BrowseMultipleAssets": "Ctrl+Shift+B",
    "RemoveLastAsset": "Ctrl+Shift+R",
}

SHORTCUT_LABELS = {
    "AddAsset": "Add Asset",
    "BrowseMultipleAssets": "Browse Multiple Assets",
    "RemoveLastAsset": "Remove Last Asset",
}


class ShortcutManager:

    def __init__(self):
        self.Shortcuts = dict(DEFAULT_SHORTCUTS)
        self.Load()

    def Load(self):
        if not os.path.exists(SHORTCUTS_FILE):
            return

        try:
            with open(SHORTCUTS_FILE,"r",encoding="utf-8") as File:
                for Line in File:
                    if "=" not in Line:
                        continue

                    Key,Value = Line.strip().split("=",1)

                    if Key in self.Shortcuts and Value:
                        self.Shortcuts[Key] = Value
        except Exception:
            pass

    def Save(self):
        with open(SHORTCUTS_FILE,"w",encoding="utf-8") as File:
            for Key,Value in self.Shortcuts.items():
                File.write(f"{Key}={Value}\n")

    def Get(self,Name):
        return self.Shortcuts.get(Name,DEFAULT_SHORTCUTS.get(Name,""))

    def Set(self,Name,KeySequenceText):
        self.Shortcuts[Name] = KeySequenceText
