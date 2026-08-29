from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

from .assets_path import AssetsPath
from .Styles import PALETTES, THEMES


class Style:
    Mode = "Dark"

    @classmethod
    def ApplyTheme(cls, Mode):
        """Swaps every stylesheet constant to the theme built for Mode
        ("Light" / "Dark" / "Developer") so the whole app can switch themes.
        Each theme's stylesheets come pre-built from scripts/Styles/ - one
        theme's look never leaks into another's."""
        Attrs = THEMES.get(Mode, THEMES["Dark"])
        cls.Mode = Mode if Mode in THEMES else "Dark"

        for Key, Value in Attrs.items():
            setattr(cls, Key, Value)

    @staticmethod
    def Shadow(widget):
        Glow = QGraphicsDropShadowEffect()
        Glow.setBlurRadius(40)
        Glow.setOffset(0,0)
        Glow.setColor(QColor(0,170,255,200))
        widget.setGraphicsEffect(Glow)

    @staticmethod
    def TextGlow(widget):
        Glow = QGraphicsDropShadowEffect()
        Glow.setBlurRadius(20)
        Glow.setOffset(0,0)
        Glow.setColor(QColor(0,255,255,200))
        widget.setGraphicsEffect(Glow)

    @staticmethod
    def AddButtonGlow():
        Glow = QGraphicsDropShadowEffect()
        Glow.setBlurRadius(60)
        Glow.setOffset(0,0)
        Glow.setColor(QColor(0,255,255,255))

    @staticmethod
    def DangerShadow(widget):
        Glow = QGraphicsDropShadowEffect()
        Glow.setBlurRadius(30)
        Glow.setOffset(0,0)
        Glow.setColor(QColor(255,80,80,220))
        widget.setGraphicsEffect(Glow)


Style.ApplyTheme(Style.Mode)
