from .assets_path import AssetsPath

class Style:
    MainWindowStyle = """
                            QWidget
                                    {
                                        background: rgba(20,20,20,55);
                                        color:white;
                                    }
                    """
    
    InputStyle = """
                        QLineEdit
                                    {
                                        background-color: rgba(0,170,255,40);
                                        color: rgb(255,255,255);
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
                                    }

                        QLineEdit:hover
                                        {
                                            background-color: rgba(0,170,255,40);
                                            border: 3px solid rgba(0,170,255,180);
                                        }

                        QLineEdit:focus
                                        {
                                            background-color: rgba(0,170,255,80);
                                            border: 2px solid rgba(0,220,255,255);
                                            color: white;
                                        }

                        QLineEdit:disabled
                                            {
                                                background-color: rgba(100,100,100,40);
                                                color: rgba(255,255,255,120);
                                                border: 1px solid rgba(255,255,255,30);
                                            }
                        """

    ComboBoxStyle = """
                            QComboBox
                                        {
                                            background-color: rgba(30,41,59,180);
                                            color:white;
                                            border:1px solid rgba(255,255,255,40);
                                            border-radius:12px;
                                            padding:10px;
                                        }

                            QComboBox:hover
                                            {
                                                border:1px solid rgb(59,130,246);
                                            }
                    """
    
    CardStyle = """
                    QFrame
                            {
                                background: rgba(255,255,255,15);
                                border:1px solid rgba(255,255,255,40);
                                border-radius:18px;
                            }
                """

    ButtonStyle = """
                        QPushButton
                                    {
                                        background: rgba(0,170,255,40);
                                        border:none;
                                        border-radius:20px;
                                        color:white;
                                        padding:12px;
                                        font-size:11pt;
                                        font-weight:700;
                                    }

                        QPushButton:hover
                                            {
                                                background: rgba(0,170,255,40);
                                                border:3px solid rgba(0,170,255,255);
                                            }

                        QPushButton:pressed
                                            {
                                                background: rgba(0,170,255,80);
                                            }
                """

    SecondaryButtonStyle = """
                                QPushButton
                                            {
                                                background: rgba(255,255,255,18);
                                                color: rgb(255,255,255);
                                                border: none;
                                                border-radius: 20px;
                                                padding: 12px 24px;
                                                font-size: 11pt;
                                                font-weight: 800;
                                            }

                                QPushButton:hover
                                                    {
                                                        background: rgba(255,255,255,28);
                                                        border: 2px solid rgba(0,220,255,180);
                                                        color: white;
                                                    }

                                QPushButton:pressed
                                                        {
                                                            background: rgba(255,255,255,40);
                                                            border: 2px solid rgba(0,255,255,255);
                                                            padding-top: 13px;
                                                            padding-bottom: 11px;
                                                        }

                                QPushButton:disabled
                                                        {
                                                            background: rgba(255,255,255,8);
                                                            color: rgba(255,255,255,90);
                                                            border: 2px solid rgba(255,255,255,20);
                                                        }
                        """
    
    LabelStyle = """
                        QLabel
                                {
                                    color:white;
                                    font-size:11pt;
                                    font-weight:bold;
                                }
                """
    
    RemoveAssetButtonStyle = """
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

    InvalidInputStyle = """
                        QLineEdit
                                    {
                                        background-color: rgba(255,120,120,18);
                                        color: rgb(255,255,255);
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
                                            color: white;
                                        }

                        QLineEdit:disabled
                                            {
                                                background-color: rgba(100,100,100,40);
                                                color: rgba(255,255,255,120);
                                                border: 1px solid rgba(255,255,255,30);
                                            }
                        """

    NormalInputStyle = InputStyle

    CheckBoxStyle = f"""
                            QCheckBox 
                                        {{
                                            color: white;
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
                                                        border: 1px solid rgba(255,255,255,70);
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
                                                                image: url({AssetsPath.Checked});
                                                                border: none;
                                                            }}

                            QCheckBox::indicator:checked:hover 
                                                                {{
                                                                    background: rgba(255,255,255,40);
                                                                    border:none;
                                                                }}
                    """

    
    RadioButtonStyle = f"""
                            QRadioButton
                                        {{
                                            color: white;
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
                        """

    ScrollAreaStyle = """
                            QScrollArea
                                        {
                                            border:none;
                                            background:transparent;
                                        }

                            QScrollBar:vertical
                                                {
                                                    background:#20242C;
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
                            """
    
    DialogStyle = """
                            QDialog
                                    {
                                        background: rgba(15,20,30,240);
                                        border: 2px solid rgba(0,170,255,120);
                                        border-radius: 24px;
                                    }

                            QLabel
                                    {
                                        color: white;
                                        font-size: 11pt;
                                        font-weight: 700;
                                    }

                            QTextEdit
                                        {
                                            background: rgba(0,0,0,120);
                                            border: 1px solid rgba(0,170,255,100);
                                            border-radius: 16px;
                                            padding: 12px;
                                        }
                    """  
    
    ProgressBarStyle = """
                            QProgressBar
                                            {
                                                background: rgba(255,255,255,12);
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

    
    ScrollBarStyle = """
                            QScrollBar:vertical
                                                {
                                                    background: transparent;
                                                    width: 14px;
                                                    margin: 4px;
                                                }

                            QScrollBar::handle:vertical
                                                        {
                                                            background: rgba(255,255,255,40);
                                                            border-radius: 7px;
                                                            min-height: 40px;
                                                        }

                            QScrollBar::handle:vertical:hover
                                                                {
                                                                    background: rgba(0,220,255,120);
                                                                }

                            QScrollBar::handle:vertical:pressed
                                                                {
                                                                    background: rgba(0,255,255,200);
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
                                                                background: rgba(255,255,255,40);
                                                                border-radius: 7px;
                                                                min-width: 40px;
                                                            }

                            QScrollBar::handle:horizontal:hover
                                                                {
                                                                    background: rgba(0,220,255,120);
                                                                }

                            QScrollBar::handle:horizontal:pressed
                                                                    {
                                                                        background: rgba(0,255,255,200);
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
                            """
    
    AssetCardStyle = """
                            QFrame
                                    {
                                        background: rgba(255,255,255,12);
                                        border: 1px solid rgba(255,255,255,50);
                                        border-radius: 18px;
                                        margin: 2px;
                                    }

                            QFrame:hover
                                        {
                                            background: rgba(0,170,255,18);
                                            border: 3px solid rgba(0,220,255,120);
                                        }
                        
                    """
    
    AddAssetButtonStyle = """
                                QPushButton
                                            {
                                                background: rgba(0,170,255,25);
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
                                                        background: rgba(0,170,255,50);
                                                        color: rgb(255,255,255);
                                                        border:2px solid rgba(0,170,255,255);
                                                    }

                                QPushButton:pressed
                                                    {
                                                        background: rgba(0,170,255,80);
                                                    }
                                """
    
    CommandTextStyle = """
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
    
    CopyButtonStyle = """
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
    
    AppNameLabelStyle = """
                            QLabel
                                    {
                                        color:white;
                                        font-size:14pt;
                                        font-weight:900;
                                    }
                        """
    
    MenuButtonStyle = """
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
    
    EdiButtonStyle = """
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
                                                        background: rgba(255,255,255,28);
                                                        border: 2px solid rgba(0,220,255,180);
                                                        color: white;
                                                    }

                                QPushButton:pressed
                                                        {
                                                            background: rgba(255,255,255,40);
                                                            border: 2px solid rgba(0,255,255,255);
                                                            padding-top: 13px;
                                                            padding-bottom: 11px;
                                                        }

                                QPushButton:disabled
                                                        {
                                                            background: rgba(255,255,255,8);
                                                            color: rgba(255,255,255,90);
                                                            border: 2px solid rgba(255,255,255,20);
                                                        }
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

