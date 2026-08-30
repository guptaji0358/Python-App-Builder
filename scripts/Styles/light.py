# A clean, bright, fully opaque light theme with its own accent color
# (a muted "office blue" rather than the neon cyan-blue reused at high
# opacity - that read as harsh/plasticky on a white background).
# Every stylesheet below is authored independently of Developer/Dark -
# tuning those themes must never change a single pixel here.

from ..assets_path import AssetsPath

PALETTE = {
    "WindowBg": "rgba(245,247,250,255)",
    "Text": "#111318",
    "SubText": "rgba(17,19,24,160)",
    "CardBg": "rgba(0,0,0,6)",
    "CardBorder": "rgba(0,0,0,25)",
    "DialogBg": "rgba(255,255,255,250)",
}


def Build():
    Result = {
        "WindowOpacity": 1.0,

        "MainWindowStyle": """
                                QWidget
                                        {
                                            background: rgba(245,247,250,255);
                                            color:#111318;
                                        }
                        """,

        "InputStyle": """
                            QLineEdit
                                        {
                                            background-color: rgba(43,92,138,16);
                                            color: #111318;
                                            border: 1px solid rgba(43,92,138,60);
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(43,92,138,180);
                                            selection-color: white;
                                        }

                            QLineEdit:hover
                                            {
                                                background-color: rgba(43,92,138,22);
                                                border: 1px solid rgba(43,92,138,140);
                                            }

                            QLineEdit:focus
                                            {
                                                background-color: rgba(43,92,138,30);
                                                border: 2px solid rgb(43,92,138);
                                                color: #111318;
                                            }

                            QLineEdit:disabled
                                                {
                                                    background-color: rgba(0,0,0,15);
                                                    color: rgba(17,19,24,120);
                                                    border: 1px solid rgba(0,0,0,25);
                                                }
                            """,

        "ComboBoxStyle": """
                                QComboBox
                                            {
                                                background-color: rgba(255,255,255,235);
                                                color:#111318;
                                                border:1px solid rgba(0,0,0,30);
                                                border-radius:12px;
                                                padding:10px;
                                            }

                                QComboBox:hover
                                                {
                                                    border:1px solid rgb(43,92,138);
                                                }

                                QComboBox QAbstractItemView
                                                            {
                                                                background-color: rgba(255,255,255,250);
                                                                color: #111318;
                                                                border: 1px solid rgba(0,0,0,30);
                                                                outline: none;
                                                                selection-background-color: rgba(43,92,138,50);
                                                                selection-color: #111318;
                                                            }
                        """,

        "CardStyle": """
                        QFrame
                                {
                                    background: rgba(0,0,0,5);
                                    border:none;
                                    border-radius:18px;
                                }
                    """,

        "ButtonStyle": """
                            QPushButton
                                        {
                                            background: rgb(43,92,138);
                                            border:none;
                                            border-radius:20px;
                                            color:white;
                                            padding:12px;
                                            font-size:11pt;
                                            font-weight:700;
                                        }

                            QPushButton:hover
                                                {
                                                    background: rgb(54,105,153);
                                                    border:3px solid rgba(43,92,138,120);
                                                }

                            QPushButton:pressed
                                                {
                                                    background: rgb(33,74,112);
                                                }
                    """,

        "SecondaryButtonStyle": """
                                    QPushButton
                                                {
                                                    background: rgba(0,0,0,7);
                                                    color: #111318;
                                                    border: 1px solid rgba(0,0,0,20);
                                                    border-radius: 20px;
                                                    padding: 12px 24px;
                                                    font-size: 11pt;
                                                    font-weight: 800;
                                                }

                                    QPushButton:hover
                                                        {
                                                            background: rgba(0,0,0,12);
                                                            border: 2px solid rgba(43,92,138,140);
                                                            color: #111318;
                                                        }

                                    QPushButton:pressed
                                                            {
                                                                background: rgba(0,0,0,18);
                                                                border: 2px solid rgb(43,92,138);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }

                                    QPushButton:disabled
                                                            {
                                                                background: rgba(0,0,0,4);
                                                                color: rgba(17,19,24,90);
                                                                border: 1px solid rgba(0,0,0,15);
                                                            }
                            """,

        "LabelStyle": """
                            QLabel
                                    {
                                        color:#111318;
                                        font-size:11pt;
                                        font-weight:bold;
                                    }
                    """,

        "RemoveAssetButtonStyle": """
                                        QPushButton
                                                    {
                                                        background: rgba(220,50,50,14);
                                                        border:1px solid rgba(220,50,50,60);
                                                        border-radius: 18px;
                                                        min-width: 36px;
                                                        max-width: 36px;
                                                        min-height: 36px;
                                                        max-height: 36px;
                                                        padding: 4px;
                                                    }

                                        QPushButton:hover
                                                            {
                                                                background: rgba(220,50,50,28);
                                                                border: 2px solid rgba(200,40,40,160);
                                                            }

                                        QPushButton:pressed
                                                            {
                                                                background: rgba(200,40,40,45);
                                                                border:1px solid rgba(180,30,30,180);
                                                            }
                                """,

        "InvalidInputStyle": """
                            QLineEdit
                                        {
                                            background-color: rgba(210,50,50,12);
                                            color: #111318;
                                            border: 1px solid rgba(210,50,50,160);
                                            border-radius: 20px;
                                            padding-left: 18px;
                                            padding-right: 18px;
                                            padding-top: 10px;
                                            padding-bottom: 10px;
                                            font-size: 11pt;
                                            font-weight: 700;
                                            selection-background-color: rgba(43,92,138,180);
                                            selection-color: white;
                                        }

                            QLineEdit:hover
                                            {
                                                background-color: rgba(210,50,50,18);
                                                border: 1px solid rgba(200,40,40,200);
                                            }

                            QLineEdit:focus
                                            {
                                                background-color: rgba(210,50,50,24);
                                                border: 2px solid rgb(200,40,40);
                                                color: #111318;
                                            }

                            QLineEdit:disabled
                                                {
                                                    background-color: rgba(0,0,0,15);
                                                    color: rgba(17,19,24,120);
                                                    border: 1px solid rgba(0,0,0,25);
                                                }
                            """,

        "CheckBoxStyle": f"""
                                QCheckBox
                                            {{
                                                color: #111318;
                                                font-size: 11pt;
                                                font-weight: 700;
                                                padding-left: 12px;
                                            }}

                                QCheckBox::indicator
                                                        {{
                                                            width: 28px;
                                                            height: 28px;
                                                            border-radius: 10px;
                                                            background:white;
                                                            border: 1px solid rgba(0,0,0,45);
                                                        }}

                                QCheckBox::indicator:hover
                                                            {{
                                                                background: rgba(43,92,138,20);
                                                                border: 1px solid rgb(43,92,138);
                                                            }}

                                QCheckBox::indicator:pressed
                                                                {{
                                                                    background:white;
                                                                    border:1px solid rgba(0,0,0,45);
                                                                }}

                                QCheckBox::indicator:checked
                                                                {{
                                                                    background: rgb(43,92,138);
                                                                    image: url({AssetsPath.Checked});
                                                                    border: 1px solid rgb(43,92,138);
                                                                }}

                                QCheckBox::indicator:checked:hover
                                                                    {{
                                                                        background: rgb(54,105,153);
                                                                        border: 1px solid rgb(54,105,153);
                                                                    }}
                        """,

        "RadioButtonStyle": f"""
                                QRadioButton
                                            {{
                                                color: #111318;
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
                                                                        image: url({AssetsPath.UncheckedOnLight});
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
                                                        background:#E3E6EB;
                                                        width:12px;
                                                        border-radius:6px;
                                                    }

                                QScrollBar::handle:vertical
                                                            {
                                                                background:#0067C0;
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
                                            background: rgba(255,255,255,250);
                                            border: 2px solid rgba(43,92,138,90);
                                            border-radius: 24px;
                                        }

                                QLabel
                                        {
                                            color: #111318;
                                            font-size: 11pt;
                                            font-weight: 700;
                                        }

                                QTextEdit
                                            {
                                                background: rgba(0,0,0,10);
                                                color: #111318;
                                                border: 1px solid rgba(43,92,138,70);
                                                border-radius: 16px;
                                                padding: 12px;
                                            }

                                QTabWidget::pane
                                                {
                                                    background: rgba(0,0,0,4);
                                                    border: 1px solid rgba(0,0,0,20);
                                                    border-radius: 14px;
                                                    top: -1px;
                                                }

                                QTabBar::tab
                                                {
                                                    background: rgba(0,0,0,5);
                                                    color: rgba(17,19,24,170);
                                                    border: 1px solid rgba(0,0,0,20);
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
                                                        background: rgba(43,92,138,14);
                                                        color: #111318;
                                                    }

                                QTabBar::tab:selected
                                                        {
                                                            background: white;
                                                            color: rgb(33,74,112);
                                                            border: 1px solid rgba(0,0,0,20);
                                                            border-bottom: 3px solid rgb(43,92,138);
                                                        }
                        """,

        "ProgressBarStyle": """
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
                                                                    background: rgba(0,0,0,35);
                                                                    border-radius: 7px;
                                                                    min-height: 40px;
                                                                }

                                QScrollBar::handle:vertical:hover
                                                                    {
                                                                        background: rgba(43,92,138,140);
                                                                    }

                                QScrollBar::handle:vertical:pressed
                                                                    {
                                                                        background: rgb(43,92,138);
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
                                                                    background: rgba(0,0,0,35);
                                                                    border-radius: 7px;
                                                                    min-width: 40px;
                                                                }

                                QScrollBar::handle:horizontal:hover
                                                                    {
                                                                        background: rgba(43,92,138,140);
                                                                    }

                                QScrollBar::handle:horizontal:pressed
                                                                        {
                                                                            background: rgb(43,92,138);
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
                                            background: rgba(0,0,0,5);
                                            border: 1px solid rgba(0,0,0,25);
                                            border-radius: 18px;
                                            margin: 2px;
                                        }

                                QFrame:hover
                                            {
                                                background: rgba(43,92,138,10);
                                                border: 3px solid rgba(43,92,138,120);
                                            }

                        """,

        "AddAssetButtonStyle": """
                                    QPushButton
                                                {
                                                    background: rgb(43,92,138);
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
                                                            background: rgb(54,105,153);
                                                            color: rgb(255,255,255);
                                                            border:2px solid rgba(43,92,138,140);
                                                        }

                                    QPushButton:pressed
                                                        {
                                                            background: rgb(33,74,112);
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
                                                        background: rgba(43,92,138,18);
                                                        border:2px solid rgba(43,92,138,120);
                                                    }

                                QPushButton:pressed
                                                    {
                                                        background: rgba(43,92,138,35);
                                                    }
                            """,

        "AppNameLabelStyle": """
                                QLabel
                                        {
                                            color:#111318;
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
                                                        background: rgba(43,92,138,16);
                                                        border:2px solid rgba(43,92,138,100);
                                                    }

                                QPushButton:pressed
                                                    {
                                                            background: rgba(43,92,138,30);
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
                                                            background: rgba(0,0,0,12);
                                                            border: 2px solid rgba(43,92,138,140);
                                                            color: #111318;
                                                        }

                                    QPushButton:pressed
                                                            {
                                                                background: rgba(0,0,0,18);
                                                                border: 2px solid rgb(43,92,138);
                                                                padding-top: 13px;
                                                                padding-bottom: 11px;
                                                            }

                                    QPushButton:disabled
                                                            {
                                                                background: rgba(0,0,0,4);
                                                                color: rgba(17,19,24,90);
                                                                border: 1px solid rgba(0,0,0,15);
                                                            }
                            """,

        "ToggleButtonStyle": """
                                    QPushButton
                                                {
                                                    background: rgba(0,0,0,6);
                                                    color: rgba(17,19,24,170);
                                                    border: none;
                                                    border-radius: 14px;
                                                    padding: 8px 18px;
                                                    font-size: 10pt;
                                                    font-weight: 700;
                                                }

                                    QPushButton:hover
                                                        {
                                                            background: rgba(43,92,138,16);
                                                            color: #111318;
                                                        }

                                    QPushButton:checked
                                                        {
                                                            background: rgb(43,92,138);
                                                            color: white;
                                                        }
                            """,
    }
    Result["NormalInputStyle"] = Result["InputStyle"]
    return Result
