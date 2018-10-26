import run
import PhotoScan
from PySide2 import QtGui, QtCore, QtWidgets

PACH_DB = r'C:\projectTree\database.db'
SETTING_PC = 'PC1'

class MainGui(QtWidgets.QDialog):

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowTitle("Автоматическая обработка:")

        self.btnStart = QtWidgets.QPushButton("Старт")
        self.btnStart.setFixedSize(100, 50)

        self.btnStop = QtWidgets.QPushButton("Стоп")
        self.btnStop.setFixedSize(100, 50)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btnStart)
        hbox.addWidget(self.btnStop)

        self.setLayout(hbox)
        self.resize(100, 100)

        QtCore.QObject.connect(self.btnStart, QtCore.SIGNAL("clicked()"), self.StartProcess)
        QtCore.QObject.connect(self.btnStop, QtCore.SIGNAL("clicked()"), self.StopProcess)
        self.exec()

    def StartProcess(self):
        print('старт')
        self.ThreadProcess = run.PhotoscanProcessing(PACH_DB, SETTING_PC)
        self.ThreadProcess.start()

    def StopProcess(self):
        print("Стоп")
        self.ThreadProcess.processingStatus = False

    def __del__(self):
        self.ThreadProcess.processingStatus = False


def main():
    doc = PhotoScan.app.document
    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()
    dlg = MainGui(parent)

label = "Автоматическая обработка/Меню"
PhotoScan.app.addMenuItem(label, main)
print("To execute this script press {}".format(label))
