from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog, QLabel, QProgressBar

from downloadHelper import DownloadHelper

class LoadWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(500, 125)
        self.setWindowTitle("Downloading selection...")

        self.title = QLabel("", self)
        self.title.setWordWrap(True)
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        self.pbar.setGeometry(50, 43, 430, 25)

        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setGeometry(0,0,500,40)

        self.pushButton = QtWidgets.QPushButton(parent=self)
        self.pushButton.setGeometry(210, 85, 80, 25)
        self.pushButton.setText("Cancel")
        self.pushButton.clicked.connect(self.cancelDownload)
        self.pushButton.setToolTip("")
        self.pushButton.setObjectName("pushButton")

        self.downloading = False

        self.downloadHelper = None
        self.cancelling = False

    def hide(self):
        super().hide()
        self.pbar.setValue(0)
        self.downloading = False

    def progressUpdate(self, progress):
        self.pbar.setValue(progress)

    def setDownloadHelper(self, downloadHelper: DownloadHelper):
        self.downloadHelper = downloadHelper
        self.downloadHelper.progressChanged.connect(self.progressUpdate)
        self.downloadHelper.messageChanged.connect(self.setMessage)
        self.downloadHelper.doneSignal.connect(self.hide)
        self.cancelling = False

    def setMessage(self, message):
        self.title.setText(message)

    def cancelDownload(self):
        if not self.cancelling:
            self.cancelling = True
            self.downloadHelper.stop()
            self.downloadHelper.messageChanged.disconnect()
            self.setMessage("Cancelling...")

    def closeEvent(self, a0):
        a0.ignore()
        self.cancelDownload()