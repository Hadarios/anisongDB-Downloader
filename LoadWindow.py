from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QLabel, QProgressBar

from downloadHelper import DownloadHelper

class LoadWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setFixedSize(500, 90)
        self.setWindowTitle("Downloading selection...")

        self.title = QLabel("", self)
        self.title.setWordWrap(True)
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)

        self.pbar.setGeometry(50, 43, 430, 25)

        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setGeometry(0,0,500,40)

        self.downloading = False

        self.downloadHelper = None

    def hide(self):
        super().hide()
        self.pbar.setValue(0)
        self.downloading = False

    def progressUpdate(self, progress):
        self.pbar.setValue(progress)
        if self.pbar.value() == 100:
            self.hide()

    def setDownloadHelper(self, downloadHelper: DownloadHelper):
        self.downloadHelper = downloadHelper
        self.downloadHelper.progressChanged.connect(self.progressUpdate)
        self.downloadHelper.messageChanged.connect(self.setMessage)

    def setMessage(self, message):
        self.title.setText(message)