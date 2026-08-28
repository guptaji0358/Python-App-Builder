from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon

from .assets_path import AssetsPath

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

