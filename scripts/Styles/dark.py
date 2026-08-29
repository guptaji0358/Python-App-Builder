# A fresh, opaque slate-navy dark theme - distinct from "Developer".
# Every stylesheet below is authored independently of Developer/Light -
# tuning those themes must never change a single pixel here.

from ..assets_path import AssetsPath

PALETTE = {
    "WindowBg": "rgba(15,18,26,235)",
    "Text": "#EAF0FF",
    "SubText": "rgba(234,240,255,170)",
    "CardBg": "rgba(255,255,255,10)",
    "CardBorder": "rgba(120,170,255,45)",
    "DialogBg": "rgba(12,16,26,250)",
}


def Build():
    return {
        "WindowOpacity": 1.0,

        "MainWindowStyle": """
                                QWidget
                                        {
                                            background: rgba(15,18,26,235);
                                            color:#EAF0FF;
                                        }
                        """,

        "InputStyle": """
                            QLineEdit
                                        {
                                            background-color: rgba(80,120,255,35);
                                            color: #EAF0FF;
                                            border:none;
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(80,120,255,180);
                                            selection-color: white;
                                        }

                            QLineEdit:hover
                                            {
                                                background-color: rgba(80,120,255,35);
                                                border: 3px solid rgba(80,120,255,180);
                                            }

                            QLineEdit:focus
                                            {
                                                background-color: rgba(80,120,255,70);
                                                border: 2px solid rgba(100,150,255,255);
                                                color: #EAF0FF;
                                            }

                            QLineEdit:disabled
                                                {
                                                    background-color: rgba(90,90,100,40);
                                                    color: rgba(234,240,255,110);
                                                    border: 1px solid rgba(234,240,255,25);
                                                }
                            """,

        "ComboBoxStyle": """
                                QComboBox
                                            {
                                                background-color: rgba(24,30,46,200);
                                                color:#EAF0FF;
                                                border:1px solid rgba(120,170,255,40);
                                                border-radius:12px;
                                                padding:10px;
                                            }

                                QComboBox:hover
                                                {
                                                    border:1px solid rgb(100,150,255);
                                                }

                                QComboBox QAbstractItemView
                                                            {
                                                                background-color: rgba(12,16,26,250);
                                                                color: #EAF0FF;
                                                                border: 1px solid rgba(120,170,255,40);
                                                                outline: none;
                                                                selection-background-color: rgba(80,120,255,140);
                                                                selection-color: white;
                                                            }
                        """,

        "CardStyle": """
                        QFrame
                                {
                                    background: rgba(255,255,255,10);
                                    border:1px solid rgba(120,170,255,45);
                                    border-radius:18px;
                                }
                    """,

        "ButtonStyle": """
                            QPushButton
                                        {
                                            background: rgba(80,120,255,45);
                                            border:none;
                                            border-radius:20px;
                                            color:white;
                                            padding:12px;
                                            font-size:11pt;
                                            font-weight:700;
                                        }

                            QPushButton:hover
                                                {
                                                    background: rgba(80,120,255,60);
                                                    border:3px solid rgba(100,150,255,255);
                                                }

                            QPushButton:pressed
                                                {
                                                    background: rgba(80,120,255,90);
                                                }
                    """,

        "SecondaryButtonStyle": """
                                    QPushButton
                                                {
                                                    background: rgba(255,255,255,14);
                                                    color: #EAF0FF;
                                                    border: none;
                                                    border-radius: 20px;
                                                    padding: 12px 24px;
                                                    font-size: 11pt;
                                                    font-weight: 800;
                                                }

                                    QPushButton:hover
                                                        {
                                                            background: rgba(255,255,255,22);
                                                            border: 2px solid rgba(100,150,255,180);
                                                            color: white;
                                                        }

                                    QPushButton:pressed
                                                            {
                                                                background: rgba(255,255,255,34);
                                                                border: 2px solid rgba(120,170,255,255);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }

                                    QPushButton:disabled
                                                            {
                                                                background: rgba(255,255,255,6);
                                                                color: rgba(234,240,255,85);
                                                                border: 2px solid rgba(234,240,255,18);
                                                            }
                            """,

        "LabelStyle": """
                            QLabel
                                    {
                                        color:#EAF0FF;
                                        font-size:11pt;
                                        font-weight:bold;
                                    }
                    """,

        "RemoveAssetButtonStyle": """
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
                                """,

        "InvalidInputStyle": """
                            QLineEdit
                                        {
                                            background-color: rgba(255,120,120,18);
                                            color: #EAF0FF;
                                            border: 1px solid rgba(255,120,120,180);
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(80,120,255,180);
                                            selection-color: white;
                                        }

                            QLineEdit:hover
                                            {
                                                background-color: rgba(255,120,120,25);
                                                border: 1px solid rgba(255,150,150,220);
                                            }

                            QLineEdit:focus
                                            {
                                                background-color: rgba(255,120,120,35);
                                                border: 2px solid rgba(255,150,150,255);
                                                color: #EAF0FF;
                                            }

                            QLineEdit:disabled
                                                {
                                                    background-color: rgba(90,90,100,40);
                                                    color: rgba(234,240,255,110);
                                                    border: 1px solid rgba(234,240,255,25);
                                                }
                            """,

        "CheckBoxStyle": f"""
                                QCheckBox
                                            {{
                                                color: #EAF0FF;
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
                                                            border: 1px solid rgba(120,170,255,60);
                                                        }}

                                QCheckBox::indicator:hover
                                                            {{
                                                                background: rgba(80,120,255,45);
                                                                border: none;
                                                            }}

                                QCheckBox::indicator:pressed
                                                                {{
                                                                    background:none;
                                                                    border:none;
                                                                }}

                                QCheckBox::indicator:checked
                                                                {{
                                                                    image: url({AssetsPath.Checked});
                                                                    border: none;
                                                                }}

                                QCheckBox::indicator:checked:hover
                                                                    {{
                                                                        background: rgba(80,120,255,45);
                                                                        border:none;
                                                                    }}
                        """,

        "RadioButtonStyle": f"""
                                QRadioButton
                                            {{
                                                color: #EAF0FF;
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
                                                                        image: url({AssetsPath.Unchecked});
                                                                    }}

                                QRadioButton::indicator:checked
                                                                {{
                                                                    image: url({AssetsPath.RadioChecked});
                                                                }}
                            """,

        "ScrollAreaStyle": """
                                QScrollArea
                                            {
                                                border:none;
                                                background:transparent;
                                            }

                                QScrollBar:vertical
                                                    {
                                                        background:#161B26;
                                                        width:12px;
                                                        border-radius:6px;
                                                    }

                                QScrollBar::handle:vertical
                                                            {
                                                                background:#4A90E2;
                                                                border-radius:6px;
                                                            }

                                QScrollBar::add-line:vertical,
                                QScrollBar::sub-line:vertical
                                                                {
                                                                    height:0px;
                                                                }
                                """,

        "DialogStyle": """
                                QDialog
                                        {
                                            background: rgba(12,16,26,250);
                                            border: 2px solid rgba(80,120,255,140);
                                            border-radius: 24px;
                                        }

                                QLabel
                                        {
                                            color: #EAF0FF;
                                            font-size: 11pt;
                                            font-weight: 700;
                                        }

                                QTextEdit
                                            {
                                                background: rgba(6,8,14,150);
                                                color: #EAF0FF;
                                                border: 1px solid rgba(80,120,255,100);
                                                border-radius: 16px;
                                                padding: 12px;
                                            }

                                QTabWidget::pane
                                                {
                                                    background: rgba(255,255,255,10);
                                                    border: 1px solid rgba(120,170,255,45);
                                                    border-radius: 14px;
                                                    top: -1px;
                                                }

                                QTabBar::tab
                                                {
                                                    background: rgba(255,255,255,14);
                                                    color: #EAF0FF;
                                                    border: 1px solid rgba(120,170,255,45);
                                                    border-bottom: none;
                                                    border-top-left-radius: 10px;
                                                    border-top-right-radius: 10px;
                                                    padding: 8px 16px;
                                                    margin-right: 2px;
                                                    font-size: 10pt;
                                                    font-weight: 700;
                                                }

                                QTabBar::tab:hover
                                                    {
                                                        background: rgba(80,120,255,45);
                                                    }

                                QTabBar::tab:selected
                                                        {
                                                            background: rgba(80,120,255,85);
                                                            border: 1px solid rgba(100,150,255,200);
                                                        }
                        """,

        "ProgressBarStyle": """
                                QProgressBar
                                                {
                                                    background: rgba(255,255,255,12);
                                                    border: 1px solid rgba(120,170,255,60);
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
                                """,

        "ScrollBarStyle": """
                                QScrollBar:vertical
                                                    {
                                                        background: transparent;
                                                        width: 14px;
                                                        margin: 4px;
                                                    }

                                QScrollBar::handle:vertical
                                                                {
                                                                    background: rgba(120,170,255,45);
                                                                    border-radius: 7px;
                                                                    min-height: 40px;
                                                                }

                                QScrollBar::handle:vertical:hover
                                                                    {
                                                                        background: rgba(100,150,255,140);
                                                                    }

                                QScrollBar::handle:vertical:pressed
                                                                    {
                                                                        background: rgba(100,150,255,220);
                                                                    }

                                QScrollBar::add-line:vertical
                                                                {
                                                                    height: 0px;
                                                                }

                                QScrollBar::sub-line:vertical
                                                                {
                                                                    height: 0px;
                                                                }

                                QScrollBar::add-page:vertical
                                                                {
                                                                    background: transparent;
                                                                }

                                QScrollBar::sub-page:vertical
                                                                {
                                                                    background: transparent;
                                                                }

                                QScrollBar:horizontal
                                                        {
                                                            background: transparent;
                                                            height: 14px;
                                                            margin: 4px;
                                                        }

                                QScrollBar::handle:horizontal
                                                                {
                                                                    background: rgba(120,170,255,45);
                                                                    border-radius: 7px;
                                                                    min-width: 40px;
                                                                }

                                QScrollBar::handle:horizontal:hover
                                                                    {
                                                                        background: rgba(100,150,255,140);
                                                                    }

                                QScrollBar::handle:horizontal:pressed
                                                                        {
                                                                            background: rgba(100,150,255,220);
                                                                        }

                                QScrollBar::add-line:horizontal
                                                                {
                                                                    width: 0px;
                                                                }

                                QScrollBar::sub-line:horizontal
                                                                {
                                                                    width: 0px;
                                                                }

                                QScrollBar::add-page:horizontal
                                                                {
                                                                    background: transparent;
                                                                }

                                QScrollBar::sub-page:horizontal
                                                                {
                                                                    background: transparent;
                                                                }
                                """,

        "AssetCardStyle": """
                                QFrame
                                        {
                                            background: rgba(255,255,255,8);
                                            border: 1px solid rgba(120,170,255,45);
                                            border-radius: 18px;
                                            margin: 2px;
                                        }

                                QFrame:hover
                                            {
                                                background: rgba(80,120,255,20);
                                                border: 3px solid rgba(100,150,255,140);
                                            }

                        """,

        "AddAssetButtonStyle": """
                                    QPushButton
                                                {
                                                    background: rgba(80,120,255,30);
                                                    color: rgb(255,255,255);
                                                    border: none;
                                                    border-radius: 22px;
                                                    font-size: 12pt;
                                                    font-weight: 900;
                                                    padding-left: 20px;
                                                    padding-right: 20px;
                                                }

                                    QPushButton:hover
                                                        {
                                                            background: rgba(80,120,255,55);
                                                            color: rgb(255,255,255);
                                                            border:2px solid rgba(100,150,255,255);
                                                        }

                                    QPushButton:pressed
                                                        {
                                                            background: rgba(80,120,255,90);
                                                        }
                                    """,

        "CommandTextStyle": """
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
                            """,

        "CopyButtonStyle": """
                                QPushButton
                                            {
                                                background: none;
                                                border:none;
                                                border-radius:22px;
                                            }

                                QPushButton:hover
                                                    {
                                                        background: rgba(80,120,255,45);
                                                        border:2px solid rgba(100,150,255,180);
                                                    }

                                QPushButton:pressed
                                                    {
                                                        background: rgba(80,120,255,90);
                                                    }
                            """,

        "AppNameLabelStyle": """
                                QLabel
                                        {
                                            color:#EAF0FF;
                                            font-size:14pt;
                                            font-weight:900;
                                        }
                            """,

        "MenuButtonStyle": """
                                    QPushButton
                                                {
                                                    border:none;
                                                    border-radius:23px;
                                                }

                                QPushButton:hover
                                                    {
                                                        background: rgba(80,120,255,40);
                                                        border:2px solid rgba(100,150,255,180);
                                                    }

                                QPushButton:pressed
                                                    {
                                                            background: rgba(80,120,255,75);
                                                    }
                            """,

        "EdiButtonStyle": """
                                    QPushButton
                                                {
                                                    background:none;
                                                    color:none;
                                                    border: none;
                                                    border-radius: 20px;
                                                    padding: 12px 24px;
                                                    font-size: 11pt;
                                                    font-weight: 800;
                                                }

                                    QPushButton:hover
                                                        {
                                                            background: rgba(255,255,255,22);
                                                            border: 2px solid rgba(100,150,255,180);
                                                            color: white;
                                                        }

                                    QPushButton:pressed
                                                            {
                                                                background: rgba(255,255,255,34);
                                                                border: 2px solid rgba(120,170,255,255);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }

                                    QPushButton:disabled
                                                            {
                                                                background: rgba(255,255,255,6);
                                                                color: rgba(234,240,255,85);
                                                                border: 2px solid rgba(234,240,255,18);
                                                            }
                            """,
    }
