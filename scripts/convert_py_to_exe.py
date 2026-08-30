from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtGui import QMovie
import sys
import shutil
import os
import string
import subprocess
import time
from win32com.client import Dispatch
import textwrap

from .threads import FileIndexerThread, IconIndexerThread, BuildThread
from .assets_path import AssetsPath
from .style import Style, PALETTES
from .messages import Messages
from .shortcuts import ShortcutManager, SHORTCUT_LABELS
from .theme import ThemeManager
from .customization import CustomizationManager
from .user_data import UserDataPath, EnsureUserDataDirs
from .build_history import BuildHistory
from .file_index_db import PyFileIndexDatabase, IconFileIndexDatabase
from .post_install import ShowThankYouFireworks

APP_VERSION = "1.0.0.0"
REPOSITORY_URL = "https://github.com/guptaji0358/Python-App-Builder"
VERIFICATION_FILE = UserDataPath("verification.txt")

class ConvertPyToExe():

    def __init__(self):
        super().__init__()
        ConvertPyToExeApp = QApplication(sys.argv)

        EnsureUserDataDirs()
        self.BuildHistory = BuildHistory()

        self.ThemeMode = ThemeManager.Get()
        Style.ApplyTheme(ThemeManager.Resolve(self.ThemeMode))

        self.ShowSplashScreen()

        self.UpdateSplash("Loading settings...")
        self.LoadVerificationSettings()

        if not self.IsRegistrationComplete():
            self.UpdateSplash("Waiting for registration...")
            self.ShowRegistrationDialog()

        self.UpdateSplash(f"Welcome, {self.AuthorName}!" if self.AuthorName else "Welcome!")

        if not ThemeManager.HasSavedChoice():
            self.UpdateSplash("Choose your theme...")
            self.ShowFirstRunThemeDialog()

        self.CustomizationManager = CustomizationManager()
        if self.CustomizationManager.Get("StartMenuPath"):
            AssetsPath.AddStartMenuShortcutPath = self.CustomizationManager.Get("StartMenuPath")

        self.CurrentProgress = 10

        self.PyIndexDB = PyFileIndexDatabase()
        self.IconIndexDB = IconFileIndexDatabase()
        self.FileIndex = self.PyIndexDB.Load()
        self.IconIndex = self.IconIndexDB.Load()

        self.UpdateSplash("Indexing Python files...")

        self.FileIndexer = FileIndexerThread()
        self.FileIndexer.IndexingFinished.connect(self.StoreFileIndex)
        self.FileIndexer.start()

        self.IconIndexer = IconIndexerThread()
        self.IconIndexer.IndexingFinished.connect(self.StoreIconIndex)
        self.IconIndexer.start()

        self.UpdateSplash("Preparing interface...")

        self.SearchTimer = QTimer()
        self.SearchTimer.setSingleShot(True)
        self.SearchTimer.timeout.connect(self.ValidatePythonFile)

        GridLayout = QGridLayout()
        GridLayout.setColumnStretch(0,1)
        GridLayout.setColumnStretch(1,5)
        GridLayout.setColumnStretch(2,2)

        MainVerticalLayout = QVBoxLayout()
        MainVerticalLayout.setSpacing(15)
        MainVerticalLayout.setContentsMargins(15,15,15,15)

        BuildTypeLayout = QHBoxLayout()
        self.BuildTypeGroup = QButtonGroup()

        ConsoleModeLayout = QHBoxLayout()
        self.ConsoleModeGroup = QButtonGroup()

        self.AssetsSectionLayout = QVBoxLayout()
        
        self.DynamicAssetsLayout = QVBoxLayout()
        self.AssetsSectionLayout.setAlignment(Qt.AlignTop)
        self.DynamicAssetsLayout.setSpacing(5)
        self.DynamicAssetsLayout.setContentsMargins(5,5,5,5)

        BuildOptionsLayout = QVBoxLayout()

        CancelAndBuildBottomButtonLayout = QHBoxLayout()
        CancelAndBuildBottomButtonLayout.addStretch()

        BottomSectionLayout = QHBoxLayout()

        PythonFileInputLayout = QHBoxLayout()
        IconFileInputLayout = QHBoxLayout()

        AssetsContainer = QWidget()
        AssetsContainer.setLayout(self.AssetsSectionLayout)
        AssetsContainer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)

        AppNameLayout = QHBoxLayout()

        self.AssetsScrollArea = QScrollArea()
        self.AssetsScrollArea.setStyleSheet(Style.ScrollAreaStyle)
        self.AssetsScrollArea.verticalScrollBar().setStyleSheet(Style.ScrollBarStyle)
        self.AssetsScrollArea.horizontalScrollBar().setStyleSheet(Style.ScrollBarStyle)
        self.AssetsScrollArea.setFrameShape(QFrame.NoFrame)
        self.AssetsScrollArea.setWidget(AssetsContainer)
        self.AssetsScrollArea.setWidgetResizable(True)
        self.AssetsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.MainWindow = QWidget()
        self.MainWindow.setWindowOpacity(Style.WindowOpacity)
        self.MainWindow.setWindowFlags(Qt.Window)
        self.MainWindow.setWindowTitle("Pyxe")
        self.MainWindow.setStyleSheet(Style.MainWindowStyle)
        self.MainWindow.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        self.MainWindow.resize(1250,750)

        #Shortcuts
        self.ShortcutManager = ShortcutManager()
        self.ShortcutActionHandlers = {
                                        "AddAsset": self.AddAsset,
                                        "BrowseMultipleAssets": self.BrowseMultipleAssets,
                                        "RemoveLastAsset": self.RemoveLastAssetRow,
                                        "FocusNextInput": self.FocusNextInput,
                                        "OpenSettings": self.ShowSettingsWindow,
                                        }
        self.ShortcutObjects = {}
        self.ApplyShortcuts()
        
        AppNameLabel = QLabel()
        AppNameLabel.setText("App Name:")
        AppNameLabel.setStyleSheet(Style.LabelStyle)

        self.AppNameInput = QLineEdit()
        self.AppNameInput.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.AppNameInput.setPlaceholderText("Enter App Name")
        self.AppNameInput.setStyleSheet(Style.InputStyle)
        self.AppNameInput.textChanged.connect(lambda:self.AppNameInput.setStyleSheet(Style.NormalInputStyle))

        self.MenuButton = QPushButton()
        self.MenuButton.setFixedSize(46,46)
        self.MenuButton.setCursor(Qt.PointingHandCursor)
        self.MenuButton.setToolTip("Settings")
        self.MenuButton.setIcon(QIcon(AssetsPath.MenuIcon))
        self.MenuButton.setIconSize(QSize(28,28))
        self.MenuButton.setStyleSheet(Style.MenuButtonStyle)
        self.MenuButton.clicked.connect(self.ShowSettingsWindow)

        DescriptionLabel =  QLabel()
        DescriptionLabel.setText("Description")
        DescriptionLabel.setStyleSheet(Style.LabelStyle)

        self.DescriptionInput = QLineEdit()
        self.DescriptionInput.setPlaceholderText("Enter Application Description")
        self.DescriptionInput.setStyleSheet(Style.InputStyle)

        VersionLabel = QLabel()
        VersionLabel.setText("Version:")
        VersionLabel.setStyleSheet(Style.LabelStyle)

        self.VersionInput = QLineEdit()
        self.VersionInput.setPlaceholderText("1.0.0")
        self.VersionInput.setText("1.0.0")
        self.VersionInput.setStyleSheet(Style.InputStyle)

        SelectPyFileLabel = QLabel()
        SelectPyFileLabel.setText("Select Your .py File:")
        SelectPyFileLabel.setStyleSheet(Style.LabelStyle)

        self.SelectPyFileInput = QLineEdit()
        self.SelectPyFileInput.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.SelectPyFileInput.setPlaceholderText("Select Your .py File:")
        self.SelectPyFileInput.textChanged.connect(self.StartValidationTimer)
        self.SelectPyFileInput.setStyleSheet(Style.InputStyle)

        self.SelectFileBrowseButton = QPushButton()
        self.SelectFileBrowseButton.setText("Browse")
        self.SelectFileBrowseButton.setCursor(Qt.PointingHandCursor)
        self.SelectFileBrowseButton.setToolTip("Browse .py Files")
        self.SelectFileBrowseButton.setStyleSheet(Style.ButtonStyle)
        self.SelectFileBrowseButton.clicked.connect(self.BrowsePythonFile)

        self.PythonFileStatusLabel = QLabel()
        self.PythonFileStatusLabel.setText("File Not Found")
        self.PythonFileStatusLabel.setStyleSheet(Style.LabelStyle)
        self.PythonFileStatusLabel.hide()

        self.IconFileStatusLabel = QLabel()
        self.IconFileStatusLabel.setText("File Not Found")
        self.IconFileStatusLabel.setStyleSheet(Style.LabelStyle)
        self.IconFileStatusLabel.hide()

        PythonExtensionLabel = QLabel()
        PythonExtensionLabel.setText(".py")
        PythonExtensionLabel.setStyleSheet(Style.LabelStyle)

        self.IconExtensionLabel = QLabel()
        self.IconExtensionLabel.setText(".ico")
        self.IconExtensionLabel.setStyleSheet(Style.LabelStyle)

        AppTypeLabel = QLabel()
        AppTypeLabel.setText("App Type:")
        AppTypeLabel.setStyleSheet(Style.LabelStyle)

        self.OneFile = QRadioButton()
        self.OneFile.setToolTip("Single file App")
        self.OneFile.setCursor(Qt.PointingHandCursor)
        self.OneFile.setText("One file")
        self.OneFile.setStyleSheet(Style.RadioButtonStyle)

        self.OneDir = QRadioButton()
        self.OneDir.setToolTip("Folder App")
        self.OneDir.setCursor(Qt.PointingHandCursor)
        self.OneDir.setText("One Dir")
        self.OneDir.setStyleSheet(Style.RadioButtonStyle)

        ConsoleModeLabel = QLabel()
        ConsoleModeLabel.setText("Console Mode")
        ConsoleModeLabel.setStyleSheet(Style.LabelStyle)

        self.NoConsole = QRadioButton()
        self.NoConsole.setToolTip("Hide The Console")
        self.NoConsole.setCursor(Qt.PointingHandCursor)
        self.NoConsole.setText("No Console")
        self.NoConsole.setStyleSheet(Style.RadioButtonStyle)

        self.WithConsole = QRadioButton()
        self.WithConsole.setToolTip("Show The Console")
        self.WithConsole.setCursor(Qt.PointingHandCursor)
        self.WithConsole.setText("Console")
        self.WithConsole.setStyleSheet(Style.RadioButtonStyle)

        IconFileLabel = QLabel()
        IconFileLabel.setText("Icon File:")
        IconFileLabel.setStyleSheet(Style.LabelStyle)

        self.IconFileInput = QLineEdit()
        self.IconFileInput.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.IconFileInput.setPlaceholderText("Enter Icon File")
        self.IconFileInput.textChanged.connect(self.ValidateIconFile)
        self.IconFileInput.setStyleSheet(Style.InputStyle)

        self.IconFileBrowseButton = QPushButton()
        self.IconFileBrowseButton.setText("Browse")
        self.IconFileBrowseButton.setCursor(Qt.PointingHandCursor)
        self.IconFileBrowseButton.setToolTip("Browse .ico Files")
        self.IconFileBrowseButton.setStyleSheet(Style.ButtonStyle)
        self.IconFileBrowseButton.clicked.connect(self.BrowseIconFile)

        AssetsLabel = QLabel()
        AssetsLabel.setText("Assets")
        AssetsLabel.setStyleSheet(Style.LabelStyle)

        self.AddAssetButton = QPushButton()
        self.AddAssetButton.setCursor(Qt.PointingHandCursor)
        self.AddAssetButton.setToolTip("Add App Assets")
        self.AddAssetButton.setText("Add Asssets")
        self.AddAssetButton.setFixedWidth(220)
        self.AddAssetButton.setFixedHeight(50)
        self.AddAssetButton.setStyleSheet(Style.AddAssetButtonStyle)
        self.AddAssetButton.clicked.connect(self.AddAsset)

        SaveAppLocationLabel = QLabel()
        SaveAppLocationLabel.setText("Save App Location:")
        SaveAppLocationLabel.setStyleSheet(Style.LabelStyle)
        
        self.SaveAppLocationInput = QLineEdit()
        self.SaveAppLocationInput.setPlaceholderText("Enter / Browse to Save Your App Location")
        self.SaveAppLocationInput.setStyleSheet(Style.InputStyle)

        self.SaveAppLocationBrowseButton = QPushButton()
        self.SaveAppLocationBrowseButton.setText("Browse")
        self.SaveAppLocationBrowseButton.setToolTip("Browse Your Save Location")
        self.SaveAppLocationBrowseButton.setCursor(Qt.PointingHandCursor)
        self.SaveAppLocationBrowseButton.setStyleSheet(Style.ButtonStyle)
        self.SaveAppLocationBrowseButton.clicked.connect(self.SaveAppLocation)
        self.SaveAppLocationInput.textChanged.connect(lambda:self.SaveAppLocationInput.setStyleSheet(Style.NormalInputStyle))

        CancelButton = QPushButton()
        CancelButton.setText("Cancel Build")
        CancelButton.setCursor(Qt.PointingHandCursor)
        CancelButton.setToolTip("Cancel App Build")
        CancelButton.setStyleSheet(Style.SecondaryButtonStyle)
        CancelButton.clicked.connect(self.ResetTheApp)

        BuildButton = QPushButton()
        BuildButton.setText("Build App")
        BuildButton.setFixedHeight(46)
        BuildButton.setFixedWidth(100)
        BuildButton.setCursor(Qt.PointingHandCursor)
        BuildButton.setToolTip("Build App")
        BuildButton.setStyleSheet(Style.ButtonStyle)
        BuildButton.clicked.connect(self.BuildApplication)

        self.ShowPyInstallerCommandCheckbox = QCheckBox()
        self.ShowPyInstallerCommandCheckbox.setText("Show PyInstaller Command")
        self.ShowPyInstallerCommandCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.ShowPyInstallerCommandCheckbox.setCursor(Qt.PointingHandCursor)
        self.ShowPyInstallerCommandCheckbox.setToolTip("Show Py Installer Command")

        self.AsksToHideorShowTerminalCheckbox = QCheckBox()
        self.AsksToHideorShowTerminalCheckbox.setText("Show Terminal")
        self.AsksToHideorShowTerminalCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.AsksToHideorShowTerminalCheckbox.setCursor(Qt.PointingHandCursor)
        self.AsksToHideorShowTerminalCheckbox.setToolTip("Show Terminal Window")

        self.CreateShortcutCheckbox = QCheckBox()
        self.CreateShortcutCheckbox.setText("Create Start Menu Shortcut")
        self.CreateShortcutCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.CreateShortcutCheckbox.setCursor(Qt.PointingHandCursor)
        self.CreateShortcutCheckbox.setToolTip("Create  Short in Start Menu")

        self.CleanFolderCheckbox = QCheckBox()
        self.CleanFolderCheckbox.setText("Clean Folder (Move DLLs into DLLs/)")
        self.CleanFolderCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.CleanFolderCheckbox.setCursor(Qt.PointingHandCursor)
        self.CleanFolderCheckbox.setToolTip("Only Applies to 'One Dir' Builds. Moves all support DLLs / files into a DLLs sub-folder next to the .exe, so the app folder stays clean while remaining standalone.")

        # Seed from Settings > Customize defaults
        (self.OneFile if self.CustomizationManager.Get("DefaultBuildType") == "OneFile" else self.OneDir).setChecked(True)
        (self.NoConsole if self.CustomizationManager.Get("DefaultConsoleMode") == "NoConsole" else self.WithConsole).setChecked(True)
        self.CreateShortcutCheckbox.setChecked(self.CustomizationManager.GetBool("DefaultCreateShortcut"))
        self.ShowPyInstallerCommandCheckbox.setChecked(self.CustomizationManager.GetBool("DefaultShowCommand"))

        #Add Glow
        Style.Shadow(self.MenuButton)

        #Add Assets (s)
        Style.AddButtonGlow

        #Label (s)
        Style.TextGlow(SelectPyFileLabel)
        Style.TextGlow(self.PythonFileStatusLabel)
        Style.TextGlow(self.IconFileStatusLabel)
        Style.TextGlow(PythonExtensionLabel)
        Style.TextGlow(self.IconExtensionLabel)
        Style.TextGlow(AppTypeLabel)
        Style.TextGlow(ConsoleModeLabel)
        Style.TextGlow(IconFileLabel)
        Style.TextGlow(AssetsLabel)
        Style.TextGlow(SaveAppLocationLabel)
        Style.TextGlow(DescriptionLabel)
        Style.TextGlow(VersionLabel)


        #Add Shadow
        #Button(s)
        Style.Shadow(BuildButton)
        Style.Shadow(CancelButton)
        Style.Shadow(self.AddAssetButton)
        Style.Shadow(self.IconFileBrowseButton)
        Style.Shadow(self.SelectFileBrowseButton)
        Style.Shadow(self.SaveAppLocationBrowseButton)
        Style.Shadow(DescriptionLabel)
        Style.Shadow(VersionLabel)

        #Input (s)
        Style.Shadow(self.AppNameInput)
        Style.Shadow(self.IconFileInput)
        Style.Shadow(self.SaveAppLocationInput)
        Style.Shadow(self.SelectPyFileInput)
        Style.Shadow(self.DescriptionInput)
        Style.Shadow(self.VersionInput)

        #Label (s)
        Style.Shadow(AppNameLabel)
        Style.Shadow(SelectPyFileLabel)
        Style.Shadow(AppTypeLabel)
        Style.Shadow(ConsoleModeLabel)
        Style.Shadow(IconFileLabel)
        Style.Shadow(AssetsLabel)
        Style.Shadow(self.IconExtensionLabel)
        Style.Shadow(PythonExtensionLabel)
        Style.Shadow(SaveAppLocationLabel)

        # Radio Buttons (s)
        Style.Shadow(self.OneFile)
        Style.Shadow(self.OneDir)
        Style.Shadow(self.WithConsole)
        Style.Shadow(self.NoConsole)

        #Checkbox (s)
        Style.Shadow(self.ShowPyInstallerCommandCheckbox)
        Style.Shadow(self.AsksToHideorShowTerminalCheckbox)
        Style.Shadow(self.CleanFolderCheckbox)

        #Radio Button Group
        self.BuildTypeGroup.addButton(self.OneFile)
        self.BuildTypeGroup.addButton(self.OneDir)

        self.ConsoleModeGroup.addButton(self.NoConsole)
        self.ConsoleModeGroup.addButton(self.WithConsole)

        # .py Label 
        PythonFileInputLayout.addWidget(self.SelectPyFileInput)
        PythonFileInputLayout.addWidget(PythonExtensionLabel)

        # .ico Label 
        IconFileInputLayout.addWidget(self.IconFileInput)
        IconFileInputLayout.addWidget(self.IconExtensionLabel)

        #Adding Layouts And Widgets
        AppNameLayout.setSpacing(10)
        AppNameLayout.addWidget(self.AppNameInput)
        AppNameLayout.addWidget(self.MenuButton)

        MainVerticalLayout.addLayout(GridLayout)
        MainVerticalLayout.addWidget(self.AssetsScrollArea,1)

        BuildTypeLayout.addWidget(self.OneFile)
        BuildTypeLayout.addWidget(self.OneDir)

        ConsoleModeLayout.addWidget(self.WithConsole)
        ConsoleModeLayout.addWidget(self.NoConsole)

        BuildOptionsLayout.addWidget(self.ShowPyInstallerCommandCheckbox)
        BuildOptionsLayout.addWidget(self.AsksToHideorShowTerminalCheckbox)
        BuildOptionsLayout.addWidget(self.CreateShortcutCheckbox)
        BuildOptionsLayout.addWidget(self.CleanFolderCheckbox)

        CancelAndBuildBottomButtonLayout.addWidget(CancelButton)
        CancelAndBuildBottomButtonLayout.addWidget(BuildButton)

        BottomSectionLayout.addLayout(BuildOptionsLayout)
        BottomSectionLayout.addStretch()
        BottomSectionLayout.addLayout(CancelAndBuildBottomButtonLayout)

        self.AssetsSectionLayout.addLayout(self.DynamicAssetsLayout)
        self.AssetsSectionLayout.addWidget(self.AddAssetButton)
        
        GridLayout.addWidget(AppNameLabel,0,0)
        GridLayout.addLayout(AppNameLayout,0,1,1,2)

        GridLayout.addWidget(DescriptionLabel,1,0)
        GridLayout.addWidget(self.DescriptionInput,1,1,1,2)

        GridLayout.addWidget(VersionLabel,2,0)
        
        GridLayout.addWidget(self.VersionInput,2,1,1,2)
        GridLayout.addWidget(SelectPyFileLabel,3,0)
        GridLayout.addLayout(PythonFileInputLayout,3,1)
        GridLayout.addWidget(self.SelectFileBrowseButton,3,2)

        GridLayout.addWidget(self.PythonFileStatusLabel,4,1)

        GridLayout.addWidget(AppTypeLabel,5,0)
        GridLayout.addLayout(BuildTypeLayout,5,1)

        GridLayout.addWidget(ConsoleModeLabel,6,0)
        GridLayout.addLayout(ConsoleModeLayout,6,1)

        GridLayout.addWidget(IconFileLabel,7,0)
        GridLayout.addLayout(IconFileInputLayout,7,1)
        GridLayout.addWidget(self.IconFileBrowseButton,7,2)

        GridLayout.addWidget(self.IconFileStatusLabel,8,1)

        GridLayout.addWidget(SaveAppLocationLabel,9,0)
        GridLayout.addWidget(self.SaveAppLocationInput,9,1)
        GridLayout.addWidget(self.SaveAppLocationBrowseButton,9,2)

        GridLayout.addWidget(AssetsLabel,10,0)

        self.MainWindow.setLayout(MainVerticalLayout)
        MainVerticalLayout.addLayout(BottomSectionLayout)

        # MainVerticalLayout.addStretch()
        self.CloseSplash()
        self.MainWindow.show()

        if "--post-install" in sys.argv:
            self.ThankYouOverlay = ShowThankYouFireworks()

        ConvertPyToExeApp.exec()
        
    def CreateAssetsRow(self):
        RemoveIcon = QIcon(AssetsPath.RemoveIcon)

        self.Placeholders = [
                            "Enter Asset Name",
                            "Paste Asset Path",
                            "Drop Asset Here"
                            ]

        self.PlaceholderIndex = 0

        NewAssetRowLayout = QHBoxLayout()
        NewAssetRowLayout.setContentsMargins(12,12,12,12)
        NewAssetRowLayout.setSpacing(12)

        AssetRowWidget = QFrame()
        AssetRowWidget.setStyleSheet(Style.AssetCardStyle)
        AssetRowWidget.setLayout(NewAssetRowLayout)

        AssetNameLabel = QLabel()
        AssetNameLabel.setText("Asset")
        AssetNameLabel.setStyleSheet(Style.LabelStyle)

        AssetNameInput = QLineEdit()
        AssetNameInput.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        AssetNameInput.setPlaceholderText(self.Placeholders[0])
        AssetNameInput.setStyleSheet(Style.InputStyle)

        AssetsBrowseButton = QPushButton()
        AssetsBrowseButton.setText("Browse Assets")
        AssetsBrowseButton.setToolTip("Browse Your Assets")
        AssetsBrowseButton.setCursor(Qt.PointingHandCursor)
        AssetsBrowseButton.setStyleSheet(Style.ButtonStyle)
        AssetsBrowseButton.clicked.connect(lambda:self.BrowseAssetFile(AssetNameInput))

        RemoveAssetButton = QPushButton()
        RemoveAssetButton.setIcon(QIcon(RemoveIcon))
        RemoveAssetButton.setIconSize(QSize(22,22))
        RemoveAssetButton.setToolTip("Remove")
        RemoveAssetButton.setStyleSheet(Style.RemoveAssetButtonStyle)
        RemoveAssetButton.setCursor(Qt.PointingHandCursor)
        RemoveAssetButton.clicked.connect(lambda:self.RemoveAssetRow(AssetWidget=AssetRowWidget))

        #Add Glow
        Style.TextGlow(AssetNameLabel)

        #Remove Button GLOW
        Style.DangerShadow(RemoveAssetButton)

        #Add Shadow
        #Label(s)
        Style.Shadow(AssetNameLabel)

        #Input (s)
        Style.Shadow(AssetNameInput)

        #Button (s)
        Style.Shadow(self.AddAssetButton)
        Style.Shadow(AssetsBrowseButton)
        Style.Shadow(RemoveAssetButton)

        #Widgets(s) 
        Style.Shadow(AssetRowWidget)

        NewAssetRowLayout.addWidget(AssetNameLabel)
        NewAssetRowLayout.addWidget(AssetNameInput)
        NewAssetRowLayout.addWidget(AssetsBrowseButton)
        NewAssetRowLayout.addWidget(RemoveAssetButton)

        return AssetRowWidget
    
    def BrowseMultipleAssets(self):
        Files, _ = QFileDialog.getOpenFileNames(self.MainWindow,"Select Assets")

        if not Files:
            return
        
        EmptyRows = []
        for Index in range(self.DynamicAssetsLayout.count()):
            RowWidget = self.DynamicAssetsLayout.itemAt(Index).widget()

            if RowWidget is None:
                continue

            AssetInput = RowWidget.findChild(QLineEdit)

            if AssetInput is None:
                continue

            if not AssetInput.toolTip():
                EmptyRows.append(AssetInput)

        for FilePath in Files:
            if EmptyRows:
                Input = EmptyRows.pop(0)

            else:
                NewRow = self.CreateAssetsRow()
                self.DynamicAssetsLayout.addWidget(NewRow)
                Input = NewRow.findChild(QLineEdit)

            Input.setText(QFileInfo(FilePath).fileName())
            Input.setToolTip(FilePath)

        for Input in EmptyRows:
            RowWidget = Input.parentWidget()

            if RowWidget:
                RowWidget.deleteLater()

    def RemoveLastAssetRow(self):
        Count = self.DynamicAssetsLayout.count()

        if Count == 0:
            return

        Item = self.DynamicAssetsLayout.takeAt(Count - 1)
        Widget = Item.widget()
        
        if Widget:
            Widget.deleteLater()

    def BrowseAssetFile(self,AssetInput):
        FilePath,_ = QFileDialog.getOpenFileName(self.MainWindow,"Select Assets File","",
                                                 "Assets Files (*.png *.jpg *.jpeg *.gif *.svg *.mp3 *.wav *.mp4 *.json *.txt *.ttf *.otf *.ico)")
        self.FullAssetFilePath = FilePath

        if FilePath:
            FileName = QFileInfo(FilePath).fileName()
            AssetInput.setText(FileName)
            AssetInput.setToolTip(FilePath)

    def AddAsset(self):
        NewRow = self.CreateAssetsRow()
        self.DynamicAssetsLayout.addWidget(NewRow)
        self.ChangePlaceholder()
        ScrollBar = self.AssetsScrollArea.verticalScrollBar()
        QTimer.singleShot(0,lambda: ScrollBar.setValue(ScrollBar.maximum()))
        self.AssetsScrollArea.ensureWidgetVisible(self.AddAssetButton)

    def ChangePlaceholder(self):
        if hasattr(self, "Timmer"):
            return

        self.Timmer = QTimer()

        self.AssetNameInput.setPlaceholderText(self.Placeholders[self.PlaceholderIndex])
        self.PlaceholderIndex += 1

        if self.PlaceholderIndex >= len(self.Placeholders):
            self.PlaceholderIndex = 0

        self.Timmer.timeout.connect(self.ChangePlaceholder)
        self.Timmer.start(2000)

    def ResetTheApp(self):
        Result = Messages.confirmReset(self.MainWindow)

        if Result == QMessageBox.Yes:

            self.AppNameInput.clear()
            self.SelectPyFileInput.clear()
            self.DescriptionInput.clear()
            self.IconFileInput.clear()
            self.SaveAppLocationInput.clear()
            self.AsksToHideorShowTerminalCheckbox.setChecked(False)
            self.ShowPyInstallerCommandCheckbox.setChecked(False)
            self.CreateShortcutCheckbox.setChecked(False)
            self.CleanFolderCheckbox.setChecked(False)

            for Button in self.BuildTypeGroup.buttons():
                
                Button.setAutoExclusive(False)
                Button.setChecked(False)
                Button.setAutoExclusive(True)

            for Button in self.ConsoleModeGroup.buttons():
                Button.setAutoExclusive(False)
                Button.setChecked(False)
                Button.setAutoExclusive(True)

            self.WithConsole.setAutoExclusive(False)
            self.WithConsole.setChecked(False)
            self.WithConsole.setAutoExclusive(True)
            self.MainWindow.repaint()
            self.AppNameInput.setFocus()

            self.OneFile.repaint()
            self.OneDir.repaint()

            self.NoConsole.repaint()
            self.WithConsole.repaint()

            while self.DynamicAssetsLayout.count():
                    LayoutItem = self.DynamicAssetsLayout.takeAt(0)
                    Widget = LayoutItem.widget()

                    if Widget is not None:
                        Widget.deleteLater()

    def BuildCompletedWindow(self,exepath):
        MainLayout = QVBoxLayout()
        TopLayout = QHBoxLayout()
        InfoLayout = QVBoxLayout()
        ButtonLayout = QHBoxLayout()
        QPixmap(AssetsPath.Checked)

        SizeMB = round(os.path.getsize(exepath) / (1024 * 1024),2)

        self.BuildHistory.Record(
            self.AppNameInput.text(),
            getattr(self,"SelectedPythonFilePath",""),
            exepath,
            "OneFile" if self.OneFile.isChecked() else "OneDir",
            "NoConsole" if self.NoConsole.isChecked() else "WithConsole",
            SizeMB,
        )

        Dialog = QDialog(self.MainWindow)
        Dialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Dialog.setWindowTitle("Build Complete")
        Dialog.setFixedSize(650,300)
        Dialog.setStyleSheet(Style.DialogStyle)

        AppNameLabel = QLabel()
        AppNameLabel.setText(f"App Name: {self.AppNameInput.text()}")
        AppNameLabel.setStyleSheet(Style.LabelStyle)

        SaveLocationLabel = QLabel()
        SaveLocationLabel.setText(f"Save Location:\n{self.SaveAppLocationInput.text()}")
        SaveLocationLabel.setStyleSheet(Style.LabelStyle)

        FileSizeLabel = QLabel()
        FileSizeLabel.setText(f"File Size: {SizeMB} MB")
        FileSizeLabel.setStyleSheet(Style.LabelStyle)

        IconLabel = QLabel()
        Pixmap = QPixmap(self.SelectedIconFilePath)
        IconLabel.setPixmap(Pixmap.scaled(
                                            128,128,
                                            Qt.KeepAspectRatio,Qt.SmoothTransformation
                                        )
                            )
        IconLabel.setStyleSheet(Style.LabelStyle)

        SuccessLabel = QLabel()
        SuccessLabel.setPixmap(QPixmap(AssetsPath.Checked).scaled(64,64,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        SuccessLabel.setAlignment(Qt.AlignCenter)
        SuccessLabel.setStyleSheet("""font-size:40pt;""")

        InfoLayout.addWidget(AppNameLabel)
        InfoLayout.addSpacing(15)
        InfoLayout.addWidget(SaveLocationLabel)
        InfoLayout.addSpacing(15)
        InfoLayout.addWidget(FileSizeLabel)

        TopLayout.addLayout(InfoLayout)
        TopLayout.addStretch()
        TopLayout.addWidget(IconLabel,alignment=Qt.AlignCenter)

        LaunchAppButton = QPushButton("Launch App")
        LaunchAppButton.setCursor(Qt.PointingHandCursor)
        LaunchAppButton.setFixedWidth(130)
        LaunchAppButton.setFixedHeight(50)
        LaunchAppButton.setToolTip("Launch App")
        LaunchAppButton.setStyleSheet(Style.ButtonStyle)
        LaunchAppButton.clicked.connect(lambda:subprocess.Popen(exepath))

        OpenFolderButton = QPushButton("Open Folder")
        OpenFolderButton.setCursor(Qt.PointingHandCursor)
        OpenFolderButton.setFixedWidth(130)
        OpenFolderButton.setFixedHeight(50)
        OpenFolderButton.setToolTip("Open Output Folder")
        OpenFolderButton.setStyleSheet(Style.SecondaryButtonStyle)
        OpenFolderButton.clicked.connect(lambda:os.startfile(os.path.dirname(exepath)))

        if self.CustomizationManager.GetBool("OpenFolderAfterBuild"):
            os.startfile(os.path.dirname(exepath))

        CloseButton = QPushButton()
        CloseButton.setText("Close")
        CloseButton.setCursor(Qt.PointingHandCursor)
        CloseButton.setToolTip("Close")
        CloseButton.setStyleSheet(Style.SecondaryButtonStyle)
        CloseButton.clicked.connect(Dialog.accept)

        #Add Shadows
        Style.Shadow(Dialog)

        ButtonLayout.addStretch()
        ButtonLayout.addWidget(LaunchAppButton)
        ButtonLayout.addWidget(OpenFolderButton)
        ButtonLayout.addWidget(CloseButton)

        MainLayout.addLayout(TopLayout)
        MainLayout.insertWidget(0,SuccessLabel)
        MainLayout.addStretch()
        MainLayout.addLayout(ButtonLayout)
        Dialog.setLayout(MainLayout)
        Dialog.exec()

    def RemoveAssetRow(self,AssetWidget):
        self.AssetsSectionLayout.removeWidget(AssetWidget)
        AssetWidget.deleteLater()

    def BrowsePythonFile(self):
        FilePath,_= QFileDialog.getOpenFileName(self.MainWindow,"Select Python (.py) file","","Python Files (*.py)")
        FileName = QFileInfo(FilePath).fileName()

        if FilePath:
            self.SelectPyFileInput.setText(FileName)
            self.SelectPyFileInput.setToolTip(FilePath)
            self.SelectedPythonFilePath = FilePath

    def BrowseIconFile(self):
        FilePath,_ = QFileDialog.getOpenFileName(self.MainWindow,"Select Icon (.ico) file","","Icon Files (*.ico)")
        FileName = QFileInfo(FilePath).baseName()
        self.SelectedIconFilePath = FilePath

        if FilePath:
            self.IconFileInput.setText(FileName)
            self.IconFileInput.setToolTip(FilePath)

    def SaveAppLocation(self):
        FilePath = QFileDialog.getExistingDirectory(self.MainWindow,"Select Folder / Location")

        if FilePath:
            self.SaveAppLocationInput.setText(FilePath)
            self.SaveAppLocationInput.setToolTip(FilePath)

    def ValidatePythonFile(self):
        FileName = self.SelectPyFileInput.text()

        if FileName.strip() == "":
            self.SelectPyFileInput.setStyleSheet(Style.NormalInputStyle)
            self.PythonFileStatusLabel.hide()
            self.SelectPyFileInput.setToolTip("")
            return

        FinalFileName = FileName + ".py"

        if FinalFileName in self.FileIndex:
            FullPath = self.FileIndex[FinalFileName]
            
            if os.path.exists(FullPath):
                self.SelectedPythonFilePath = FullPath
                self.SelectPyFileInput.setToolTip(FullPath)
                self.SelectPyFileInput.setStyleSheet(Style.NormalInputStyle)
                self.PythonFileStatusLabel.hide()

            else:
                del self.FileIndex[FinalFileName]

                self.SelectPyFileInput.setToolTip("")
                self.SelectPyFileInput.setStyleSheet(Style.InvalidInputStyle)
                self.PythonFileStatusLabel.show()
                self.StartBackgroundRescan()

        else:
            self.SelectPyFileInput.setStyleSheet(Style.InvalidInputStyle)
            self.PythonFileStatusLabel.show()
            self.SelectPyFileInput.setToolTip("")

    def StartBackgroundRescan(self):

        if self.FileIndexer.isRunning():
            return

        self.FileIndexer = FileIndexerThread()
        self.FileIndexer.IndexingFinished.connect(self.StoreFileIndex)
        self.FileIndexer.start()

    def StartValidationTimer(self):
        self.SearchTimer.start(1000)

    def StoreFileIndex(self, Index):
        # Merge rather than replace - a background rescan that (for whatever
        # reason) misses a folder it previously covered shouldn't erase a
        # file the user already has typed in and validated.
        self.FileIndex = {**self.FileIndex, **Index}
        self.PyIndexDB.Save(self.FileIndex)
        # The field may have been red only because this scan hadn't finished
        # yet - re-check whatever's currently typed now that the index grew.
        if hasattr(self,"SelectPyFileInput"):
            self.ValidatePythonFile()

    def ValidateIconFile(self):
        FileName = self.IconFileInput.text()

        if FileName.strip() == "":
            self.IconFileInput.setStyleSheet(Style.NormalInputStyle)
            self.IconFileInput.setToolTip("")
            self.IconFileStatusLabel.hide()
            return

        if FileName.lower().endswith(".ico"):
            FileName = FileName[:-len(".ico")]

            self.IconFileInput.blockSignals(True)
            self.IconFileInput.setText(FileName)
            self.IconFileInput.blockSignals(False)

            if FileName.strip() == "":
                self.IconFileInput.setStyleSheet(Style.NormalInputStyle)
                self.IconFileInput.setToolTip("")
                self.IconFileStatusLabel.hide()
                return

        FinalFileName = FileName + ".ico"

        if FinalFileName in self.IconIndex:
            FullPath = self.IconIndex[FinalFileName]

            if os.path.exists(FullPath):
                self.SelectedIconFilePath = FullPath
                self.IconFileInput.setToolTip(FullPath)
                self.IconFileInput.setStyleSheet(Style.NormalInputStyle)
                self.IconFileStatusLabel.hide()

            else:
                del self.IconIndex[FinalFileName]
                self.IconFileInput.setToolTip("")
                self.IconFileInput.setStyleSheet(Style.InvalidInputStyle)
                self.IconFileStatusLabel.show()
                self.StartBackgroundIconRescan()

        else:
            self.IconFileInput.setStyleSheet(Style.InvalidInputStyle)
            self.IconFileInput.setToolTip("")
            self.IconFileStatusLabel.show()

    def StartBackgroundIconRescan(self):

        if self.IconIndexer.isRunning():
            return

        self.IconIndexer = IconIndexerThread()
        self.IconIndexer.IndexingFinished.connect(self.StoreIconIndex)
        self.IconIndexer.start()

    def StoreIconIndex(self, Index):
        self.IconIndex = {**self.IconIndex, **Index}
        self.IconIndexDB.Save(self.IconIndex)
        if hasattr(self,"IconFileInput"):
            self.ValidateIconFile()

    def BuildApplication(self):

        #App Name Error Handling
        if not self.AppNameInput.text().strip():
            self.AppNameInput.setStyleSheet(Style.InvalidInputStyle)
            self.AppNameInput.setFocus()
            return
        
        #Description Input error Handling
        if not self.DescriptionInput.text().strip():
            Result = QMessageBox.question(self.MainWindow,"Description Empty","Description is empty.\n\nDo you want to continue anyway?",QMessageBox.Yes | QMessageBox.No)

            if Result == QMessageBox.No:
                self.DescriptionInput.setFocus()
                return
    
        # Python File Error Handling
        if (not hasattr(self, "SelectedPythonFilePath") or not os.path.exists(self.SelectedPythonFilePath)):
            self.SelectPyFileInput.setStyleSheet(Style.InvalidInputStyle)
            self.SelectPyFileInput.setFocus()
            return

        PythonExecutable = self.GetPythonExecutable()

        if not PythonExecutable:
            QMessageBox.critical(
                                    self.MainWindow,
                                    "Python Not Found",
                                    "Could not find a Python interpreter with PyInstaller installed.\n\n"
                                    "This app was built with PyInstaller, so it cannot run PyInstaller "
                                    "using itself. Please install Python and run:\n\n"
                                    "    pip install pyinstaller\n\n"
                                    "then make sure that Python is available on your system PATH."
                                )
            return

        Command = [PythonExecutable,"-m","PyInstaller"]
        Command.extend(
                        [
                            "--noconfirm",
                            "--clean",
                            "--paths",
                            os.path.dirname(self.SelectedPythonFilePath),
                            "--hidden-import=ctypes",
                            "--hidden-import=PySide6",
                            "--hidden-import=PySide6.QtCore",
                            "--hidden-import=PySide6.QtGui",
                            "--hidden-import=PySide6.QtWidgets",
                            "--hidden-import=html",
                            "--hidden-import=os"
                        ]
                    )

        # Build Type
        if self.CleanFolderCheckbox.isChecked() and not self.OneDir.isChecked():
            QMessageBox.warning(
                                    self.MainWindow,
                                    "Clean Folder Ignored",
                                    "'Clean Folder' only applies to 'One Dir' builds.\n\n"
                                    "Select 'One Dir' as the App Type to move DLLs into a DLLs folder."
                                )

        if self.OneFile.isChecked():
            Command.append("--onefile")

        elif self.OneDir.isChecked():

            if self.CleanFolderCheckbox.isChecked():
                Command.append("--contents-directory=DLLs")

        else:
            Command.append("--onefile")

        # Console Mode
        if self.NoConsole.isChecked():
            Command.append("--noconsole")

        elif self.WithConsole.isChecked():
            pass

        else:
            Command.append("--noconsole")

        # Icon file error handling
        if (not hasattr(self, "SelectedIconFilePath") or not os.path.exists(self.SelectedIconFilePath)):
            Result = Messages.EmptyIcon(self.MainWindow,self.AuthorName)

            if Result == QMessageBox.No:
                self.IconFileInput.setFocus()
                return
            
        if not self.SaveAppLocationInput.text().strip():
            self.SaveAppLocationInput.setStyleSheet(Style.InvalidInputStyle)
            self.SaveAppLocationInput.setFocus()
            return
    

        # Checks Path  exists or not
        SavePath = self.SaveAppLocationInput.text().strip()
        if not os.path.exists(SavePath):
            Result = Messages.CreateFolderQuestion(self.MainWindow,SavePath)

            if Result == QMessageBox.Yes:
                try:
                    os.makedirs(SavePath,exist_ok=True)

                except Exception:
                    self.SaveAppLocationInput.setStyleSheet(Style.InvalidInputStyle)
                    self.SaveAppLocationInput.setFocus()
                    return

            else:
                self.SaveAppLocationInput.setFocus()
                return
        
        if hasattr(self, "SelectedIconFilePath"):
            Command.append(f"--icon={self.SelectedIconFilePath}")

        if self.SaveAppLocationInput.text():
            Command.extend(["--distpath",self.SaveAppLocationInput.text()])

        if not self.ValidateAssets():
            return

        AssetSourcePaths = []

        for Index in range(self.DynamicAssetsLayout.count()):

            RowWidget = self.DynamicAssetsLayout.itemAt(Index).widget()

            if RowWidget is None:
                continue

            AssetInput = RowWidget.findChild(QLineEdit)

            if AssetInput is None:
                continue

            AssetPath = AssetInput.toolTip()

            if AssetPath:
                Command.extend(
                                [
                                    "--add-data",
                                    f"{AssetPath};."
                                ]
                                )
                AssetSourcePaths.append(AssetPath)

        if self.AppNameInput.text().strip():

            Command.extend(
                            [
                                "--name",
                                self.AppNameInput.text().strip()
                            ]
                        )
            
            VersionFilePath = self.GenerateVersionFile()
            Command.extend(
                            [
                                "--version-file",
                                VersionFilePath
                            ]
                            )

        Command.append(self.SelectedPythonFilePath)
        self.AssetSourcePaths = AssetSourcePaths
        CommandString = (" ".join(Command))

        if self.ShowPyInstallerCommandCheckbox.isChecked():
            self.ShowCommandPreviewWindow(CommandString,Command)
            return
        
        self.BuildCommand = Command
        self.ShowProgressDialog()
        self.BuildThread = BuildThread(
                                            self.BuildCommand,
                                            self.AsksToHideorShowTerminalCheckbox.isChecked(),
                                            self.SaveAppLocationInput.text(),
                                            self.AppNameInput.text(),
                                            os.path.dirname(self.SelectedPythonFilePath),
                                            self.AssetSourcePaths
                                        )
        self.BuildThread.ProgressChanged.connect(self.UpdateBuildProgress)
        self.BuildThread.BuildFinished.connect(
        self.ProgressDialog.accept)
        self.BuildThread.start()
        self.ProgressDialog.exec()
        self.BuildThread.wait()

        ExePath = os.path.join(
                                self.SaveAppLocationInput.text(),
                                f"{self.AppNameInput.text()}.exe"
                            )
        
        if os.path.exists(ExePath):

            if self.CreateShortcutCheckbox.isChecked():
                self.CreateStartMenuShortcut(ExePath)

            self.BuildCompletedWindow(ExePath)

    def HasPyInstaller(self,PythonExecutable):
        try:
            Result = subprocess.run(
                                        [PythonExecutable,"-c","import PyInstaller"],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL,
                                        timeout=15
                                    )
            return Result.returncode == 0

        except Exception:
            return False

    def GetPythonExecutable(self):
        if not getattr(sys, "frozen", False) and self.HasPyInstaller(sys.executable):
            return sys.executable

        for Candidate in ("python", "python3", "py"):
            Found = shutil.which(Candidate)

            if Found and self.HasPyInstaller(Found):
                return Found

        return None

    def ValidateAssets(self):
        AssetCount = 0

        BlockedExtensions = [
                                ".py",
                                ".pyw",
                                ".txt",
                                ".pdf",
                                ".docx"
                            ]
        
        for Index in range(self.DynamicAssetsLayout.count()):

            RowWidget = self.DynamicAssetsLayout.itemAt(Index).widget()
            if RowWidget is None:
                continue

            AssetInput = RowWidget.findChild(QLineEdit)
            if AssetInput is None:
                continue

            AssetPath = AssetInput.toolTip()
            if not AssetPath:
                continue

            Extension = os.path.splitext(AssetPath)[1].lower()
            if Extension in BlockedExtensions:
                QMessageBox.warning(self.MainWindow,"Invalid Asset",f"{Extension} files are not allowed as assets.")
                return False

            AssetCount += 1
            if not os.path.exists(AssetPath):
                AssetInput.setStyleSheet(Style.InvalidInputStyle)
                AssetInput.setFocus()
                QMessageBox.warning(self.MainWindow,"Missing Asset",f"I cannot find:\n\n{AssetPath}\n\nPlease select a real asset.")
                return False

        if AssetCount == 0:
            QMessageBox.warning(self.MainWindow,"Assets Missing","No assets added.\n\nReal applications usually need assets.")
            return False
        return True

    def ShowCommandPreviewWindow(self,CommandString,Command):
        LoaderWidget = QLabel()
        Movie = QMovie(AssetsPath.Loader)
        Movie.setScaledSize(QSize(24,24))
        LoaderWidget.setMovie(Movie)
        Movie.start()

        self.CopyIcon = QIcon(AssetsPath.CopyIcon)
        self.CheckedIcon = QIcon(AssetsPath.Checked)

        DialogMainLauout = QVBoxLayout()
        ButtonLayout = QHBoxLayout()
        Container = QWidget()
        Container.setFixedSize(40,40)

        self.CopyStack = QStackedLayout(Container)

        PreviewDialog = QDialog(self.MainWindow)
        PreviewDialog.setWindowTitle("PyInstaller Gennerated Command")
        PreviewDialog.setFixedSize(750,400)
        PreviewDialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        PreviewDialog.setStyleSheet(Style.DialogStyle)

        AppNameLabel = QLabel()
        AppNameLabel.setText(f"App Name: {self.AppNameInput.text()}")
        AppNameLabel.setStyleSheet(Style.AppNameLabelStyle)

        CommandLabel = QLabel()
        CommandLabel.setText("Command:")

        CommandText = QTextEdit()
        CommandText.setReadOnly(True)
        CommandText.setPlainText(CommandString)
        CommandText.setStyleSheet(Style.CommandTextStyle)

        self.CopyButton = QPushButton()
        self.CopyButton.setFixedSize(40,40)
        self.CopyButton.setIcon(QIcon(self.CopyIcon))
        self.CopyButton.setIconSize(QSize(24,24))
        self.CopyButton.setCursor(Qt.PointingHandCursor)
        self.CopyButton.setToolTip("Copy")
        self.CopyButton.setStyleSheet(Style.CopyButtonStyle)
        self.CopyButton.clicked.connect(lambda:self.CopyCommand(CommandString,self.CopyButton))

        CheckLabel = QLabel()
        CheckLabel.setAlignment(Qt.AlignCenter)
        CheckLabel.setPixmap(QPixmap(AssetsPath.Checked).scaled(24,24,Qt.KeepAspectRatio,Qt.SmoothTransformation))

        self.CopyStack.addWidget(self.CopyButton)
        self.CopyStack.addWidget(LoaderWidget)
        self.CopyStack.addWidget(CheckLabel)

        ContinueButton = QPushButton()
        ContinueButton.setText("continue")
        ContinueButton.setCursor(Qt.PointingHandCursor)
        ContinueButton.setFixedWidth(100)
        ContinueButton.setToolTip("Continue Build")
        ContinueButton.setStyleSheet(Style.ButtonStyle)
        ContinueButton.clicked.connect(PreviewDialog.accept)

        BackButton = QPushButton()
        BackButton.setText("Back")
        BackButton.setToolTip("Back")
        BackButton.setCursor(Qt.PointingHandCursor)
        BackButton.setStyleSheet(Style.SecondaryButtonStyle)
        BackButton.clicked.connect(PreviewDialog.reject)

        #Add Shadows
        Style.Shadow(CommandText)
        Style.Shadow(self.CopyButton)
        Style.Shadow(ContinueButton)
        Style.Shadow(BackButton)
        Style.Shadow(PreviewDialog)

        DialogMainLauout.addWidget(AppNameLabel)
        DialogMainLauout.addWidget(CommandLabel)
        DialogMainLauout.addWidget(CommandText)

        ButtonLayout.addWidget(BackButton)
        ButtonLayout.addStretch()
        ButtonLayout.addWidget(Container)
        ButtonLayout.addWidget(ContinueButton)

        DialogMainLauout.addLayout(ButtonLayout)
        PreviewDialog.setLayout(DialogMainLauout)

        Result = PreviewDialog.exec()
        QDialog.rejected

        if Result == QDialog.Accepted:
            if self.AsksToHideorShowTerminalCheckbox.isChecked():
                self.StartBuild(Command=Command)

            else:
                self.StartBuild(Command=Command)

    def CopyCommand(self, CommandString, Button):
        QApplication.clipboard().setText(CommandString)

        Button.setEnabled(False)
        Button.setIcon(QIcon())

        self.CopyStack.setCurrentIndex(1)
        QTimer.singleShot(800,lambda:self.CopyFinished(Button))
        
    def CopyFinished(self,Button):
        self.CopyStack.setCurrentIndex(2)
        QToolTip.showText(QCursor.pos(),"Copied!")
        QTimer.singleShot(1500,lambda:self.ResetCopyButton(Button))

    def ResetCopyButton(self,Button):
        self.CopyStack.setCurrentIndex(0)
        self.CopyButton.setIcon(QIcon(AssetsPath.CopyIcon))
        self.CopyButton.setEnabled(True)

    def ShowProgressDialog(self):
        Layout = QVBoxLayout()

        self.ProgressDialog = QDialog(self.MainWindow)
        self.ProgressDialog.resize(700,120)
        self.ProgressDialog.setWindowTitle("Progress")
        self.ProgressDialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        self.ProgressDialog.setStyleSheet(Style.DialogStyle)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setWindowTitle("Building Application")
        self.ProgressBar.resize(900,150)
        self.ProgressBar.setFixedHeight(20)
        self.ProgressBar.setTextVisible(True)
        self.ProgressBar.setRange(0,100)
        self.ProgressBar.setStyleSheet(Style.ProgressBarStyle)

        if self.AsksToHideorShowTerminalCheckbox.isChecked():
            self.ProgressBar.setRange(0,0)
            self.ProgressBar.setFormat("Building... (see terminal window)")

        else:
            self.ProgressBar.setRange(0,100)
            self.ProgressBar.setValue(0)

        self.ProgressStatusLabel = QLabel()
        self.ProgressStatusLabel.setText("Preparing Build...")
        self.ProgressStatusLabel.setStyleSheet(Style.LabelStyle)

        Layout.addWidget(self.ProgressStatusLabel)
        Layout.addWidget(self.ProgressBar)

        self.CancelBuildButton = QPushButton("Cancel Build")
        self.CancelBuildButton.setCursor(Qt.PointingHandCursor)
        self.CancelBuildButton.setToolTip("Cancel  Proogress")
        self.CancelBuildButton.setStyleSheet(Style.EdiButtonStyle)
        self.CancelBuildButton.clicked.connect(self.CancelBuild)

        Layout.addWidget(self.CancelBuildButton)
        self.ProgressDialog.setLayout(Layout)


    def UpdateBuildProgress(self, Value):

        self.ProgressBar.setValue(Value)

        if Value < 20:
            self.ProgressStatusLabel.setText("Preparing Build...")

        elif Value < 40:
            self.ProgressStatusLabel.setText("Analyzing Modules...")

        elif Value < 60:
            self.ProgressStatusLabel.setText("Collecting Libraries...")

        elif Value < 75:
            self.ProgressStatusLabel.setText("Building PYZ...")

        elif Value < 95:
            self.ProgressStatusLabel.setText("Building EXE...")

        elif Value < 96:
            self.ProgressStatusLabel.setText("Installing...")

        elif Value < 100:
            self.ProgressStatusLabel.setText("Finalizing Build...")

        else:
            self.ProgressStatusLabel.setText("Build Complete")

    def CancelBuild(self):
        Result = QMessageBox.question(self.ProgressDialog,"Cancel Build","Do you really want to cancel this build?",QMessageBox.Yes | QMessageBox.No)

        if Result == QMessageBox.No:
            return
        
        if hasattr(self, "BuildThread"):
            self.BuildThread.CancelBuild()

        self.ProgressDialog.reject()

    def StartBuild(self, Command):
        self.ShowProgressDialog()
        self.BuildThread = BuildThread(
                                            Command,
                                            self.AsksToHideorShowTerminalCheckbox.isChecked(),
                                            self.SaveAppLocationInput.text(),
                                            self.AppNameInput.text(),
                                            os.path.dirname(self.SelectedPythonFilePath),
                                            getattr(self,"AssetSourcePaths",[])
                                        )
        self.BuildThread.ProgressChanged.connect(self.UpdateBuildProgress)
        self.BuildThread.BuildFinished.connect(self.ProgressDialog.accept)
        self.BuildThread.start()
        self.ProgressDialog.exec()

        ExePath = os.path.join(self.SaveAppLocationInput.text(),f"{self.AppNameInput.text()}.exe")

        if os.path.exists(ExePath):
            self.CreateStartMenuShortcut(ExePath)
            self.BuildCompletedWindow(exepath=ExePath)

    def ShowSplashScreen(self):
        Palette = PALETTES.get(Style.Mode,PALETTES["Dark"])

        self.Splash = QWidget()
        self.Splash.setObjectName("SplashScreen")
        self.Splash.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        self.Splash.setAttribute(Qt.WA_TranslucentBackground)
        self.Splash.setFixedSize(420,260)
        self.Splash.setStyleSheet(f"""
                                    QWidget#SplashScreen
                                                        {{
                                                            background: {Palette['DialogBg']};
                                                            border: 2px solid rgba(0,170,255,140);
                                                            border-radius: 24px;
                                                        }}
                                """)

        Layout = QVBoxLayout(self.Splash)
        Layout.setAlignment(Qt.AlignCenter)
        Layout.setSpacing(10)

        IconLabel = QLabel()
        IconLabel.setPixmap(QIcon(AssetsPath.ApplicationIcon).pixmap(64,64))
        IconLabel.setAlignment(Qt.AlignCenter)
        IconLabel.setStyleSheet("background:transparent;border:none;")

        TitleLabel = QLabel("Pyxe")
        TitleLabel.setStyleSheet(Style.AppNameLabelStyle)
        TitleLabel.setAlignment(Qt.AlignCenter)
        Style.TextGlow(TitleLabel)

        LoaderLabel = QLabel()
        LoaderLabel.setAlignment(Qt.AlignCenter)
        LoaderLabel.setStyleSheet("background:transparent;border:none;")
        self.SplashMovie = QMovie(AssetsPath.Loader)
        self.SplashMovie.setScaledSize(QSize(36,36))
        LoaderLabel.setMovie(self.SplashMovie)
        self.SplashMovie.start()

        self.SplashStatusLabel = QLabel("Starting up...")
        self.SplashStatusLabel.setStyleSheet(Style.LabelStyle)
        self.SplashStatusLabel.setAlignment(Qt.AlignCenter)

        Layout.addStretch()
        Layout.addWidget(IconLabel)
        Layout.addWidget(TitleLabel)
        Layout.addWidget(LoaderLabel)
        Layout.addWidget(self.SplashStatusLabel)
        Layout.addStretch()

        ScreenGeometry = QApplication.primaryScreen().geometry()
        self.Splash.move(ScreenGeometry.center() - self.Splash.rect().center())

        self.Splash.show()
        self.SplashShownAt = time.time()
        self.SplashMinDurationMs = 1400
        QApplication.processEvents()

    def UpdateSplash(self,Text):
        if hasattr(self,"SplashStatusLabel"):
            self.SplashStatusLabel.setText(Text)
            QApplication.processEvents()

    def CloseSplash(self):
        if not hasattr(self,"Splash"):
            return

        # Startup (settings load + file indexing) is fast enough that the
        # splash could otherwise flash and vanish before it's even seen -
        # hold it on screen for a minimum duration, like a real splash.
        Elapsed = (time.time() - self.SplashShownAt) * 1000
        Remaining = int(self.SplashMinDurationMs - Elapsed)
        if Remaining > 0:
            Loop = QEventLoop()
            QTimer.singleShot(Remaining,Loop.quit)
            Loop.exec()

        if hasattr(self,"SplashMovie"):
            self.SplashMovie.stop()
        self.Splash.close()
        self.Splash.deleteLater()

    def BuildThemeSwatch(self,Mode):
        """A small VS-style mockup window (title bar / card / sample text)
        previewing what Mode actually looks like, independent of the app's
        currently-applied Style."""
        Palette = PALETTES.get(ThemeManager.Resolve(Mode),PALETTES["Dark"])

        Swatch = QFrame()
        Swatch.setFixedSize(148,84)
        Swatch.setStyleSheet(f"""
                                QFrame {{
                                            background:{Palette['WindowBg']};
                                            border:1px solid {Palette['CardBorder']};
                                            border-radius:10px;
                                        }}
                            """)

        Layout = QVBoxLayout(Swatch)
        Layout.setContentsMargins(9,9,9,9)
        Layout.setSpacing(6)

        TitleBar = QFrame()
        TitleBar.setFixedHeight(12)
        TitleBar.setStyleSheet("QFrame { background: rgba(0,170,255,190); border-radius:4px; }")

        Card = QFrame()
        Card.setFixedHeight(22)
        Card.setStyleSheet(f"""
                                QFrame {{
                                            background:{Palette['CardBg']};
                                            border:1px solid {Palette['CardBorder']};
                                            border-radius:6px;
                                        }}
                            """)

        SampleText = QLabel("Aa Bb")
        SampleText.setStyleSheet(f"QLabel {{ color:{Palette['Text']}; font-size:9pt; font-weight:700; background:transparent; border:none; }}")

        Layout.addWidget(TitleBar)
        Layout.addWidget(Card)
        Layout.addWidget(SampleText)
        Layout.addStretch()

        return Swatch

    def ShowFirstRunThemeDialog(self):
        Dialog = QDialog()
        Dialog.setWindowTitle("Choose Your Theme")
        Dialog.resize(460,420)
        Dialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Dialog.setStyleSheet(Style.DialogStyle)

        Layout = QVBoxLayout()

        TitleLabel = QLabel("Welcome! Pick a theme to get started.")
        TitleLabel.setStyleSheet(Style.LabelStyle)
        TitleLabel.setWordWrap(True)
        Style.TextGlow(TitleLabel)

        Group = QButtonGroup(Dialog)
        Radios = {}

        Layout.addSpacing(6)
        Layout.addWidget(TitleLabel)
        Layout.addSpacing(14)

        OptionsGrid = QGridLayout()
        OptionsGrid.setHorizontalSpacing(18)
        OptionsGrid.setVerticalSpacing(14)

        for Row,Mode in enumerate(("Light","Dark","System","Developer")):
            Radio = QRadioButton(Mode)
            Radio.setStyleSheet(Style.RadioButtonStyle)
            Radio.setCursor(Qt.PointingHandCursor)
            if Mode == self.ThemeMode:
                Radio.setChecked(True)
            Group.addButton(Radio)
            Radios[Mode] = Radio

            OptionsGrid.addWidget(self.BuildThemeSwatch(Mode),Row,0)
            OptionsGrid.addWidget(Radio,Row,1,Qt.AlignVCenter)

        Layout.addLayout(OptionsGrid)

        def PreviewSelection(Mode):
            OldSnapshot = self.SnapshotStyle()
            Style.ApplyTheme(ThemeManager.Resolve(Mode))
            self.RethemeWidgetTree(Dialog,OldSnapshot)

        for Mode,Radio in Radios.items():
            Radio.toggled.connect(lambda Checked,M=Mode: PreviewSelection(M) if Checked else None)

        Layout.addStretch()

        SkipButton = QPushButton("Skip")
        SkipButton.setCursor(Qt.PointingHandCursor)
        SkipButton.setStyleSheet(Style.SecondaryButtonStyle)

        def Skip():
            # Undo any live preview so the app doesn't launch in a theme
            # the user never actually confirmed.
            Style.ApplyTheme(ThemeManager.Resolve(self.ThemeMode))
            Dialog.reject()

        SkipButton.clicked.connect(Skip)

        ContinueButton = QPushButton("Continue")
        ContinueButton.setCursor(Qt.PointingHandCursor)
        ContinueButton.setStyleSheet(Style.ButtonStyle)

        def Confirm():
            for Mode,Radio in Radios.items():
                if Radio.isChecked():
                    self.ThemeMode = Mode
                    break
            ThemeManager.Set(self.ThemeMode)
            Style.ApplyTheme(ThemeManager.Resolve(self.ThemeMode))
            Dialog.accept()

        ContinueButton.clicked.connect(Confirm)

        ButtonLayout = QHBoxLayout()
        ButtonLayout.addWidget(SkipButton)
        ButtonLayout.addStretch()
        ButtonLayout.addWidget(ContinueButton)
        Layout.addLayout(ButtonLayout)

        Dialog.setLayout(Layout)
        Dialog.exec()

    def SnapshotStyle(self):
        """Every current Style.* stylesheet string, keyed by attribute name."""
        return {Name: Value for Name,Value in vars(Style).items() if isinstance(Value,str)}

    def RethemeWidgetTree(self,Root,OldSnapshot):
        """Re-applies the now-current Style.* stylesheets to every live widget
        under Root that was styled from the OLD snapshot - this is what makes
        a theme switch repaint every button/input/card immediately instead of
        only on the next launch. Works on any widget tree (the main window,
        or a standalone dialog like the first-run theme picker)."""
        NewSnapshot = self.SnapshotStyle()

        Widgets = Root.findChildren(QWidget)
        Widgets.append(Root)

        for Widget in Widgets:
            Current = Widget.styleSheet()
            if not Current:
                continue
            for Name,OldValue in OldSnapshot.items():
                if Current == OldValue:
                    NewValue = NewSnapshot.get(Name)
                    if NewValue is not None and NewValue != Current:
                        Widget.setStyleSheet(NewValue)
                    break

    def RethemeAllWidgets(self,OldSnapshot):
        self.RethemeWidgetTree(self.MainWindow,OldSnapshot)

    def AnimateThemeChange(self,ApplyFunction):
        """Crossfades self.MainWindow while ApplyFunction swaps the palette."""
        Effect = QGraphicsOpacityEffect(self.MainWindow)
        self.MainWindow.setGraphicsEffect(Effect)

        FadeOut = QPropertyAnimation(Effect,b"opacity",self.MainWindow)
        FadeOut.setDuration(140)
        FadeOut.setStartValue(1.0)
        FadeOut.setEndValue(0.25)
        FadeOut.setEasingCurve(QEasingCurve.OutCubic)

        FadeIn = QPropertyAnimation(Effect,b"opacity",self.MainWindow)
        FadeIn.setDuration(180)
        FadeIn.setStartValue(0.25)
        FadeIn.setEndValue(1.0)
        FadeIn.setEasingCurve(QEasingCurve.InCubic)

        def SwapAndFadeIn():
            ApplyFunction()
            FadeIn.start(QAbstractAnimation.DeleteWhenStopped)

        FadeOut.finished.connect(SwapAndFadeIn)
        FadeIn.finished.connect(lambda: self.MainWindow.setGraphicsEffect(None))

        self.ThemeAnimations = (FadeOut,FadeIn)
        FadeOut.start(QAbstractAnimation.DeleteWhenStopped)

    def PreviewTheme(self,Mode):
        Resolved = ThemeManager.Resolve(Mode)

        def Apply():
            OldSnapshot = self.SnapshotStyle()
            Style.ApplyTheme(Resolved)
            self.MainWindow.setWindowOpacity(Style.WindowOpacity)
            self.RethemeAllWidgets(OldSnapshot)
            self.CurrentThemeLabel.setText(
                f"Current mode: {Resolved}" + (" (via System)" if Mode == "System" else "")
            )

        self.AnimateThemeChange(Apply)

    def SaveThemeSettings(self):
        for Mode,Radio in self.ThemeRadios.items():
            if Radio.isChecked():
                self.ThemeMode = Mode
                break
        ThemeManager.Set(self.ThemeMode)

        def Apply():
            OldSnapshot = self.SnapshotStyle()
            Style.ApplyTheme(ThemeManager.Resolve(self.ThemeMode))
            self.MainWindow.setWindowOpacity(Style.WindowOpacity)
            self.RethemeAllWidgets(OldSnapshot)

        self.AnimateThemeChange(Apply)

    def SaveCustomizationDefaults(self):
        IsOneFile = self.DefaultOneFileToggle.isChecked()
        IsNoConsole = self.DefaultNoConsoleToggle.isChecked()
        WantsShortcut = self.DefaultCreateShortcutCheckbox.isChecked()
        WantsShowCommand = self.DefaultShowCommandCheckbox.isChecked()

        self.CustomizationManager.Set("DefaultBuildType","OneFile" if IsOneFile else "OneDir")
        self.CustomizationManager.Set("DefaultConsoleMode","NoConsole" if IsNoConsole else "WithConsole")
        self.CustomizationManager.Set("DefaultCreateShortcut",WantsShortcut)
        self.CustomizationManager.Set("DefaultShowCommand",WantsShowCommand)
        self.CustomizationManager.Set("OpenFolderAfterBuild",self.OpenFolderAfterBuildCheckbox.isChecked())
        self.CustomizationManager.Save()

        # Reflect the new defaults on the already-open main window immediately,
        # not just on the next launch.
        (self.OneFile if IsOneFile else self.OneDir).setChecked(True)
        (self.NoConsole if IsNoConsole else self.WithConsole).setChecked(True)
        self.CreateShortcutCheckbox.setChecked(WantsShortcut)
        self.ShowPyInstallerCommandCheckbox.setChecked(WantsShowCommand)

        QMessageBox.information(self.MainWindow,"Defaults Saved","Your default build preferences have been saved and applied.")

    def ShowSettingsWindow(self):
        Dialog = QDialog(self.MainWindow)
        Dialog.setWindowTitle("Settings")
        Dialog.resize(700,520)
        Dialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Dialog.setStyleSheet(Style.DialogStyle)

        MainLayout = QVBoxLayout()
        Tabs = QTabWidget()

        #Verify Tab
        VerifyTab = QWidget()
        VerifyLayout = QFormLayout()
        

        self.CompanyNameInput = QLineEdit()
        self.CompanyNameInput.setText(self.CompanyName)
        self.CompanyNameInput.setStyleSheet(Style.InputStyle)

        self.AuthorInput = QLineEdit()
        self.AuthorInput.setText(self.AuthorName)
        self.AuthorInput.setStyleSheet(Style.InputStyle)

        self.CopyrightInput = QLineEdit()
        self.CopyrightInput.setText(self.Copyright)
        self.CopyrightInput.setStyleSheet(Style.InputStyle)

        self.TrademarkInput = QLineEdit()
        self.TrademarkInput.setText(self.Trademark)
        self.TrademarkInput.setStyleSheet(Style.InputStyle)

        VerifyLayout.addRow("Company Name:",self.CompanyNameInput)
        VerifyLayout.addRow("Author:",self.AuthorInput)
        VerifyLayout.addRow("Copyright:",self.CopyrightInput)

        VerifyLayout.addRow("Trademark:",self.TrademarkInput)

        VerifyTab.setLayout(VerifyLayout)

        # About Tab
        AboutTab = QWidget()
        AboutLayout = QVBoxLayout()
        AboutLayout.setSpacing(4)

        AboutHeaderLayout = QHBoxLayout()
        AboutHeaderLayout.setSpacing(14)

        AboutIconLabel = QLabel()
        AboutIconLabel.setPixmap(QIcon(AssetsPath.ApplicationIcon).pixmap(56,56))
        AboutIconLabel.setStyleSheet("background:transparent;border:none;")

        AboutTitleLayout = QVBoxLayout()
        AboutTitleLayout.setSpacing(2)

        AppNameLabel = QLabel("Pyxe")
        AppNameLabel.setStyleSheet(Style.AppNameLabelStyle)
        Style.TextGlow(AppNameLabel)

        VersionLabel = QLabel(f"Version {APP_VERSION}  •  Theme: {self.ThemeMode}")
        VersionLabel.setStyleSheet(Style.LabelStyle)

        AboutTitleLayout.addWidget(AppNameLabel)
        AboutTitleLayout.addWidget(VersionLabel)

        AboutHeaderLayout.addWidget(AboutIconLabel)
        AboutHeaderLayout.addLayout(AboutTitleLayout)
        AboutHeaderLayout.addStretch()

        DescriptionLabel = QLabel(
            "Convert Python (.py) scripts into standalone Windows executables (.exe) using "
            "PyInstaller — without writing a build command by hand."
        )
        DescriptionLabel.setWordWrap(True)
        DescriptionLabel.setStyleSheet(Style.LabelStyle)

        HighlightsCard = QFrame()
        HighlightsCard.setStyleSheet(Style.CardStyle)
        HighlightsLayout = QVBoxLayout(HighlightsCard)
        HighlightsLayout.setContentsMargins(18,14,18,14)
        HighlightsLayout.setSpacing(6)

        HighlightsTitle = QLabel("Highlights")
        HighlightsTitle.setStyleSheet(Style.LabelStyle)

        HighlightsLayout.addWidget(HighlightsTitle)

        for Highlight in (
            "One-File / One-Dir builds with a live PyInstaller command preview",
            "Custom icon, version metadata, and bundled assets",
            "Editable keyboard shortcuts and Start Menu shortcut path",
            "Light, Dark, System, and Developer themes with instant live switching",
        ):
            HighlightLabel = QLabel(f"•  {Highlight}")
            HighlightLabel.setWordWrap(True)
            HighlightLabel.setStyleSheet(Style.LabelStyle)
            HighlightsLayout.addWidget(HighlightLabel)

        CreditsLabel = QLabel("Developer: Robin Gupta  •  Assisted by Claude Code")
        CreditsLabel.setStyleSheet(Style.LabelStyle)

        LinksLayout = QHBoxLayout()
        LinksLayout.addStretch()

        GitHubButton = QPushButton("View on GitHub")
        GitHubButton.setCursor(Qt.PointingHandCursor)
        GitHubButton.setStyleSheet(Style.SecondaryButtonStyle)
        GitHubButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(REPOSITORY_URL)))

        ReportIssueButton = QPushButton("Report an Issue")
        ReportIssueButton.setCursor(Qt.PointingHandCursor)
        ReportIssueButton.setStyleSheet(Style.SecondaryButtonStyle)
        ReportIssueButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"{REPOSITORY_URL}/issues")))

        LinksLayout.addWidget(GitHubButton)
        LinksLayout.addWidget(ReportIssueButton)

        AboutLayout.addSpacing(10)
        AboutLayout.addLayout(AboutHeaderLayout)
        AboutLayout.addSpacing(10)
        AboutLayout.addWidget(DescriptionLabel)
        AboutLayout.addSpacing(12)
        AboutLayout.addWidget(HighlightsCard)
        AboutLayout.addSpacing(12)
        AboutLayout.addWidget(CreditsLabel)
        AboutLayout.addStretch()
        AboutLayout.addLayout(LinksLayout)

        AboutTab.setLayout(AboutLayout)

        #Shortcut Tab
        ShortcutsTab = QWidget()
        ShortcutsLayout = QVBoxLayout()
        ShortcutsFormLayout = QFormLayout()

        self.ShortcutEdits = {}

        for Name,Label in SHORTCUT_LABELS.items():
            Edit = QKeySequenceEdit(QKeySequence(self.ShortcutManager.Get(Name)))
            Edit.setStyleSheet(Style.InputStyle)
            self.ShortcutEdits[Name] = Edit
            ShortcutsFormLayout.addRow(f"{Label}:",Edit)

        ShortcutsLayout.addLayout(ShortcutsFormLayout)
        ShortcutsLayout.addStretch()

        ShortcutsButtonLayout = QHBoxLayout()
        ShortcutsButtonLayout.addStretch()

        ResetShortcutsButton = QPushButton("Reset")
        ResetShortcutsButton.setCursor(Qt.PointingHandCursor)
        ResetShortcutsButton.setToolTip("Reset to Saved Shortcuts")
        ResetShortcutsButton.setStyleSheet(Style.SecondaryButtonStyle)
        ResetShortcutsButton.clicked.connect(self.ResetShortcuts)

        SaveShortcutsButton = QPushButton("Save Shortcuts")
        SaveShortcutsButton.setCursor(Qt.PointingHandCursor)
        SaveShortcutsButton.setToolTip("Save Shortcuts")
        SaveShortcutsButton.setStyleSheet(Style.ButtonStyle)
        SaveShortcutsButton.clicked.connect(self.SaveShortcuts)

        ShortcutsButtonLayout.addWidget(ResetShortcutsButton)
        ShortcutsButtonLayout.addWidget(SaveShortcutsButton)
        ShortcutsLayout.addLayout(ShortcutsButtonLayout)

        ShortcutsTab.setLayout(ShortcutsLayout)

        # Customize Tab
        CustomizeTab = QWidget()
        CustomizeOuterLayout = QVBoxLayout(CustomizeTab)
        CustomizeOuterLayout.setSpacing(16)
        CustomizeOuterLayout.setContentsMargins(2,10,2,2)

        def CustomizeSectionTitle(Text):
            Label = QLabel(Text)
            Label.setStyleSheet(Style.LabelStyle)
            Style.TextGlow(Label)
            return Label

        def CustomizeTogglePair(Options,Checked):
            Group = QButtonGroup()
            Layout = QHBoxLayout()
            Layout.setSpacing(6)
            Toggles = {}

            for Key,Text in Options:
                Toggle = QPushButton(Text)
                Toggle.setCheckable(True)
                Toggle.setStyleSheet(Style.ToggleButtonStyle)
                Toggle.setCursor(Qt.PointingHandCursor)
                Toggle.setChecked(Key == Checked)
                Group.addButton(Toggle)
                Toggles[Key] = Toggle
                Layout.addWidget(Toggle)

            Layout.addStretch()
            return Group,Toggles,Layout

        # --- Start Menu Shortcut card ---
        StartMenuCard = QFrame()
        StartMenuCard.setStyleSheet(Style.CardStyle)
        StartMenuCardLayout = QVBoxLayout(StartMenuCard)
        StartMenuCardLayout.setContentsMargins(20,16,20,18)
        StartMenuCardLayout.setSpacing(10)

        StartMenuCardLayout.addWidget(CustomizeSectionTitle("Start Menu Shortcut"))

        StartMenuPathRow = QHBoxLayout()
        StartMenuPathRow.setSpacing(10)

        self.StartMenuPathInput = QLineEdit()
        self.StartMenuPathInput.setStyleSheet(Style.InputStyle)
        self.StartMenuPathInput.setReadOnly(True)
        self.StartMenuPathInput.setText(AssetsPath.AddStartMenuShortcutPath)
        self.StartMenuPathInput.setToolTip(AssetsPath.AddStartMenuShortcutPath)

        EditButton = QPushButton("Edit")
        EditButton.setToolTip("Edit Path")
        EditButton.setCursor(Qt.PointingHandCursor)
        EditButton.setFixedWidth(90)
        EditButton.setStyleSheet(Style.SecondaryButtonStyle)
        EditButton.clicked.connect(self.EditStartMenuPath)

        StartMenuPathRow.addWidget(self.StartMenuPathInput,1)
        StartMenuPathRow.addWidget(EditButton)

        StartMenuCardLayout.addLayout(StartMenuPathRow)

        # --- Build defaults card ---
        DefaultsCard = QFrame()
        DefaultsCard.setStyleSheet(Style.CardStyle)
        DefaultsCardLayout = QVBoxLayout(DefaultsCard)
        DefaultsCardLayout.setContentsMargins(20,16,20,18)
        DefaultsCardLayout.setSpacing(18)

        DefaultsCardLayout.addWidget(CustomizeSectionTitle("Defaults for New Builds"))

        DefaultsGrid = QGridLayout()
        DefaultsGrid.setHorizontalSpacing(16)
        DefaultsGrid.setVerticalSpacing(10)
        DefaultsGrid.setColumnStretch(1,1)

        BuildTypeRowLabel = QLabel("Build Type")
        BuildTypeRowLabel.setStyleSheet(Style.LabelStyle)

        self.DefaultBuildTypeGroup,BuildTypeToggles,DefaultBuildTypeLayout = CustomizeTogglePair(
            [("OneFile","One File"),("OneDir","One Dir")],
            self.CustomizationManager.Get("DefaultBuildType"),
        )
        self.DefaultOneFileToggle = BuildTypeToggles["OneFile"]
        self.DefaultOneDirToggle = BuildTypeToggles["OneDir"]

        ConsoleModeRowLabel = QLabel("Console Mode")
        ConsoleModeRowLabel.setStyleSheet(Style.LabelStyle)

        self.DefaultConsoleModeGroup,ConsoleModeToggles,DefaultConsoleModeLayout = CustomizeTogglePair(
            [("NoConsole","No Console"),("WithConsole","Console")],
            self.CustomizationManager.Get("DefaultConsoleMode"),
        )
        self.DefaultNoConsoleToggle = ConsoleModeToggles["NoConsole"]
        self.DefaultWithConsoleToggle = ConsoleModeToggles["WithConsole"]

        DefaultsGrid.addWidget(BuildTypeRowLabel,0,0)
        DefaultsGrid.addLayout(DefaultBuildTypeLayout,0,1)
        DefaultsGrid.addWidget(ConsoleModeRowLabel,1,0)
        DefaultsGrid.addLayout(DefaultConsoleModeLayout,1,1)

        DefaultsCardLayout.addLayout(DefaultsGrid)

        CheckboxColumnLayout = QVBoxLayout()
        CheckboxColumnLayout.setSpacing(10)

        self.DefaultCreateShortcutCheckbox = QCheckBox("Create Start Menu Shortcut")
        self.DefaultCreateShortcutCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.DefaultCreateShortcutCheckbox.setCursor(Qt.PointingHandCursor)
        self.DefaultCreateShortcutCheckbox.setChecked(self.CustomizationManager.GetBool("DefaultCreateShortcut"))

        self.DefaultShowCommandCheckbox = QCheckBox("Show PyInstaller Command")
        self.DefaultShowCommandCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.DefaultShowCommandCheckbox.setCursor(Qt.PointingHandCursor)
        self.DefaultShowCommandCheckbox.setChecked(self.CustomizationManager.GetBool("DefaultShowCommand"))

        self.OpenFolderAfterBuildCheckbox = QCheckBox("Open Output Folder After Build")
        self.OpenFolderAfterBuildCheckbox.setStyleSheet(Style.CheckBoxStyle)
        self.OpenFolderAfterBuildCheckbox.setCursor(Qt.PointingHandCursor)
        self.OpenFolderAfterBuildCheckbox.setToolTip("Automatically opens the output folder in Explorer once a build finishes.")
        self.OpenFolderAfterBuildCheckbox.setChecked(self.CustomizationManager.GetBool("OpenFolderAfterBuild"))

        CheckboxColumnLayout.addWidget(self.DefaultCreateShortcutCheckbox)
        CheckboxColumnLayout.addWidget(self.DefaultShowCommandCheckbox)
        CheckboxColumnLayout.addWidget(self.OpenFolderAfterBuildCheckbox)

        DefaultsCardLayout.addLayout(CheckboxColumnLayout)

        SaveCustomizeButtonLayout = QHBoxLayout()
        SaveCustomizeButtonLayout.addStretch()

        SaveCustomizeButton = QPushButton("Save Defaults")
        SaveCustomizeButton.setCursor(Qt.PointingHandCursor)
        SaveCustomizeButton.setToolTip("Save Default Preferences")
        SaveCustomizeButton.setFixedWidth(150)
        SaveCustomizeButton.setStyleSheet(Style.ButtonStyle)
        SaveCustomizeButton.clicked.connect(self.SaveCustomizationDefaults)

        SaveCustomizeButtonLayout.addWidget(SaveCustomizeButton)

        CustomizeOuterLayout.addWidget(StartMenuCard)
        CustomizeOuterLayout.addWidget(DefaultsCard)
        CustomizeOuterLayout.addStretch()
        CustomizeOuterLayout.addLayout(SaveCustomizeButtonLayout)

        # Developer Tab (Theme)
        DeveloperTab = QWidget()
        DeveloperLayout = QVBoxLayout()

        ThemeLabel = QLabel("App Theme")
        ThemeLabel.setStyleSheet(Style.LabelStyle)
        Style.TextGlow(ThemeLabel)

        self.ThemeGroup = QButtonGroup()
        self.ThemeRadios = {}

        ThemeGrid = QGridLayout()
        ThemeGrid.setHorizontalSpacing(18)
        ThemeGrid.setVerticalSpacing(12)

        for Row,Mode in enumerate(("Light","Dark","System","Developer")):
            Radio = QRadioButton(Mode)
            Radio.setStyleSheet(Style.RadioButtonStyle)
            Radio.setCursor(Qt.PointingHandCursor)
            if Mode == self.ThemeMode:
                Radio.setChecked(True)
            self.ThemeGroup.addButton(Radio)
            self.ThemeRadios[Mode] = Radio

            ThemeGrid.addWidget(self.BuildThemeSwatch(Mode),Row,0)
            ThemeGrid.addWidget(Radio,Row,1,Qt.AlignVCenter)

        DeveloperLayout.addLayout(ThemeGrid)

        self.CurrentThemeLabel = QLabel(f"Current mode: {ThemeManager.Resolve(self.ThemeMode)}"
                                         + (" (via System)" if self.ThemeMode == "System" else ""))
        self.CurrentThemeLabel.setStyleSheet(Style.LabelStyle)

        for Mode,Radio in self.ThemeRadios.items():
            Radio.toggled.connect(lambda Checked,M=Mode: self.PreviewTheme(M) if Checked else None)

        DeveloperLayout.addSpacing(10)
        DeveloperLayout.addWidget(self.CurrentThemeLabel)
        DeveloperLayout.addStretch()

        DeveloperTab.setLayout(DeveloperLayout)

        # Tabs
        Tabs.addTab(VerifyTab,"Verify")
        Tabs.addTab(ShortcutsTab,"Shortcut")
        Tabs.addTab(CustomizeTab,"Customize")
        Tabs.addTab(DeveloperTab,"Theme")
        Tabs.addTab(AboutTab,"About")

        # Buttons
        ButtonLayout = QHBoxLayout()

        SaveButton = QPushButton("Save")
        SaveButton.setCursor(Qt.PointingHandCursor)
        SaveButton.setToolTip("Save")
        SaveButton.setStyleSheet(Style.ButtonStyle)

        CloseButton = QPushButton("Close")
        CloseButton.setCursor(Qt.PointingHandCursor)
        CloseButton.setToolTip("Close")
        CloseButton.setStyleSheet(Style.SecondaryButtonStyle)

        SaveButton.clicked.connect(self.SaveVerificationSettings)
        SaveButton.clicked.connect(self.SaveThemeSettings)
        CloseButton.clicked.connect(Dialog.accept)

        ButtonLayout.addStretch()
        ButtonLayout.addWidget(SaveButton)
        ButtonLayout.addWidget(CloseButton)

        MainLayout.addWidget(Tabs)
        MainLayout.addLayout(ButtonLayout)

        Dialog.setLayout(MainLayout)
        Dialog.exec()

    def EditStartMenuPath(self):
        self.PathDialog = QDialog(self.MainWindow)
        self.PathDialog.resize(850,120)
        self.PathDialog.setWindowTitle("Edit Start Menu Shortcut Creation Path")
        self.PathDialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        self.PathDialog.setStyleSheet(Style.DialogStyle)

        Layout = QVBoxLayout()
        Layout = QGridLayout()
        ButtonLayout = QHBoxLayout()

        self.PathInput = QLineEdit()
        self.PathInput.setStyleSheet((Style.InputStyle))
        self.PathInput.setText(self.StartMenuPathInput.text())

        self.BrowseButton = QPushButton("Browse")
        self.BrowseButton.setToolTip("Browse Path")
        self.BrowseButton.setCursor(Qt.PointingHandCursor)
        self.BrowseButton.setStyleSheet(Style.ButtonStyle)
        self.BrowseButton.setFixedWidth(100)
        self.BrowseButton.clicked.connect(self.BrowseButtonLogic)

        self.SaveButton = QPushButton("Save")
        self.SaveButton.setToolTip("Save Path")
        self.SaveButton.setCursor(Qt.PointingHandCursor)
        self.SaveButton.setFixedWidth(100)
        self.SaveButton.setStyleSheet(Style.ButtonStyle)
        self.SaveButton.clicked.connect(self.SaveButtonLogic)

        Layout.addWidget(self.PathInput,0,0)
        Layout.addWidget(self.BrowseButton,0,1)

        ButtonLayout.addStretch()

        CancelButton = QPushButton("Cancel")
        CancelButton.setCursor(Qt.PointingHandCursor)
        CancelButton.setToolTip("Cancel")
        CancelButton.setFixedWidth(100)
        CancelButton.setStyleSheet(Style.SecondaryButtonStyle)
        CancelButton.clicked.connect(self.PathDialog.reject)

        ButtonLayout.addWidget(self.SaveButton)
        ButtonLayout.addWidget(CancelButton)

        Layout.addLayout(ButtonLayout,1,0,1,2)
        self.PathDialog.setLayout(Layout)
        self.PathDialog.exec()
        
    def BrowseButtonLogic(self):
        Folder = QFileDialog.getExistingDirectory(self.PathDialog,"Select Shortcut Folder")

        if Folder:
            self.PathInput.setText(Folder)

    def SaveButtonLogic(self):
        Path = self.PathInput.text().strip()

        if not os.path.exists(Path):
            QMessageBox.warning(
                                    self.PathDialog,
                                    "Invalid Path",
                                    "This path does not exist."
                                )

            return

        self.StartMenuPathInput.setText(Path)
        AssetsPath.AddStartMenuShortcutPath = Path
        self.CustomizationManager.Set("StartMenuPath",Path)
        self.CustomizationManager.Save()
        self.PathDialog.accept()

    def SaveVerificationSettings(self):
        try:

            with open(VERIFICATION_FILE,"w",encoding="utf-8") as File:
                File.write(f"CompanyName={self.CompanyNameInput.text()}\n")
                File.write(f"AuthorName={self.AuthorInput.text()}\n")
                File.write(f"Copyright={self.CopyrightInput.text()}\n")
                File.write(f"Trademark={self.TrademarkInput.text()}\n")

            self.CompanyName = self.CompanyNameInput.text()
            self.AuthorName = self.AuthorInput.text()
            self.Copyright = self.CopyrightInput.text()
            self.Trademark = self.TrademarkInput.text()
            Messages.settingsSaved(self.MainWindow)

        except Exception as Error:
            Messages.saveError(self.MainWindow,str(Error))

    def LoadVerificationSettings(self):

        self.CompanyName = ""
        self.AuthorName = ""
        self.Copyright = ""
        self.Trademark = ""

        try:
            if not os.path.exists(VERIFICATION_FILE):
                return

            with open(VERIFICATION_FILE,"r",encoding="utf-8") as File:

                for Line in File:
                    if "=" not in Line:
                        continue

                    Key,Value = Line.strip().split("=",1)

                    if Key == "CompanyName":
                        self.CompanyName = Value

                    elif Key == "AuthorName":
                        self.AuthorName = Value

                    elif Key == "Copyright":
                        self.Copyright = Value

                    elif Key == "Trademark":
                        self.Trademark = Value

        except Exception:
            pass

    def ApplyShortcuts(self):
        for Name,Handler in self.ShortcutActionHandlers.items():
            KeySequenceText = self.ShortcutManager.Get(Name)

            if Name in self.ShortcutObjects:
                self.ShortcutObjects[Name].setKey(QKeySequence(KeySequenceText))
            else:
                Shortcut = QShortcut(
                                        QKeySequence(KeySequenceText),
                                        self.MainWindow,
                                        Handler
                                    )
                Shortcut.setContext(Qt.WidgetWithChildrenShortcut)
                self.ShortcutObjects[Name] = Shortcut

    def FocusNextInput(self):
        FocusWidget = self.MainWindow.focusWidget()

        if FocusWidget:
            FocusWidget.focusNextChild()

    def SaveShortcuts(self):
        try:
            UsedSequences = {}

            for Name,Edit in self.ShortcutEdits.items():
                SequenceText = Edit.keySequence().toString()

                if not SequenceText:
                    continue

                if SequenceText in UsedSequences:
                    QMessageBox.warning(
                                            self.MainWindow,
                                            "Duplicate Shortcut",
                                            f"'{SequenceText}' is already assigned to "
                                            f"'{SHORTCUT_LABELS[UsedSequences[SequenceText]]}'."
                                        )
                    return

                UsedSequences[SequenceText] = Name

            for Name,Edit in self.ShortcutEdits.items():
                SequenceText = Edit.keySequence().toString()

                if SequenceText:
                    self.ShortcutManager.Set(Name,SequenceText)

            self.ShortcutManager.Save()
            self.ApplyShortcuts()
            Messages.settingsSaved(self.MainWindow)

        except Exception as Error:
            Messages.saveError(self.MainWindow,str(Error))

    def ResetShortcuts(self):
        for Name,Edit in self.ShortcutEdits.items():
            Edit.setKeySequence(QKeySequence(self.ShortcutManager.Get(Name)))

    def IsRegistrationComplete(self):
        return bool(
                    self.CompanyName.strip()
                    and self.AuthorName.strip()
                    and self.Copyright.strip()
                    and self.Trademark.strip()
                )

    def ShowRegistrationDialog(self):
        Dialog = QDialog()
        Dialog.setWindowTitle("Welcome - Registration Required")
        Dialog.resize(500,350)
        Dialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Dialog.setStyleSheet(Style.DialogStyle)
        Dialog.setWindowFlags(Dialog.windowFlags() & ~Qt.WindowCloseButtonHint)

        MainLayout = QVBoxLayout()

        InfoLabel = QLabel("Please fill in your details before you get started.")
        InfoLabel.setStyleSheet(Style.LabelStyle)
        InfoLabel.setWordWrap(True)
        MainLayout.addWidget(InfoLabel)
        MainLayout.addSpacing(10)

        FormLayout = QFormLayout()

        CompanyNameInput = QLineEdit()
        CompanyNameInput.setStyleSheet(Style.InputStyle)

        AuthorInput = QLineEdit()
        AuthorInput.setStyleSheet(Style.InputStyle)

        CopyrightInput = QLineEdit()
        CopyrightInput.setStyleSheet(Style.InputStyle)

        TrademarkInput = QLineEdit()
        TrademarkInput.setStyleSheet(Style.InputStyle)

        FormLayout.addRow("Company Name:",CompanyNameInput)
        FormLayout.addRow("Author:",AuthorInput)
        FormLayout.addRow("Copyright:",CopyrightInput)
        FormLayout.addRow("Trademark:",TrademarkInput)

        MainLayout.addLayout(FormLayout)
        MainLayout.addStretch()

        ButtonLayout = QHBoxLayout()

        NotNowButton = QPushButton("Not Now")
        NotNowButton.setCursor(Qt.PointingHandCursor)
        NotNowButton.setToolTip("Skip for now - you can fill this in later from Settings > Verify")
        NotNowButton.setStyleSheet(Style.SecondaryButtonStyle)
        NotNowButton.clicked.connect(Dialog.accept)

        GetStartedButton = QPushButton("Get Started")
        GetStartedButton.setCursor(Qt.PointingHandCursor)
        GetStartedButton.setStyleSheet(Style.ButtonStyle)

        ButtonLayout.addWidget(NotNowButton)
        ButtonLayout.addStretch()
        ButtonLayout.addWidget(GetStartedButton)
        MainLayout.addLayout(ButtonLayout)

        Dialog.setLayout(MainLayout)

        def HandleGetStarted():
            if (
                not CompanyNameInput.text().strip()
                or not AuthorInput.text().strip()
                or not CopyrightInput.text().strip()
                or not TrademarkInput.text().strip()
            ):
                QMessageBox.warning(
                                        Dialog,
                                        "Missing Details",
                                        "All fields are required before you can continue."
                                    )
                return

            self.CompanyName = CompanyNameInput.text().strip()
            self.AuthorName = AuthorInput.text().strip()
            self.Copyright = CopyrightInput.text().strip()
            self.Trademark = TrademarkInput.text().strip()

            try:
                with open(VERIFICATION_FILE,"w",encoding="utf-8") as File:
                    File.write(f"CompanyName={self.CompanyName}\n")
                    File.write(f"AuthorName={self.AuthorName}\n")
                    File.write(f"Copyright={self.Copyright}\n")
                    File.write(f"Trademark={self.Trademark}\n")
            except Exception as Error:
                Messages.saveError(Dialog,str(Error))
                return

            Dialog.accept()

        GetStartedButton.clicked.connect(HandleGetStarted)

        return Dialog.exec() == QDialog.Accepted

    def GenerateVersionFile(self):
        VersionFilePath = os.path.join(
                                        os.path.dirname(self.SelectedPythonFilePath),
                                        "version_info.txt"
                                        )

        Version = self.VersionInput.text().strip()

        Parts = Version.split(".")

        while len(Parts) < 4:
            Parts.append("0")

        Major,Minor,Patch,Build = Parts[:4]

        with open(
            VersionFilePath,
            "w",
            encoding="utf-8"
        ) as File:

            File.write(
    textwrap.dedent(f"""\
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({Major},{Minor},{Patch},{Build}),
        prodvers=({Major},{Minor},{Patch},{Build}),
        mask=0x3f,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo(
            [
                StringTable(
                    '040904B0',
                    [
                        StringStruct(
                            'CompanyName',
                            {repr(self.CompanyName)}
                        ),

                        StringStruct(
                            'FileDescription',
                            {repr(self.DescriptionInput.text())}
                        ),

                        StringStruct(
                            'FileVersion',
                            {repr(Version)}
                        ),

                        StringStruct(
                            'InternalName',
                            {repr(self.AppNameInput.text())}
                        ),

                        StringStruct(
                            'OriginalFilename',
                            {repr(self.AppNameInput.text() + ".exe")}
                        ),

                        StringStruct(
                            'ProductName',
                            {repr(self.AppNameInput.text())}
                        ),

                        StringStruct(
                            'ProductVersion',
                            {repr(Version)}
                        ),

                        StringStruct(
                            'LegalCopyright',
                            {repr(self.Copyright)}
                        ),

                        StringStruct(
                            'LegalTrademarks',
                            {repr(self.Trademark)}
                        )
                    ]
                )
            ]
        ),

        VarFileInfo(
            [
                VarStruct(
                    'Translation',
                    [1033, 1200]
                )
            ]
        )
    ]
)
""").lstrip()
)

        return VersionFilePath
    
    def CreateStartMenuShortcut(self, ExePath):
        ShortcutFolder = AssetsPath.AddStartMenuShortcutPath

        if not os.path.exists(ShortcutFolder):
            os.makedirs(ShortcutFolder, exist_ok=True)

        ShortcutName = f"{self.AppNameInput.text()}.lnk"
        ShortcutPath = os.path.join(ShortcutFolder,ShortcutName)
        Shell = Dispatch("WScript.Shell")
        Shortcut = Shell.CreateShortCut(ShortcutPath)
        Shortcut.TargetPath = ExePath
        Shortcut.WorkingDirectory = os.path.dirname(ExePath)
        Shortcut.IconLocation = ExePath
        Shortcut.save()
        
