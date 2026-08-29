import os
import winreg

THEME_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "theme.txt"
)

MODES = ("Light", "Dark", "System", "Developer")


class ThemeManager:
    """Persists the user's theme preference (Light / Dark / System / Developer)
    and resolves "System" down to the OS's current light/dark setting."""

    @staticmethod
    def HasSavedChoice():
        return os.path.exists(THEME_FILE)

    @staticmethod
    def Get():
        try:
            if os.path.exists(THEME_FILE):
                with open(THEME_FILE, "r", encoding="utf-8") as File:
                    Mode = File.read().strip()
                    if Mode in MODES:
                        return Mode
        except OSError:
            pass
        return "Dark"

    @staticmethod
    def Set(Mode):
        if Mode not in MODES:
            Mode = "Dark"
        try:
            with open(THEME_FILE, "w", encoding="utf-8") as File:
                File.write(Mode)
        except OSError:
            pass

    @staticmethod
    def DetectSystemMode():
        """Reads the Windows "Apps use light theme" registry setting."""
        try:
            Key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            Value, _ = winreg.QueryValueEx(Key, "AppsUseLightTheme")
            winreg.CloseKey(Key)
            return "Light" if Value == 1 else "Dark"
        except OSError:
            return "Dark"

    @classmethod
    def Resolve(cls, Mode=None):
        """Returns the actual palette to render ("Light"/"Dark"/"Developer"),
        resolving "System" against the current OS setting."""
        Mode = Mode or cls.Get()
        if Mode == "System":
            return cls.DetectSystemMode()
        return Mode
