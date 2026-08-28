from PySide6.QtCore import QThread, Signal
import os
import string
import subprocess
import shutil
import time

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

