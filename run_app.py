# This Python file uses the following encoding: utf-8

# step 1: generate ui-form
# pyside6-uic form.ui > ui_form.py

# wrap the program in exe or app
# pyinstaller --windowed --onefile --clean --noconfirm main.py
# pyinstaller --clean --noconfirm --windowed --onefile main_ui.spec


import sys
import os
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from gui.ui_form import Ui_UI_GUI

from utils.TIFtoPNG import tif2png


def checkArguments(inputFilePath, outputFilePath, in_type, out_type):

    if Path(inputFilePath).suffix == in_type and Path(outputFilePath).suffix == out_type:
        return True
    elif not Path(inputFilePath).suffix == in_type:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setWindowTitle("Input Error")
        msg.setText("Data Format mismatch!")
        msg.exec()

    elif not Path(outputFilePath).suffix == out_type:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setWindowTitle("Output Error")
        msg.setText("Data Format mismatch!")
        msg.exec()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Error")
        msg.setText("Can not find files!")
        msg.exec()

    return False


def popupMsg(title_msg):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle(title_msg)
    msg.setText("Task Finished!")
    msg.exec()


class Ui_APP(QMainWindow):
    def __init__(self):
        super(Ui_APP, self).__init__()
        self.ui = Ui_UI_GUI()
        self.ui.setupUi(self)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        # convert
        self.ui.pushButtonRun.clicked.connect(self.convert)
        self.ui.toolButtonTIF.clicked.connect(self.browseTIFfile)
        self.ui.toolButtonPNG.clicked.connect(self.browsePNGfiledir)
        # resize
        self.ui.toolButton_InputPNG.clicked.connect(self.browseInputPNGfile)
        self.ui.toolButton_OutputPNG.clicked.connect(self.browseOutputPNGDir)
        self.ui.pushButtonRun_Resize.clicked.connect(self.resizeImage)
        # invert BW
        self.ui.toolButton_InputMask.clicked.connect(self.browseInputMaskfile)
        self.ui.toolButton_OutputMask.clicked.connect(self.browseOutputMaskDir)
        self.ui.pushButtonRun_InvertMask.clicked.connect(self.invertMask)

    def convert(self):
        # print("Convert button pressed")
        inputFilePath = self.ui.lineEditTIF.text()
        outputFilePath = self.ui.lineEditPNG.text()
        # print(f"[Input: ] {inputFilePath}.")
        # print(f"[Target:] {outputFilePath}")
        if checkArguments(inputFilePath, outputFilePath, '.tif', '.png'):
            dst_ds = tif2png(inputFilePath, outputFilePath)
            # print(f"[Output:] {dst_ds}")
        popupMsg(title_msg="TIF to PNG")

    def resizeImage(self):
        from utils.resizePNG import resizePNG
        inputFilePath = self.ui.lineEdit_InputPNG.text()
        outputFilePath = self.ui.lineEdit_OutputPNG.text()
        scale = self.ui.horizontalSlider.value()
        print(f"[Input: ] {inputFilePath}.")
        print(f"[Target:] {outputFilePath}")
        print(f"[Scale:] {scale}")
        if checkArguments(inputFilePath, outputFilePath, '.png', '.png'):
            resizePNG(inputFilePath, outputFilePath, scale_percent=scale)

        popupMsg(title_msg="PNG to PNG: Resize")

    def invertMask(self):
        from utils.invertBW import invertBW

        inputFilePath = self.ui.lineEdit_InputMask.text()
        outputFilePath = self.ui.lineEdit_OutputMask.text()
        if checkArguments(inputFilePath, outputFilePath, '.png',  '.png'):
            invertBW(inputFilePath, outputFilePath)
        popupMsg(title_msg="PNG to PNG: Mask Invert")

    def cancel(self):
        self.close()
        # print("Cancel button pressed")

    def browseTIFfile(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "TIF Files (*.tif)",
            options=options)
        if fileName:
            self.ui.lineEditTIF.setText(fileName)
        # print("Browse file for tif")

    def browsePNGfiledir(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        inputFilePath = self.ui.lineEditTIF.text()

        fileDir = QFileDialog.getExistingDirectory(
            self,
            "Open a Folder",
            "../data/",
            options=options)
        if fileDir:
            file_name = Path(inputFilePath).stem + '.png'
            self.ui.lineEditPNG.setText(fileDir + "/" + file_name)
        # print("Browse file for PNG")

    def browseInputPNGfile(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "PNG Files (*.png)",
            options=options)
        if fileName:
            self.ui.lineEdit_InputPNG.setText(fileName)
        # print("Browse file for tif")

    def browseOutputPNGDir(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        inputFilePath = self.ui.lineEdit_InputPNG.text()
        scale = self.ui.horizontalSlider.value()
        fileDir = QFileDialog.getExistingDirectory(
            self,
            "Open a Folder",
            "../data/",
            options=options)
        if fileDir:
            file_name = Path(inputFilePath).stem + str(scale)+'p.png'
            self.ui.lineEdit_OutputPNG.setText(fileDir + "/" + file_name)

    def browseInputMaskfile(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            None,
            "QFileDialog.getOpenFileName()",
            "",
            "PNG Files (*.png)",
            options=options)
        if fileName:
            self.ui.lineEdit_InputMask.setText(fileName)
        # print("Browse file for tif")

    def browseOutputMaskDir(self):
        ''' Called when the user presses the Browse button
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        inputFilePath = self.ui.lineEdit_InputMask.text()
        fileDir = QFileDialog.getExistingDirectory(
            self,
            "Open a Folder",
            "../data/",
            options=options)
        if fileDir:
            file_name = Path(inputFilePath).stem + '.invert.png'
            self.ui.lineEdit_OutputMask.setText(fileDir + "/" + file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = Ui_APP()
    GUI.show()
    sys.exit(app.exec())
