from PySide6.QtWidgets import QGraphicsDropShadowEffect
from PySide6.QtGui import QColor

from .assets_path import AssetsPath

PALETTES = {
    # The app's original hand-tuned look, kept exactly as-is and offered as
    # its own selectable mode for anyone who prefers the classic style.
    "Developer": {
        "WindowBg": "rgba(20,20,20,55)",
        "Text": "white",
        "SubText": "rgba(255,255,255,180)",
        "CardBg": "rgba(255,255,255,15)",
        "CardBorder": "rgba(255,255,255,40)",
        "DialogBg": "rgba(15,20,30,240)",
        "InputBg": "rgba(0,170,255,40)",
        "InputHoverBg": "rgba(0,170,255,40)",
        "InputFocusBg": "rgba(0,170,255,80)",
        "InputDisabledBg": "rgba(100,100,100,40)",
        "InputDisabledText": "rgba(255,255,255,120)",
        "InputDisabledBorder": "rgba(255,255,255,30)",
        "ComboBg": "rgba(30,41,59,180)",
        "ComboBorder": "rgba(255,255,255,40)",
        "SecondaryBg": "rgba(255,255,255,18)",
        "SecondaryHoverBg": "rgba(255,255,255,28)",
        "SecondaryPressedBg": "rgba(255,255,255,40)",
        "SecondaryDisabledBg": "rgba(255,255,255,8)",
        "SecondaryDisabledText": "rgba(255,255,255,90)",
        "SecondaryDisabledBorder": "rgba(255,255,255,20)",
        "ScrollTrack": "#20242C",
        "ScrollHandle": "rgba(255,255,255,40)",
        "TextEditBg": "rgba(0,0,0,120)",
        "AssetCardBg": "rgba(255,255,255,12)",
        "AssetCardBorder": "rgba(255,255,255,50)",
    },
    # A fresh, opaque slate-navy dark theme — distinct from "Developer".
    "Dark": {
        "WindowBg": "rgba(15,18,26,235)",
        "Text": "#EAF0FF",
        "SubText": "rgba(234,240,255,170)",
        "CardBg": "rgba(255,255,255,10)",
        "CardBorder": "rgba(120,170,255,45)",
        "DialogBg": "rgba(12,16,26,250)",
        "InputBg": "rgba(80,120,255,35)",
        "InputHoverBg": "rgba(80,120,255,35)",
        "InputFocusBg": "rgba(80,120,255,70)",
        "InputDisabledBg": "rgba(90,90,100,40)",
        "InputDisabledText": "rgba(234,240,255,110)",
        "InputDisabledBorder": "rgba(234,240,255,25)",
        "ComboBg": "rgba(24,30,46,200)",
        "ComboBorder": "rgba(120,170,255,40)",
        "SecondaryBg": "rgba(255,255,255,14)",
        "SecondaryHoverBg": "rgba(255,255,255,22)",
        "SecondaryPressedBg": "rgba(255,255,255,34)",
        "SecondaryDisabledBg": "rgba(255,255,255,6)",
        "SecondaryDisabledText": "rgba(234,240,255,85)",
        "SecondaryDisabledBorder": "rgba(234,240,255,18)",
        "ScrollTrack": "#161B26",
        "ScrollHandle": "rgba(120,170,255,45)",
        "TextEditBg": "rgba(6,8,14,150)",
        "AssetCardBg": "rgba(255,255,255,8)",
        "AssetCardBorder": "rgba(120,170,255,45)",
    },
    "Light": {
        "WindowBg": "rgba(245,247,250,255)",
        "Text": "#111318",
        "SubText": "rgba(17,19,24,160)",
        "CardBg": "rgba(0,0,0,6)",
        "CardBorder": "rgba(0,0,0,25)",
        "DialogBg": "rgba(255,255,255,250)",
        "InputBg": "rgba(0,120,220,16)",
        "InputHoverBg": "rgba(0,120,220,16)",
        "InputFocusBg": "rgba(0,120,220,35)",
        "InputDisabledBg": "rgba(0,0,0,15)",
        "InputDisabledText": "rgba(17,19,24,120)",
        "InputDisabledBorder": "rgba(0,0,0,25)",
        "ComboBg": "rgba(255,255,255,220)",
        "ComboBorder": "rgba(0,0,0,30)",
        "SecondaryBg": "rgba(0,0,0,7)",
        "SecondaryHoverBg": "rgba(0,0,0,12)",
        "SecondaryPressedBg": "rgba(0,0,0,18)",
        "SecondaryDisabledBg": "rgba(0,0,0,4)",
        "SecondaryDisabledText": "rgba(17,19,24,90)",
        "SecondaryDisabledBorder": "rgba(0,0,0,15)",
        "ScrollTrack": "#E3E6EB",
        "ScrollHandle": "rgba(0,0,0,35)",
        "TextEditBg": "rgba(0,0,0,10)",
        "AssetCardBg": "rgba(0,0,0,5)",
        "AssetCardBorder": "rgba(0,0,0,30)",
    },
}


class Style:
    Mode = "Dark"

    @classmethod
    def ApplyTheme(cls, Mode):
        """Rebuilds every stylesheet constant from the palette for Mode
        ("Dark" or "Light") so the whole app can switch themes."""
        Palette = PALETTES.get(Mode, PALETTES["Dark"])
        cls.Mode = Mode if Mode in PALETTES else "Dark"

        # Only the original "Developer" look uses a see-through window;
        # Dark and Light render on a fully opaque, static background.
        cls.WindowOpacity = 0.76 if cls.Mode == "Developer" else 1.0

        # The Light palette is bright, so white check/radio glyphs and
        # low-alpha white overlays need swapping for higher-contrast ones.
        IsLight = cls.Mode == "Light"
        CheckedIcon = AssetsPath.CheckedOnLight if IsLight else AssetsPath.Checked
        UncheckedIcon = AssetsPath.UncheckedOnLight if IsLight else AssetsPath.Unchecked
        AccentAlpha = 235 if IsLight else 40
        AccentHoverAlpha = 235 if IsLight else 40
        AccentPressedAlpha = 255 if IsLight else 80

        cls.MainWindowStyle = f"""
                                QWidget
                                        {{
                                            background: {Palette['WindowBg']};
                                            color:{Palette['Text']};
                                        }}
                        """

        cls.InputStyle = f"""
                            QLineEdit
                                        {{
                                            background-color: {Palette['InputBg']};
                                            color: {Palette['Text']};
                                            border:none;
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(0,170,255,180);
                                            selection-color: white;
                                        }}

                            QLineEdit:hover
                                            {{
                                                background-color: {Palette['InputHoverBg']};
                                                border: 3px solid rgba(0,170,255,180);
                                            }}

                            QLineEdit:focus
                                            {{
                                                background-color: {Palette['InputFocusBg']};
                                                border: 2px solid rgba(0,220,255,255);
                                                color: {Palette['Text']};
                                            }}

                            QLineEdit:disabled
                                                {{
                                                    background-color: {Palette['InputDisabledBg']};
                                                    color: {Palette['InputDisabledText']};
                                                    border: 1px solid {Palette['InputDisabledBorder']};
                                                }}
                            """

        cls.ComboBoxStyle = f"""
                                QComboBox
                                            {{
                                                background-color: {Palette['ComboBg']};
                                                color:{Palette['Text']};
                                                border:1px solid {Palette['ComboBorder']};
                                                border-radius:12px;
                                                padding:10px;
                                            }}

                                QComboBox:hover
                                                {{
                                                    border:1px solid rgb(59,130,246);
                                                }}

                                QComboBox QAbstractItemView
                                                            {{
                                                                background-color: {Palette['DialogBg']};
                                                                color: {Palette['Text']};
                                                                border: 1px solid {Palette['ComboBorder']};
                                                                outline: none;
                                                                selection-background-color: rgba(0,170,255,120);
                                                                selection-color: white;
                                                            }}
                        """

        cls.CardStyle = f"""
                        QFrame
                                {{
                                    background: {Palette['CardBg']};
                                    border:1px solid {Palette['CardBorder']};
                                    border-radius:18px;
                                }}
                    """

        cls.ButtonStyle = f"""
                            QPushButton
                                        {{
                                            background: rgba(0,170,255,{AccentAlpha});
                                            border:none;
                                            border-radius:20px;
                                            color:white;
                                            padding:12px;
                                            font-size:11pt;
                                            font-weight:700;
                                        }}

                            QPushButton:hover
                                                {{
                                                    background: rgba(0,170,255,{AccentHoverAlpha});
                                                    border:3px solid rgba(0,170,255,255);
                                                }}

                            QPushButton:pressed
                                                {{
                                                    background: rgba(0,170,255,{AccentPressedAlpha});
                                                }}
                    """

        cls.SecondaryButtonStyle = f"""
                                    QPushButton
                                                {{
                                                    background: {Palette['SecondaryBg']};
                                                    color: {Palette['Text']};
                                                    border: none;
                                                    border-radius: 20px;
                                                    padding: 12px 24px;
                                                    font-size: 11pt;
                                                    font-weight: 800;
                                                }}

                                    QPushButton:hover
                                                        {{
                                                            background: {Palette['SecondaryHoverBg']};
                                                            border: 2px solid rgba(0,220,255,180);
                                                            color: {Palette['Text']};
                                                        }}

                                    QPushButton:pressed
                                                            {{
                                                                background: {Palette['SecondaryPressedBg']};
                                                                border: 2px solid rgba(0,255,255,255);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }}

                                    QPushButton:disabled
                                                            {{
                                                                background: {Palette['SecondaryDisabledBg']};
                                                                color: {Palette['SecondaryDisabledText']};
                                                                border: 2px solid {Palette['SecondaryDisabledBorder']};
                                                            }}
                            """

        cls.LabelStyle = f"""
                            QLabel
                                    {{
                                        color:{Palette['Text']};
                                        font-size:11pt;
                                        font-weight:bold;
                                    }}
                    """

        cls.RemoveAssetButtonStyle = """
                                        QPushButton
                                                    {
                                                        background: rgba(255,80,80,20);
                                                        border:none;
                                                        border-radius: 18px;
                                                        min-width: 36px;
                                                        max-width: 36px;
                                                        min-height: 36px;
                                                        max-height: 36px;
                                                        padding: 4px;
                                                    }

                                        QPushButton:hover
                                                            {
                                                                background: rgba(255,80,80,45);
                                                                border: 2px solid rgba(255,120,120,200);
                                                            }

                                        QPushButton:pressed
                                                            {
                                                                background: rgba(255,40,40,90);
                                                                border:none;
                                                            }
                                """

        cls.InvalidInputStyle = f"""
                            QLineEdit
                                        {{
                                            background-color: rgba(255,120,120,18);
                                            color: {Palette['Text']};
                                            border: 1px solid rgba(255,120,120,180);
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(0,170,255,180);
                                            selection-color: white;
                                        }}

                            QLineEdit:hover
                                            {{
                                                background-color: rgba(255,120,120,25);
                                                border: 1px solid rgba(255,150,150,220);
                                            }}

                            QLineEdit:focus
                                            {{
                                                background-color: rgba(255,120,120,35);
                                                border: 2px solid rgba(255,150,150,255);
                                                color: {Palette['Text']};
                                            }}

                            QLineEdit:disabled
                                                {{
                                                    background-color: {Palette['InputDisabledBg']};
                                                    color: {Palette['InputDisabledText']};
                                                    border: 1px solid {Palette['InputDisabledBorder']};
                                                }}
                            """

        cls.NormalInputStyle = cls.InputStyle

        cls.CheckBoxStyle = f"""
                                QCheckBox
                                            {{
                                                color: {Palette['Text']};
                                                font-size: 11pt;
                                                font-weight: 700;
                                                padding-left: 12px;
                                            }}

                                QCheckBox::indicator
                                                        {{
                                                            width: 28px;
                                                            height: 28px;
                                                            border-radius: 10px;
                                                            background:none;
                                                            border: 1px solid {Palette['CardBorder']};
                                                        }}

                                QCheckBox::indicator:hover
                                                            {{
                                                                background: rgba(0,170,255,40);
                                                                border: none;
                                                            }}

                                QCheckBox::indicator:pressed
                                                                {{
                                                                    background:none;
                                                                    border:none;
                                                                }}

                                QCheckBox::indicator:checked
                                                                {{
                                                                    image: url({CheckedIcon});
                                                                    border: none;
                                                                }}

                                QCheckBox::indicator:checked:hover
                                                                    {{
                                                                        background: rgba(0,170,255,40);
                                                                        border:none;
                                                                    }}
                        """

        cls.RadioButtonStyle = f"""
                                QRadioButton
                                            {{
                                                color: {Palette['Text']};
                                                font-size: 11pt;
                                                font-weight: 700;
                                                spacing: 12px;
                                            }}

                                QRadioButton::indicator
                                                        {{
                                                            width: 24px;
                                                            height: 24px;
                                                        }}

                                QRadioButton::indicator:unchecked
                                                                    {{
                                                                        image: url({UncheckedIcon});
                                                                    }}

                                QRadioButton::indicator:checked
                                                                {{
                                                                    image: url({AssetsPath.RadioChecked});
                                                                }}
                            """

        cls.ScrollAreaStyle = f"""
                                QScrollArea
                                            {{
                                                border:none;
                                                background:transparent;
                                            }}

                                QScrollBar:vertical
                                                    {{
                                                        background:{Palette['ScrollTrack']};
                                                        width:12px;
                                                        border-radius:6px;
                                                    }}

                                QScrollBar::handle:vertical
                                                            {{
                                                                background:#4A90E2;
                                                                border-radius:6px;
                                                            }}

                                QScrollBar::add-line:vertical,
                                QScrollBar::sub-line:vertical
                                                                {{
                                                                    height:0px;
                                                                }}
                                """

        cls.DialogStyle = f"""
                                QDialog
                                        {{
                                            background: {Palette['DialogBg']};
                                            border: 2px solid rgba(0,170,255,120);
                                            border-radius: 24px;
                                        }}

                                QLabel
                                        {{
                                            color: {Palette['Text']};
                                            font-size: 11pt;
                                            font-weight: 700;
                                        }}

                                QTextEdit
                                            {{
                                                background: {Palette['TextEditBg']};
                                                color: {Palette['Text']};
                                                border: 1px solid rgba(0,170,255,100);
                                                border-radius: 16px;
                                                padding: 12px;
                                            }}

                                QTabWidget::pane
                                                {{
                                                    background: {Palette['CardBg']};
                                                    border: 1px solid {Palette['CardBorder']};
                                                    border-radius: 14px;
                                                    top: -1px;
                                                }}

                                QTabBar::tab
                                                {{
                                                    background: {Palette['SecondaryBg']};
                                                    color: {Palette['Text']};
                                                    border: 1px solid {Palette['CardBorder']};
                                                    border-bottom: none;
                                                    border-top-left-radius: 10px;
                                                    border-top-right-radius: 10px;
                                                    padding: 8px 16px;
                                                    margin-right: 2px;
                                                    font-size: 10pt;
                                                    font-weight: 700;
                                                }}

                                QTabBar::tab:hover
                                                    {{
                                                        background: rgba(0,170,255,{AccentHoverAlpha});
                                                        color: white;
                                                    }}

                                QTabBar::tab:selected
                                                        {{
                                                            background: rgba(0,170,255,{AccentPressedAlpha});
                                                            color: white;
                                                        }}
                        """

        cls.ProgressBarStyle = """
                                QProgressBar
                                                {
                                                    background: rgba(20,20,20,130);
                                                    border: 1px solid rgba(255,255,255,60);
                                                    border-radius: 10px;
                                                    padding: 0px;
                                                    color: #ffffff;
                                                    font-size:10pt;
                                                    font-weight:bold;
                                                    text-align: center;
                                                }

                                QProgressBar::chunk {
                                                        background-color: qlineargradient(
                                                                                            x1: 0,y1: 0,
                                                                                            x2: 1, y2: 0,
                                                                                            stop: 0.0 #FF0000,
                                                                                            stop: 0.2 #FF7F00,
                                                                                            stop: 0.4 #FFFF00,
                                                                                            stop: 0.6 #00FF00,
                                                                                            stop: 0.8 #0000FF,
                                                                                            stop: 1.0 #8B00FF
                                                                                        );
                                                                                        border-radius: 10px;
                                                                                    }
                                """

        cls.ScrollBarStyle = f"""
                                QScrollBar:vertical
                                                    {{
                                                        background: transparent;
                                                        width: 14px;
                                                        margin: 4px;
                                                    }}

                                QScrollBar::handle:vertical
                                                                {{
                                                                    background: {Palette['ScrollHandle']};
                                                                    border-radius: 7px;
                                                                    min-height: 40px;
                                                                }}

                                QScrollBar::handle:vertical:hover
                                                                    {{
                                                                        background: rgba(0,220,255,120);
                                                                    }}

                                QScrollBar::handle:vertical:pressed
                                                                    {{
                                                                        background: rgba(0,255,255,200);
                                                                    }}

                                QScrollBar::add-line:vertical
                                                                {{
                                                                    height: 0px;
                                                                }}

                                QScrollBar::sub-line:vertical
                                                                {{
                                                                    height: 0px;
                                                                }}

                                QScrollBar::add-page:vertical
                                                                {{
                                                                    background: transparent;
                                                                }}

                                QScrollBar::sub-page:vertical
                                                                {{
                                                                    background: transparent;
                                                                }}

                                QScrollBar:horizontal
                                                        {{
                                                            background: transparent;
                                                            height: 14px;
                                                            margin: 4px;
                                                        }}

                                QScrollBar::handle:horizontal
                                                                {{
                                                                    background: {Palette['ScrollHandle']};
                                                                    border-radius: 7px;
                                                                    min-width: 40px;
                                                                }}

                                QScrollBar::handle:horizontal:hover
                                                                    {{
                                                                        background: rgba(0,220,255,120);
                                                                    }}

                                QScrollBar::handle:horizontal:pressed
                                                                        {{
                                                                            background: rgba(0,255,255,200);
                                                                        }}

                                QScrollBar::add-line:horizontal
                                                                {{
                                                                    width: 0px;
                                                                }}

                                QScrollBar::sub-line:horizontal
                                                                {{
                                                                    width: 0px;
                                                                }}

                                QScrollBar::add-page:horizontal
                                                                {{
                                                                    background: transparent;
                                                                }}

                                QScrollBar::sub-page:horizontal
                                                                {{
                                                                    background: transparent;
                                                                }}
                                """

        cls.AssetCardStyle = f"""
                                QFrame
                                        {{
                                            background: {Palette['AssetCardBg']};
                                            border: 1px solid {Palette['AssetCardBorder']};
                                            border-radius: 18px;
                                            margin: 2px;
                                        }}

                                QFrame:hover
                                            {{
                                                background: rgba(0,170,255,18);
                                                border: 3px solid rgba(0,220,255,120);
                                            }}

                        """

        cls.AddAssetButtonStyle = f"""
                                    QPushButton
                                                {{
                                                    background: rgba(0,170,255,{AccentAlpha});
                                                    color: rgb(255,255,255);
                                                    border: none;
                                                    border-radius: 22px;
                                                    font-size: 12pt;
                                                    font-weight: 900;
                                                    padding-left: 20px;
                                                    padding-right: 20px;
                                                }}

                                    QPushButton:hover
                                                        {{
                                                            background: rgba(0,170,255,{AccentHoverAlpha});
                                                            color: rgb(255,255,255);
                                                            border:2px solid rgba(0,170,255,255);
                                                        }}

                                    QPushButton:pressed
                                                        {{
                                                            background: rgba(0,170,255,{AccentPressedAlpha});
                                                        }}
                                    """

        cls.CommandTextStyle = """
                                QTextEdit
                                            {
                                                background: rgba(10,10,10,180);
                                                color: rgb(0,255,150);
                                                border: 1px solid rgba(0,255,150,80);
                                                border-radius: 15px;
                                                padding: 15px;
                                                font-family: Consolas;
                                                font-size: 11pt;
                                                font-weight: bold;
                                            }
                            """

        cls.CopyButtonStyle = """
                                QPushButton
                                            {
                                                background: none;
                                                border:none;
                                                border-radius:22px;
                                            }

                                QPushButton:hover
                                                    {
                                                        background: rgba(0,170,255,40);
                                                        border:2px solid rgba(0,170,255,180);;
                                                    }

                                QPushButton:pressed
                                                    {
                                                        background: rgba(0,170,255,80);
                                                    }
                            """

        cls.AppNameLabelStyle = f"""
                                QLabel
                                        {{
                                            color:{Palette['Text']};
                                            font-size:14pt;
                                            font-weight:900;
                                        }}
                            """

        cls.MenuButtonStyle = """
                                    QPushButton
                                                {
                                                    border:none;
                                                    border-radius:23px;
                                                }

                                QPushButton:hover
                                                    {
                                                        background: rgba(0,170,255,35);
                                                        border:2px solid rgba(0,220,255,180);
                                                    }

                                QPushButton:pressed
                                                    {
                                                            background: rgba(0,170,255,70);
                                                    }
                            """

        cls.EdiButtonStyle = f"""
                                    QPushButton
                                                {{
                                                    background:none;
                                                    color:none;
                                                    border: none;
                                                    border-radius: 20px;
                                                    padding: 12px 24px;
                                                    font-size: 11pt;
                                                    font-weight: 800;
                                                }}

                                    QPushButton:hover
                                                        {{
                                                            background: {Palette['SecondaryHoverBg']};
                                                            border: 2px solid rgba(0,220,255,180);
                                                            color: {Palette['Text']};
                                                        }}

                                    QPushButton:pressed
                                                            {{
                                                                background: {Palette['SecondaryPressedBg']};
                                                                border: 2px solid rgba(0,255,255,255);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }}

                                    QPushButton:disabled
                                                            {{
                                                                background: {Palette['SecondaryDisabledBg']};
                                                                color: {Palette['SecondaryDisabledText']};
                                                                border: 2px solid {Palette['SecondaryDisabledBorder']};
                                                            }}
                            """

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
