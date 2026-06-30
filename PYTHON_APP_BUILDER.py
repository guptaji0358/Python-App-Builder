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

class ConvertPyToExe():

    def __init__(self):
        super().__init__()
        ConvertPyToExeApp = QApplication(sys.argv)

        self.LoadVerificationSettings()
        self.CurrentProgress = 10

        self.FileIndex = {}
        
        self.FileIndexer = FileIndexerThread()
        self.FileIndexer.IndexingFinished.connect(self.StoreFileIndex)
        self.FileIndexer.start()

        self.IconIndexer = IconIndexerThread()
        self.IconIndexer.IndexingFinished.connect(self.StoreIconIndex)
        self.IconIndexer.start()

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
        self.MainWindow.setWindowOpacity(0.76)
        self.MainWindow.setWindowFlags(Qt.Window)
        self.MainWindow.setWindowTitle("python App Builder")
        self.MainWindow.setStyleSheet(Style.MainWindowStyle)
        self.MainWindow.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        self.MainWindow.resize(1250,750)

        #Shortcuts
        QShortcut(QKeySequence("Ctrl + Shift + B"),self.MainWindow,self.BrowseMultipleAssets)
        QShortcut(QKeySequence("Ctrl + Shift + A"),self.MainWindow,self.AddAsset)
        QShortcut(QKeySequence("Ctrl + Shift + R"),self.MainWindow,self.RemoveLastAssetRow)
        
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

        #Add Glow
        Style.Shadow(self.MenuButton)

        #Add Assets (s)
        Style.AddButtonGlow

        #Label (s)
        Style.TextGlow(SelectPyFileLabel)
        Style.TextGlow(self.PythonFileStatusLabel)
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

        GridLayout.addWidget(SaveAppLocationLabel,8,0)
        GridLayout.addWidget(self.SaveAppLocationInput,8,1)
        GridLayout.addWidget(self.SaveAppLocationBrowseButton,8,2)

        GridLayout.addWidget(AssetsLabel,9,0)

        self.MainWindow.setLayout(MainVerticalLayout)
        MainVerticalLayout.addLayout(BottomSectionLayout)

        # MainVerticalLayout.addStretch()
        self.MainWindow.show()
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

        Dialog = QDialog(self.MainWindow)
        Dialog.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Dialog.setWindowTitle("Build Complete")
        Dialog.setFixedSize(650,300)

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
        self.FileIndex = Index

    def ValidateIconFile(self):
        FileName = self.IconFileInput.text()

        if FileName.strip() == "":
            self.IconFileInput.setStyleSheet(Style.NormalInputStyle)
            self.IconFileInput.setToolTip("")
            return
        
        FinalFileName = FileName + ".ico"

        if FinalFileName in self.IconIndex:
            FullPath = self.IconIndex[FinalFileName]

            if os.path.exists(FullPath):
                self.SelectedIconFilePath = FullPath
                self.IconFileInput.setToolTip(FullPath)
                self.IconFileInput.setStyleSheet(Style.NormalInputStyle)

            else:
                del self.IconIndex[FinalFileName]
                self.IconFileInput.setToolTip("")
                self.IconFileInput.setStyleSheet(Style.InvalidInputStyle)
                self.StartBackgroundIconRescan()

        else:
            self.IconFileInput.setStyleSheet(Style.InvalidInputStyle)
            self.IconFileInput.setToolTip("")

    def StartBackgroundIconRescan(self):

        if self.IconIndexer.isRunning():
            return

        self.IconIndexer = IconIndexerThread()
        self.IconIndexer.IndexingFinished.connect(self.StoreIconIndex)
        self.IconIndexer.start()

    def StoreIconIndex(self, Index):
        self.IconIndex = Index

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
        Command = [sys.executable,"-m","PyInstaller"]
        Command.extend(
                        [
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
        if self.OneFile.isChecked():
            Command.append("--onefile")

        elif self.OneDir.isChecked():
            pass

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

        for Index in range(self.DynamicAssetsLayout.count()):

            if not self.ValidateAssets():
                return
            
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
                                            self.AppNameInput.text()
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
                                            self.AppNameInput.text()
                                        )
        self.BuildThread.ProgressChanged.connect(self.UpdateBuildProgress)
        self.BuildThread.BuildFinished.connect(self.ProgressDialog.accept)
        self.BuildThread.start()
        self.ProgressDialog.exec()

        ExePath = os.path.join(self.SaveAppLocationInput.text(),f"{self.AppNameInput.text()}.exe")

        if os.path.exists(ExePath):
            self.CreateStartMenuShortcut(ExePath)
            self.BuildCompletedWindow(exepath=ExePath)

    def ShowSettingsWindow(self):
        Dialog = QDialog(self.MainWindow)
        Dialog.setWindowTitle("Settings")
        Dialog.resize(700,450)
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

        AppNameLabel = QLabel("Python App Builder")
        VersionLabel = QLabel("Version : 1.0.0.0")
        DescriptionLabel = QLabel("Description : Convert Python (.py) files into executable (.exe) applications.")
        MotiveLabel = QLabel("Motive : Automate Python to EXE conversion without writing long PyInstaller commands manually.")
        DeveloperLabel = QLabel("Developer : Robin Gupta")

        for Label in [AppNameLabel,VersionLabel,DescriptionLabel,MotiveLabel,DeveloperLabel]:
            Label.setStyleSheet(Style.LabelStyle)
            Style.TextGlow(Label)

        AboutLayout.addSpacing(15)
        AboutLayout.addWidget(AppNameLabel)
        AboutLayout.addSpacing(10)

        AboutLayout.addWidget(VersionLabel)
        AboutLayout.addSpacing(10)

        AboutLayout.addWidget(DescriptionLabel)
        AboutLayout.addSpacing(10)

        AboutLayout.addWidget(MotiveLabel)
        AboutLayout.addSpacing(10)

        AboutLayout.addWidget(DeveloperLabel)
        AboutLayout.addStretch()

        AboutTab.setLayout(AboutLayout)

        #Shortcut Tab
        ShortcutsTab = QWidget()
        ShortcutsLayout = QVBoxLayout()
        ShortcutsInfo = QLabel(
                                """
                                    #     Shortcut          Description
                                
                                    1  Ctrl + Shift + A  = Add Asset

                                    2  Ctrl + Shift + B  = Browse Multiple Assets

                                    3  Ctrl + Shift + R  = Remove Last Asset
                                    """
                                )

        ShortcutsInfo.setStyleSheet(Style.LabelStyle)
        ShortcutsLayout.addWidget(ShortcutsInfo)
        ShortcutsLayout.addStretch()
        ShortcutsTab.setLayout(ShortcutsLayout)

        # Customize Tab
        CustomizeTab = QWidget()
        CustomizeLayout = QFormLayout()
        EditButtonLayout = QHBoxLayout()

        self.StartMenuPathInput = QLineEdit()
        self.StartMenuPathInput.setStyleSheet(Style.InputStyle)
        self.StartMenuPathInput.setReadOnly(True)
        self.StartMenuPathInput.setText(AssetsPath.AddStartMenuShortcutPath)
        self.StartMenuPathInput.setToolTip(AssetsPath.AddStartMenuShortcutPath)

        EditButton = QPushButton("Edit")
        EditButton.setToolTip("Eddit Path")
        EditButton.setCursor(Qt.PointingHandCursor)
        EditButton.setStyleSheet(Style.EdiButtonStyle)
        EditButton.clicked.connect(self.EditStartMenuPath)

        CustomizeLayout.addRow("Start Menu Path:",self.StartMenuPathInput)
        EditButtonLayout.addStretch()
        EditButtonLayout.addWidget(EditButton)
        CustomizeLayout.addRow("",EditButtonLayout)
        CustomizeTab.setLayout(CustomizeLayout)

        # Tabs
        Tabs.addTab(VerifyTab,"Verify")
        Tabs.addTab(ShortcutsTab,"Shortcut")
        Tabs.addTab(CustomizeTab,"Customize")
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
        self.PathDialog.accept()

    def SaveVerificationSettings(self):
        try:

            with open("verification.txt","w",encoding="utf-8") as File:
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

        self.CompanyName = "Robin Gupta Studios"
        self.AuthorName = "Robin Gupta"
        self.Copyright = "Copyright © Robin Gupta"
        self.Trademark = "RGS™"

        try:
            if not os.path.exists("verification.txt"):
                return

            with open("verification.txt","r",encoding="utf-8") as File:

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

    def GenerateVersionFile(self):
        VersionFilePath = "version_info.txt"

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
        
class FileIndexerThread(QThread):
    IndexingFinished = Signal(dict)

    def run(self):
        FileIndex = {}
        UserFolder = os.path.expanduser("~")
        PriorityFolder = [
                            os.path.join(UserFolder,"Desktop"),
                            os.path.join(UserFolder,"Downloads"),
                            os.path.join(UserFolder,"Documents"),
                            os.path.join(UserFolder,"OneDrive"),
                            "C:/Users"
                        ]

        ExcludeFolder = [
                            "Windows",
                            "Program Files",
                            "Program Files (x86)",
                            "AppData",
                            "__pycache__",
                            "venv",
                            ".git",
                            "node_modules",
                            ".vscode",
                            ".idea",
                            "$RECYCLE.BIN",
                            "System Volume Information",
                            "Temp",
                            "tmp",
                            "recents",
                            "%temp%"
                        ]

        for Folder in PriorityFolder:
            if os.path.exists(Folder):
                try:
                    for Root, Dirs, Files in os.walk(Folder):
                        Dirs[:] = [
                            Dir 
                            for Dir in Dirs
                            if (not Dir.startswith(".")
                                and Dir not in ExcludeFolder)
                                    ]

                        DllCount = 0
                        EXECount = 0

                        for File in Files:

                            if File.endswith(".exe"):
                                EXECount += 1

                            elif File.endswith(".dll"):
                                DllCount += 1

                        if EXECount > 5 or DllCount > 20:
                            Dirs.clear()
                            continue

                        for File in Files:

                            if File.endswith(".py"):
                                FilePath = os.path.join(
                                                        Root,
                                                        File
                                                        )
                                
                                FileIndex[File] = FilePath
                except:
                    continue

        Drives = [
                    f"{Drive}:/"
                    for Drive in string.ascii_uppercase
                    if os.path.exists(f"{Drive}:/")
                    and Drive != "C"
        ]

        for Drive in  Drives:
            try:
                for Root,Dirs,Files in os.walk(Drive):
                    Dirs[:] = [
                            Dir 
                            for Dir in Dirs
                            if (not Dir.startswith(".")
                                and Dir not in ExcludeFolder)
                        ]

                    DllCount = 0
                    EXECount = 0

                    for File in Files:

                        if File.endswith(".exe"):
                            EXECount += 1

                        elif File.endswith(".dll"):
                            DllCount += 1

                    if EXECount > 5 or DllCount > 20:
                        Dirs.clear()
                        continue

                    for File in Files:
                        if File.endswith(".py"):
                            FilePath = os.path.join(
                                                    Root,
                                                    File
                                                    )
                            
                            FileIndex[File] = FilePath
            except:
                continue

        self.IndexingFinished.emit(FileIndex)

class IconIndexerThread(QThread):
    IndexingFinished = Signal(dict)

    def run(self):
        IconIndex = {}

        UserFolder = os.path.expanduser("~")
        PriorityFolders = [
                            os.path.join(UserFolder, "Desktop"),
                            os.path.join(UserFolder, "Downloads"),
                            os.path.join(UserFolder, "Documents"),
                            os.path.join(UserFolder, "OneDrive")
                            ]

        ExcludeFolder = [
                            "Windows",
                            "Program Files",
                            "Program Files (x86)",
                            "AppData",
                            "__pycache__",
                            "venv",
                            ".git",
                            "node_modules",
                            ".vscode",
                            ".idea",
                            "$RECYCLE.BIN",
                            "System Volume Information",
                            "Temp",
                            "recents",
                            "tmp"
                        ]

        for Folder in PriorityFolders:
            if os.path.exists(Folder):
                try:
                    for Root, Dirs, Files in os.walk(Folder):

                        Dirs[:] = [
                                    Dir
                                    for Dir in Dirs
                                    if (
                                        not Dir.startswith(".")
                                        and Dir not in ExcludeFolder
                                        )
                                    ]

                        for File in Files:
                            if File.endswith(".ico"):
                                FilePath = os.path.join(
                                                        Root,
                                                        File
                                                        )

                                IconIndex[File] = FilePath

                except:
                    continue

        CUsersPath = "C:/Users"

        if os.path.exists(CUsersPath):
            try:
                for Root, Dirs, Files in os.walk(CUsersPath):
                    Dirs[:] = [
                                Dir
                                for Dir in Dirs
                                if (
                                    not Dir.startswith(".")
                                    and Dir not in ExcludeFolder
                                    )
                                ]

                    for File in Files:
                        if File.endswith(".ico"):
                            FilePath = os.path.join(
                                                    Root,
                                                    File
                                                    )

                            IconIndex[File] = FilePath

            except:
                pass

        Drives = [
                    f"{Drive}:/"
                    for Drive in string.ascii_uppercase
                    if os.path.exists(f"{Drive}:/")
                    and Drive not in ["A", "B", "C"]
                ]

        for Drive in Drives:
            try:
                for Root, Dirs, Files in os.walk(Drive):

                    Dirs[:] = [
                                Dir
                                for Dir in Dirs
                                if not Dir.startswith(".")
                                ]

                    for File in Files:

                        if File.endswith(".ico"):

                            FilePath = os.path.join(
                                                    Root,
                                                    File
                                                    )

                            IconIndex[File] = FilePath

            except:
                continue

        self.IndexingFinished.emit(IconIndex)

class BuildThread(QThread):

    ProgressChanged = Signal(int)
    BuildFinished = Signal()

    ProgressChanged = Signal(int)
    BuildFinished = Signal()

    def __init__(self,Command,ShowTerminal,SaveLocation,AppName):
        super().__init__()

        self.command = Command
        self.ShowTerminal = ShowTerminal
        self.SaveLocation = SaveLocation
        self.AppName = AppName

        self.CancelRequested = False
        self.CurrentProgress = 10

    def CancelBuild(self):
        self.CancelRequested = True

    def run(self):

        if self.ShowTerminal:
            self.ProgressChanged.emit(10)

            self.ProgressChanged.emit(10)

            Process = subprocess.Popen(
                                            self.command,
                                            creationflags=subprocess.CREATE_NEW_CONSOLE
                                        )

            while Process.poll() is None:

                if self.CancelRequested:
                                Process.kill()
                                ReturnCode = -1
                                break
                
                if self.CurrentProgress < 95:
                    self.CurrentProgress += 1

                self.ProgressChanged.emit(self.CurrentProgress)
                time.sleep(2)

            ReturnCode = Process.wait()

        else:
            Process = subprocess.Popen(
                                        self.command,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.STDOUT,
                                        text=True
                                    )
            
            for Line in Process.stdout:

                if self.CancelRequested:
                    Process.kill()
                    ReturnCode = -1
                    break

                print(Line.strip())

                if "wrote" in Line:
                    self.ProgressChanged.emit(5)

                elif "Module search paths" in Line:
                    self.ProgressChanged.emit(10)

                elif "checking Analysis" in Line:
                    self.ProgressChanged.emit(15)

                elif "Building Analysis" in Line:
                    self.ProgressChanged.emit(20)

                elif "Analyzing modules" in Line:
                    self.ProgressChanged.emit(25)

                elif "Processing standard module hook" in Line:
                    self.ProgressChanged.emit(30)

                elif "Processing pre-find-module-path hook" in Line:
                    self.ProgressChanged.emit(35)

                elif "Processing pre-safe-import-module hook" in Line:
                    self.ProgressChanged.emit(40)

                elif "Looking for Python shared library" in Line:
                    self.ProgressChanged.emit(45)

                elif "Looking for dynamic libraries" in Line:
                    self.ProgressChanged.emit(50)

                elif "Looking for ctypes DLLs" in Line:
                    self.ProgressChanged.emit(55)

                elif "Creating base_library.zip" in Line:
                    self.ProgressChanged.emit(60)

                elif "Building PYZ" in Line:
                    self.ProgressChanged.emit(65)

                elif "Building PKG" in Line:
                    self.ProgressChanged.emit(75)

                elif "Bootloader" in Line:
                    self.ProgressChanged.emit(85)

                elif "Building EXE" in Line:
                    self.ProgressChanged.emit(95)

                elif "Build complete!" in Line:
                    self.ProgressChanged.emit(100)

            if not self.CancelRequested:
                ReturnCode = Process.wait()

        AppName = self.AppName
        Dist = self.SaveLocation
        ParentBuildFolder = os.path.join(os.getcwd(),"build")
        SpecFile = os.path.join(os.getcwd(),f"{AppName}.spec")
        VersionFile = os.path.join(os.getcwd(),"version_info.txt")

        def RemoveReadOnly(Function, Path, ExcInfo):
            try:
                os.chmod(Path, 0o777)
                Function(Path)
            except:
                pass

        if ReturnCode != 0:
            
            if os.path.exists(ParentBuildFolder):

                try:
                    shutil.rmtree(
                                    ParentBuildFolder,
                                    onerror=RemoveReadOnly
                                )

                except:
                    pass

            if os.path.exists(SpecFile):
                os.remove(SpecFile)

            # if os.path.exists(Dist):
            #     shutil.rmtree(Dist, ignore_errors=True)

            if os.path.exists(VersionFile):

                for _ in range(5):

                    try:
                        if os.path.exists(VersionFile):
                            os.chmod(VersionFile, 0o777)
                            os.remove(VersionFile)
                            print("Version file deleted")
                            
                    except Exception as Error:
                        print("Delete failed:", Error)

            self.BuildFinished.emit()
            return

        if ReturnCode == 0:
            print("RETURN CODE =", ReturnCode)
            print("COMMAND =", " ".join(self.command))
            print("SAVE LOCATION =", self.SaveLocation)
            if os.path.exists(ParentBuildFolder):

                try:
                    shutil.rmtree(
                                    ParentBuildFolder,
                                    onerror=RemoveReadOnly
                                )

                except:
                    pass

            if os.path.exists(SpecFile):
                os.remove(SpecFile)

            # if os.path.exists(Dist):
            #     shutil.rmtree(Dist, ignore_errors=True)
                print("Deleting:", Dist)

            if os.path.exists(VersionFile):

                for _ in range(5):

                    try:
                        if os.path.exists(VersionFile):
                            os.chmod(VersionFile, 0o777)
                            os.remove(VersionFile)
                            print("Version file deleted")

                    except Exception as Error:
                        print("Delete failed:", Error)

        print("RETURN CODE =", ReturnCode)

        if ReturnCode == 0:
            self.ProgressChanged.emit(100)
            self.BuildFinished.emit()
            QThread.msleep(500)

        else:
            print("BUILD FAILED")

class AssetsPath:
    CopyIcon = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/Calculator/COPY ICON.svg"
    RemoveIcon = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/REMOVE.svg"
    Checked = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/TODO App/Check.png"
    Unchecked = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/RADIO_BUTTON_UNCHECKED.svg"
    RadioChecked = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/RADIO_BUTTON_CHECKED.svg"
    Loader = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/LOADER.gif"
    MenuIcon = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/Menu.svg"
    ApplicationIcon = "C:/Users/Lenovo/OneDrive/Desktop/WORK/Upcoming Tools Idea/Python/App Builder/APP_BUILDER_ICON.ico"
    AddStartMenuShortcutPath = "C:/Users/Lenovo/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/ROBIN Apps"


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

class Messages:
    @staticmethod
    def confirmReset(parent):
        Message = QMessageBox(parent)
        Message.setWindowTitle("Reset Application")
        Message.setText("Do You Reeally  Wan't to Cancel ? \nThis Cancel Makes Everything Get Reset")
        Message.setIcon(QMessageBox.Question)
        Message.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Message.setStandardButtons(QMessageBox.Yes |QMessageBox.No)
        return Message.exec()

    @staticmethod
    def settingsSaved(parent):
        Message = QMessageBox(parent)
        Message.setWindowTitle("Settings Saved")
        Message.setText("Verification settings saved successfully.")
        Message.setIcon(QMessageBox.Information)
        Message.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Message.exec()

    @staticmethod
    def saveError(parent,error):
        Message = QMessageBox(parent)
        Message.setWindowTitle("Save Error")
        Message.setText(error)
        Message.setIcon(QMessageBox.Critical)
        Message.setWindowIcon(QIcon(AssetsPath.ApplicationIcon))
        Message.exec()

    @staticmethod
    def EmptyIcon(parent,UserName):
        Message = QMessageBox(parent)
        Message.setWindowTitle("Icon Missing")
        Message.setText("No icon file selected.\n\nYour application will use the default Windows icon.\n\nDo you want to continue anyway?")
        Message.setIcon(QMessageBox.Question)
        Message.setStandardButtons(QMessageBox.Yes |QMessageBox.No)
        return Message.exec()
    
    @staticmethod
    def CreateFolderQuestion(parent,Path):
        Message = QMessageBox(parent)
        Message.setWindowTitle("Folder Not Found")
        Message.setText(f"The folder does not exist.\n\n"f"{Path}\n\n"f"Do you want to create it?")
        Message.setIcon(QMessageBox.Question)
        Message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return Message.exec()

if __name__ == "__main__":
    ConvertPyToExe()