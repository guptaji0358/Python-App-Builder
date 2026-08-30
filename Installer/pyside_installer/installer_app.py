"""Custom PySide6-based installer UI for Pywix.

Replaces Inno Setup's native wizard chrome with a themed Qt wizard that
mirrors the target app's own look: a step sidebar, gradient accents, and a
live-progress install page. It copies the already-built app payload
(out/Pywix when run from source, or the bundled 'payload' folder
when frozen by PyInstaller) into the chosen install directory, optionally
creates shortcuts, then launches the installed app with --post-install so
the app's own fireworks "thank you" screen (scripts/post_install.py) plays.
"""

import os
import sys
import shutil

from PySide6.QtWidgets import (
    QApplication, QWizard, QWizardPage, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QCheckBox, QProgressBar, QFileDialog, QFrame,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QThread, Signal, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QIcon

from installer_style import WizardStyle

APP_DISPLAY_NAME = "Pywix"
APP_EXE_NAME = "Pywix.exe"

STEP_NAMES = ["Welcome", "Location", "Options", "Install", "Finish"]


def BaseDir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def PayloadDir():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "payload")
    return os.path.join(BaseDir(), "out", "Pywix")


def AppIconPath():
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "Assets", "APP_BUILDER_ICON.ico")
    return os.path.join(BaseDir(), "Assets", "APP_BUILDER_ICON.ico")


def DefaultInstallDir():
    ProgramFiles = os.environ.get("ProgramFiles", "C:\\Program Files")
    return os.path.join(ProgramFiles, APP_DISPLAY_NAME)


# --------------------------------------------------------------------------
# Shared chrome: a step sidebar every page embeds itself alongside, so the
# wizard reads as one connected product instead of stock QWizard pages.
# --------------------------------------------------------------------------

class Sidebar(QFrame):
    def __init__(self, ActiveIndex):
        super().__init__()
        self.setObjectName("Sidebar")
        self.setFixedWidth(190)

        Layout = QVBoxLayout()
        Layout.setContentsMargins(24, 28, 20, 24)
        Layout.setSpacing(18)

        Brand = QLabel(APP_DISPLAY_NAME)
        Brand.setObjectName("SidebarBrand")
        Brand.setWordWrap(True)
        Layout.addWidget(Brand)

        Rule = QFrame()
        Rule.setObjectName("HeaderRule")
        Layout.addWidget(Rule)
        Layout.addSpacing(6)

        for Index, Name in enumerate(STEP_NAMES):
            if Index < ActiveIndex:
                Text, ObjectName = f"\u2713  {Name}", "SidebarStepDone"
            elif Index == ActiveIndex:
                Text, ObjectName = f"\u25B8  {Name}", "SidebarStepActive"
            else:
                Text, ObjectName = f"    {Name}", "SidebarStep"
            StepLabel = QLabel(Text)
            StepLabel.setObjectName(ObjectName)
            Layout.addWidget(StepLabel)

        Layout.addStretch()
        self.setLayout(Layout)


def PageShell(ActiveIndex, ContentWidget):
    """Wraps a page's own content widget with the shared sidebar."""
    Root = QHBoxLayout()
    Root.setContentsMargins(0, 0, 0, 0)
    Root.setSpacing(0)
    Root.addWidget(Sidebar(ActiveIndex))
    ContentWidget.setContentsMargins(0, 0, 0, 0)
    Root.addWidget(ContentWidget, stretch=1)
    return Root


class CopyWorker(QThread):
    Progress = Signal(int, int, str)
    Finished = Signal(bool, str)

    def __init__(self, SourceDir, DestDir):
        super().__init__()
        self.SourceDir = SourceDir
        self.DestDir = DestDir

    def run(self):
        try:
            AllFiles = []
            for Root, _Dirs, Files in os.walk(self.SourceDir):
                for FileName in Files:
                    AllFiles.append(os.path.join(Root, FileName))

            Total = max(1, len(AllFiles))
            os.makedirs(self.DestDir, exist_ok=True)

            for Index, SourcePath in enumerate(AllFiles, start=1):
                RelativePath = os.path.relpath(SourcePath, self.SourceDir)
                DestPath = os.path.join(self.DestDir, RelativePath)
                os.makedirs(os.path.dirname(DestPath), exist_ok=True)
                shutil.copy2(SourcePath, DestPath)
                self.Progress.emit(Index, Total, RelativePath)

            self.Finished.emit(True, "")
        except OSError as Error:
            self.Finished.emit(False, str(Error))


class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()

        Content = QFrame()
        Layout = QVBoxLayout()
        Layout.setContentsMargins(48, 48, 48, 40)
        Layout.setSpacing(16)

        IconCircle = QFrame()
        IconCircle.setObjectName("IconCircle")
        IconCircle.setFixedSize(68, 68)
        Layout.addWidget(IconCircle, alignment=Qt.AlignLeft)

        Badge = QLabel("SETUP WIZARD")
        Badge.setObjectName("BadgeLabel")
        Layout.addWidget(Badge)

        Title = QLabel(f"Welcome to {APP_DISPLAY_NAME}")
        Title.setObjectName("TitleLabel")
        Title.setWordWrap(True)
        Layout.addWidget(Title)

        Body = QLabel(
            "This wizard installs everything you need to turn Python "
            "scripts into standalone Windows .exe files — no PyInstaller "
            "command line required."
        )
        Body.setObjectName("SubLabel")
        Body.setWordWrap(True)
        Layout.addWidget(Body)

        Layout.addSpacing(8)
        for Line in (
            "\u2022  Point-and-click .exe builds, no terminal needed",
            "\u2022  Light, Dark, and Developer themes built in",
            "\u2022  Optional desktop and Start Menu shortcuts",
        ):
            FeatureLabel = QLabel(Line)
            FeatureLabel.setObjectName("SubLabel")
            Layout.addWidget(FeatureLabel)

        Layout.addStretch()
        Content.setLayout(Layout)

        self.setLayout(PageShell(0, Content))


class LocationPage(QWizardPage):
    def __init__(self):
        super().__init__()

        Content = QFrame()
        Layout = QVBoxLayout()
        Layout.setContentsMargins(48, 40, 48, 40)
        Layout.setSpacing(14)

        Badge = QLabel("STEP 2 OF 4")
        Badge.setObjectName("BadgeLabel")
        Layout.addWidget(Badge)

        Title = QLabel("Choose Install Location")
        Title.setObjectName("TitleLabel")
        Layout.addWidget(Title)

        Label = QLabel(f"Setup will install {APP_DISPLAY_NAME} in the following folder.")
        Label.setObjectName("SubLabel")
        Label.setWordWrap(True)
        Layout.addWidget(Label)

        Layout.addSpacing(10)
        Row = QHBoxLayout()
        self.PathInput = QLineEdit(DefaultInstallDir())
        BrowseButton = QPushButton("Browse...")
        BrowseButton.clicked.connect(self.BrowseForFolder)
        Row.addWidget(self.PathInput)
        Row.addWidget(BrowseButton)
        Layout.addLayout(Row)

        Layout.addStretch()
        Content.setLayout(Layout)

        self.setLayout(PageShell(1, Content))
        self.registerField("InstallDir*", self.PathInput)

    def BrowseForFolder(self):
        Chosen = QFileDialog.getExistingDirectory(self, "Choose Install Folder", self.PathInput.text())
        if Chosen:
            self.PathInput.setText(os.path.join(Chosen, APP_DISPLAY_NAME))


class OptionsPage(QWizardPage):
    def __init__(self):
        super().__init__()

        Content = QFrame()
        Layout = QVBoxLayout()
        Layout.setContentsMargins(48, 40, 48, 40)
        Layout.setSpacing(14)

        Badge = QLabel("STEP 3 OF 4")
        Badge.setObjectName("BadgeLabel")
        Layout.addWidget(Badge)

        Title = QLabel("Additional Options")
        Title.setObjectName("TitleLabel")
        Layout.addWidget(Title)

        Label = QLabel("Select the shortcuts you'd like Setup to create.")
        Label.setObjectName("SubLabel")
        Label.setWordWrap(True)
        Layout.addWidget(Label)

        Layout.addSpacing(10)
        self.DesktopShortcutCheckbox = QCheckBox("Create a desktop shortcut")
        self.StartMenuShortcutCheckbox = QCheckBox("Create a Start Menu shortcut")
        self.StartMenuShortcutCheckbox.setChecked(True)
        Layout.addWidget(self.DesktopShortcutCheckbox)
        Layout.addWidget(self.StartMenuShortcutCheckbox)

        Layout.addStretch()
        Content.setLayout(Layout)

        self.setLayout(PageShell(2, Content))
        self.registerField("DesktopShortcut", self.DesktopShortcutCheckbox)
        self.registerField("StartMenuShortcut", self.StartMenuShortcutCheckbox)


class ChecklistRow(QLabel):
    def __init__(self, Text):
        super().__init__(f"\u25CB  {Text}")
        self.BaseText = Text
        self.setObjectName("ChecklistItem")

    def MarkDone(self):
        self.setText(f"\u2713  {self.BaseText}")
        self.setObjectName("ChecklistItemDone")
        self.style().unpolish(self)
        self.style().polish(self)


class InstallPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.Worker = None
        self.Done = False
        self.ShortcutsApplied = False

        Content = QFrame()
        Layout = QVBoxLayout()
        Layout.setContentsMargins(48, 40, 48, 40)
        Layout.setSpacing(14)

        Badge = QLabel("STEP 4 OF 4")
        Badge.setObjectName("BadgeLabel")
        Layout.addWidget(Badge)

        Title = QLabel("Installing")
        Title.setObjectName("TitleLabel")
        Layout.addWidget(Title)

        Layout.addSpacing(6)
        self.PercentLabel = QLabel("0%")
        self.PercentLabel.setObjectName("BigPercent")
        Layout.addWidget(self.PercentLabel)

        self.ProgressBar = QProgressBar()
        self.ProgressBar.setRange(0, 100)
        self.ProgressBar.setTextVisible(False)
        Layout.addWidget(self.ProgressBar)

        self.StatusLine = QLabel("Preparing...")
        self.StatusLine.setObjectName("StatusLine")
        self.StatusLine.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        Layout.addWidget(self.StatusLine)

        Layout.addSpacing(16)
        self.CopyRow = ChecklistRow("Copy application files")
        self.ShortcutRow = ChecklistRow("Create shortcuts")
        self.FinalizeRow = ChecklistRow("Finalize installation")
        Layout.addWidget(self.CopyRow)
        Layout.addWidget(self.ShortcutRow)
        Layout.addWidget(self.FinalizeRow)

        Layout.addStretch()
        Content.setLayout(Layout)

        self.setLayout(PageShell(3, Content))

        self.Animation = QPropertyAnimation(self.ProgressBar, b"value")
        self.Animation.setEasingCurve(QEasingCurve.OutCubic)
        self.Animation.setDuration(180)

    def initializePage(self):
        self.Done = False
        SourceDir = PayloadDir()
        DestDir = self.field("InstallDir")

        if not os.path.isdir(SourceDir):
            self.StatusLine.setText(f"Error: build payload not found at {SourceDir}")
            return

        self.Worker = CopyWorker(SourceDir, DestDir)
        self.Worker.Progress.connect(self.OnProgress)
        self.Worker.Finished.connect(self.OnCopyFinished)
        self.Worker.start()

    def AnimateTo(self, Value):
        self.Animation.stop()
        self.Animation.setStartValue(self.ProgressBar.value())
        self.Animation.setEndValue(Value)
        self.Animation.start()
        self.PercentLabel.setText(f"{Value}%")

    def OnProgress(self, Index, Total, RelativePath):
        Percent = int((Index / Total) * 85)
        self.AnimateTo(Percent)
        self.StatusLine.setText(f"Copying {RelativePath}")

    def OnCopyFinished(self, Success, ErrorMessage):
        if not Success:
            self.StatusLine.setText(f"Installation failed: {ErrorMessage}")
            return

        self.CopyRow.MarkDone()
        self.AnimateTo(90)
        self.StatusLine.setText("Creating shortcuts...")

        DestDir = self.field("InstallDir")
        ExePath = os.path.join(DestDir, APP_EXE_NAME)
        if self.field("DesktopShortcut"):
            CreateShortcut(ExePath, DesktopFolder())
        if self.field("StartMenuShortcut"):
            CreateShortcut(ExePath, StartMenuFolder())

        self.ShortcutRow.MarkDone()
        self.AnimateTo(100)
        self.StatusLine.setText("Installation complete.")
        self.FinalizeRow.MarkDone()

        self.Done = True
        self.completeChanged.emit()

    def isComplete(self):
        return self.Done


class FinishPage(QWizardPage):
    def __init__(self):
        super().__init__()

        Content = QFrame()
        Layout = QVBoxLayout()
        Layout.setContentsMargins(48, 48, 48, 40)
        Layout.setSpacing(16)

        IconCircle = QFrame()
        IconCircle.setObjectName("IconCircle")
        IconCircle.setFixedSize(68, 68)
        Layout.addWidget(IconCircle, alignment=Qt.AlignLeft)

        Badge = QLabel("ALL DONE")
        Badge.setObjectName("BadgeLabel")
        Layout.addWidget(Badge)

        Title = QLabel(f"{APP_DISPLAY_NAME} is ready")
        Title.setObjectName("TitleLabel")
        Title.setWordWrap(True)
        Layout.addWidget(Title)

        Body = QLabel("Setup has finished installing it on your computer.")
        Body.setObjectName("SubLabel")
        Body.setWordWrap(True)
        Layout.addWidget(Body)

        Layout.addSpacing(10)
        self.LaunchCheckbox = QCheckBox(f"Launch {APP_DISPLAY_NAME}")
        self.LaunchCheckbox.setChecked(True)
        Layout.addWidget(self.LaunchCheckbox)

        Layout.addStretch()
        Content.setLayout(Layout)

        self.setLayout(PageShell(4, Content))
        self.registerField("LaunchApp", self.LaunchCheckbox)


def DesktopFolder():
    return os.path.join(os.path.expanduser("~"), "Desktop")


def StartMenuFolder():
    AppData = os.environ.get("APPDATA", "")
    return os.path.join(AppData, "Microsoft", "Windows", "Start Menu", "Programs")


def CreateShortcut(ExePath, FolderPath):
    try:
        from win32com.client import Dispatch
        os.makedirs(FolderPath, exist_ok=True)
        ShortcutPath = os.path.join(FolderPath, f"{APP_DISPLAY_NAME}.lnk")
        Shell = Dispatch("WScript.Shell")
        Shortcut = Shell.CreateShortCut(ShortcutPath)
        Shortcut.TargetPath = ExePath
        Shortcut.WorkingDirectory = os.path.dirname(ExePath)
        Shortcut.IconLocation = ExePath
        Shortcut.save()
    except Exception:
        pass


class InstallerWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_DISPLAY_NAME} Setup")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setStyleSheet(WizardStyle)
        self.setOption(QWizard.NoBackButtonOnLastPage, True)
        self.setMinimumSize(680, 460)

        IconPath = AppIconPath()
        if os.path.exists(IconPath):
            self.setWindowIcon(QIcon(IconPath))

        self.addPage(WelcomePage())
        self.addPage(LocationPage())
        self.addPage(OptionsPage())
        self.InstallPageRef = InstallPage()
        self.addPage(self.InstallPageRef)
        self.FinishPageRef = FinishPage()
        self.addPage(self.FinishPageRef)

        self.finished.connect(self.OnWizardFinished)

    def OnWizardFinished(self, Result):
        if Result != QWizard.Accepted:
            return

        InstallDir = self.field("InstallDir")
        ExePath = os.path.join(InstallDir, APP_EXE_NAME)

        if self.field("LaunchApp") and os.path.exists(ExePath):
            os.startfile(ExePath, arguments="--post-install")  # noqa: S606 - user-chosen local exe just installed


def main():
    App = QApplication(sys.argv)
    Wizard = InstallerWizard()
    Wizard.show()
    sys.exit(App.exec())


if __name__ == "__main__":
    main()
