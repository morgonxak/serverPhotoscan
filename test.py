import PhotoScan
from PySide2 import QtGui, QtCore, QtWidgets

class MaskByColor(QtWidgets.QDialog):

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        self.color = QtGui.QColor(0, 0, 0)
        red, green, blue = self.color.red(), self.color.green(), self.color.blue()

        self.setWindowTitle("Masking by color:")

        self.btnQuit = QtWidgets.QPushButton("Quit")
        self.btnQuit.setFixedSize(100, 50)

        self.btnP1 = QtWidgets.QPushButton("Mask")
        self.btnP1.setFixedSize(100, 50)

        self.pBar = QtWidgets.QProgressBar()
        self.pBar.setTextVisible(False)
        self.pBar.setFixedSize(130, 50)

        self.selTxt = QtWidgets.QLabel()
        self.selTxt.setText("Apply to:")
        self.selTxt.setFixedSize(100, 25)

        self.radioBtn_all = QtWidgets.QRadioButton("all cameras")
        self.radioBtn_sel = QtWidgets.QRadioButton("selected cameras")
        self.radioBtn_all.setChecked(True)
        self.radioBtn_sel.setChecked(False)

        self.colTxt = QtWidgets.QLabel()
        self.colTxt.setText("Select color:")
        self.colTxt.setFixedSize(100, 25)

        strColor = "{:0>2d}{:0>2d}{:0>2d}".format(int(hex(red)[2:]), int(hex(green)[2:]), int(hex(blue)[2:]))
        self.btnCol = QtWidgets.QPushButton(strColor)
        self.btnCol.setFixedSize(80, 25)
        pix = QtGui.QPixmap(10, 10)
        pix.fill(self.color)
        icon = QtGui.QIcon()
        icon.addPixmap(pix)
        self.btnCol.setIcon(icon)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Button, self.color)
        self.btnCol.setPalette(palette)
        self.btnCol.setAutoFillBackground(True)

        self.txtTol = QtWidgets.QLabel()
        self.txtTol.setText("Tolerance:")
        self.txtTol.setFixedSize(100, 25)

        self.sldTol = QtWidgets.QSlider()
        self.sldTol.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.sldTol.setMinimum(0)
        self.sldTol.setMaximum(99)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.pBar)
        hbox.addWidget(self.btnP1)
        hbox.addWidget(self.btnQuit)

        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(self.selTxt, 0, 0)
        layout.addWidget(self.radioBtn_all, 1, 0)
        layout.addWidget(self.radioBtn_sel, 2, 0)
        layout.addWidget(self.colTxt, 0, 1)
        layout.addWidget(self.btnCol, 1, 1)
        layout.addWidget(self.txtTol, 0, 2)
        layout.addWidget(self.sldTol, 1, 2)
        layout.addLayout(hbox, 3, 0, 5, 3)
        self.setLayout(layout)

        proc_mask = lambda: self.maskColor()
        proc_color = lambda: self.changeColor()

        #QtCore.QObject.connect(self.btnP1, QtCore.SIGNAL("clicked()"), proc_mask)
        #QtCore.QObject.connect(self.btnCol, QtCore.SIGNAL("clicked()"), proc_color)
        QtCore.QObject.connect(self.btnQuit, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("reject()"))

        self.exec()

def start():
    doc = PhotoScan.app.document
    app = QtWidgets.QApplication.instance()
    parent = app.activeWindow()
    dlg = MaskByColor(parent)

label = "Custom menu/Masking by color"
PhotoScan.app.addMenuItem(label, start)
print("To execute this script press {}".format(label))