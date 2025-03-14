# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

import http.client
import json
import logging
import math
import os
import sys
import requests
import tempfile
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
import time

from LoadWindow import LoadWindow
from downloadHelper import DownloadHelper

http.client.HTTPConnection.debuglevel = 1

requestURL = "https://anisongdb.com/api/search_request"
random50URL = "https://anisongdb.com/api/get_50_random_songs"
session = requests.session()

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Content-Type": "application/json",
}
logFile = os.path.join(tempfile.gettempdir(
), "anisongDB-Downloader" + str(time.time()) + ".log")
logging.basicConfig(
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
    filename=logFile
)

requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True


class QEntryItem(QtWidgets.QTableWidgetItem):
    def __init__(self, entry, *__args):
        super(QEntryItem, self).__init__(*__args)
        self.entry = entry


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("AnisongDB Downloader")
        self.setFixedSize(1166, 806)

        self.tableWidget = QtWidgets.QTableWidget(parent=self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 130, 1146, 664))
        self.tableWidget.setVerticalHeaderLabels([])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setColumnWidth(0, 1)
        self.tableWidget.setHorizontalHeaderLabels(
            ["", "ANN ID", "Anime", "Type", "Song Name", "Artist", "Diff."])
        self.tableWidget.itemChanged.connect(self.entryClicked)
        self.tableWidget.setObjectName("tableWidget")

        self.lineEdit = QtWidgets.QLineEdit(parent=self)
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 785, 21))
        self.lineEdit.setPlaceholderText("Search by anime...")
        self.lineEdit.returnPressed.connect(self.searchButton)
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 40, 785, 21))
        self.lineEdit_2.setPlaceholderText("Search by song name...")
        self.lineEdit_2.returnPressed.connect(self.searchButton)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_3.setGeometry(QtCore.QRect(10, 70, 785, 21))
        self.lineEdit_3.setPlaceholderText("Search by artist...")
        self.lineEdit_3.returnPressed.connect(self.searchButton)
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 100, 474, 21))
        self.lineEdit_4.setPlaceholderText("Search by composer...")
        self.lineEdit_4.returnPressed.connect(self.searchButton)
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.checkBox = QtWidgets.QCheckBox(parent=self)
        self.checkBox.setGeometry(QtCore.QRect(804, 10, 101, 21))
        self.checkBox.setText("Partial Match")
        self.checkBox.setChecked(True)
        self.checkBox.setToolTip(
            "If activated, results only have to contain the filter and not match it exactly")
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_2.setGeometry(QtCore.QRect(804, 40, 101, 21))
        self.checkBox_2.setText("Partial Match")
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setToolTip(
            "If activated, results only have to contain the filter and not match it exactly")
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_3.setGeometry(QtCore.QRect(804, 70, 101, 21))
        self.checkBox_3.setText("Partial Match")
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setToolTip(
            "If activated, results only have to contain the filter and not match it exactly")
        self.checkBox_3.setObjectName("checkBox_3")

        self.checkBox_4 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_4.setGeometry(QtCore.QRect(492, 100, 101, 21))
        self.checkBox_4.setText("Partial Match")
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setToolTip(
            "If activated, results only have to contain the filter and not match it exactly")
        self.checkBox_4.setObjectName("checkBox_4")

        self.checkBox_5 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_5.setGeometry(QtCore.QRect(904, 10, 41, 21))
        self.checkBox_5.setText("OP")
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setToolTip("Whether to search for opening songs")
        self.checkBox_5.setObjectName("checkBox_5")

        self.checkBox_6 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_6.setGeometry(QtCore.QRect(904, 40, 40, 21))
        self.checkBox_6.setText("ED")
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setToolTip("Whether to search for ending songs")
        self.checkBox_6.setObjectName("checkBox_6")

        self.checkBox_7 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_7.setGeometry(QtCore.QRect(904, 70, 50, 21))
        self.checkBox_7.setText("INS")
        self.checkBox_7.setChecked(True)
        self.checkBox_7.setToolTip("Whether to search for insert songs")
        self.checkBox_7.setObjectName("checkBox_7")

        self.checkBox_8 = QtWidgets.QCheckBox(parent=self)
        self.checkBox_8.setGeometry(QtCore.QRect(594, 100, 121, 21))
        self.checkBox_8.setText("Ignore duplicates")
        self.checkBox_8.setChecked(True)
        self.checkBox_8.setToolTip(
            "This will ignore duplicates and only take into account the first instance of [Song Name by Artist] that it has encountered. (Different sets of artists are not considered duplicates)")
        self.checkBox_8.setObjectName("checkBox_8")

        self.pushButton = QtWidgets.QPushButton(parent=self)
        self.pushButton.setGeometry(QtCore.QRect(1074, 10, 81, 25))
        self.pushButton.setText("Search")
        self.pushButton.clicked.connect(self.searchButton)
        self.pushButton.setToolTip("")
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(parent=self)
        self.pushButton_2.setGeometry(QtCore.QRect(964, 40, 191, 25))
        self.pushButton_2.setText("Download (MP3)")
        self.pushButton_2.clicked.connect(self.downloadMP3)
        self.pushButton_2.setToolTip(
            "Download the selected songs as MP3 files")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(parent=self)
        self.pushButton_3.setGeometry(QtCore.QRect(1061, 70, 94, 25))
        self.pushButton_3.setText("Download (SD)")
        self.pushButton_3.clicked.connect(self.downloadSD)
        self.pushButton_3.setToolTip(
            "Download the selected songs as videos of the lowest quality available")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(parent=self)
        self.pushButton_4.setGeometry(QtCore.QRect(964, 70, 94, 25))
        self.pushButton_4.setText("Download (HD)")
        self.pushButton_4.clicked.connect(self.downloadHD)
        self.pushButton_4.setToolTip(
            "Download the selected songs as videos of the highest quality available")
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(parent=self)
        self.pushButton_5.setGeometry(QtCore.QRect(964, 100, 94, 25))
        self.pushButton_5.setText("Show selection")
        self.pushButton_5.clicked.connect(self.showSelection)
        self.pushButton_5.setToolTip("Show all selected songs in the table")
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = QtWidgets.QPushButton(parent=self)
        self.pushButton_6.setGeometry(QtCore.QRect(1061, 100, 94, 25))
        self.pushButton_6.setText("Reinitialize")
        self.pushButton_6.clicked.connect(self.reinitializeTable)
        self.pushButton_6.setToolTip(
            "Empty the table and deselect all previously selected songs")
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = QtWidgets.QPushButton(parent=self)
        self.pushButton_7.setGeometry(QtCore.QRect(867, 100, 94, 25))
        self.pushButton_7.setText("(De)select all")
        self.pushButton_7.clicked.connect(self.toggleSelection)
        self.pushButton_7.setToolTip(
            "Select/Deselect all songs currently in the table")
        self.pushButton_7.setObjectName("pushButton_7")

        self.comboBox = QtWidgets.QComboBox(parent=self)
        self.comboBox.setGeometry(QtCore.QRect(964, 10, 101, 25))
        self.comboBox.setEditable(False)
        self.comboBox.setCurrentText("")
        self.comboBox.setPlaceholderText("")
        self.comboBox.addItems(["Intersection", "Union"])
        self.comboBox.setToolTip(
            "Define how the filters will be combined together")
        self.comboBox.setObjectName("comboBox")

        self.comboBox_2 = QtWidgets.QComboBox(parent=self)
        self.comboBox_2.setGeometry(QtCore.QRect(809, 100, 50, 25))
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setPlaceholderText("")
        self.comboBox_2.addItems(["eu", "naw", "nae"])
        self.comboBox_2.setToolTip("Catbox host to download from")
        self.comboBox_2.setObjectName("comboBox_2")

        self.comboBox_3 = QtWidgets.QComboBox(parent=self)
        self.comboBox_3.setGeometry(QtCore.QRect(720, 100, 81, 25))
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setCurrentText("")
        self.comboBox_3.setPlaceholderText("")
        self.comboBox_3.addItems(["Japanese", "English"])
        self.comboBox_3.setToolTip("Language to use for the anime title")
        self.comboBox_3.setObjectName("comboBox_3")

        self.lw = LoadWindow(self)
        self.errorWindow = QtWidgets.QErrorMessage()

        self.entryDict = {}
        self.selectedItemsInTable: dict[int, dict] = {}

    def getAnimeField(self):
        return "animeJPName" if self.comboBox_3.currentText() == "Japanese" else "animeENName"

    def showErrorMessage(self, message, type):
        self.errorWindow.showMessage(
            f'{message}\nFor more information, please see the log file "{logFile}"', type)

    def toggleSelection(self):
        try:
            if len(self.selectedItemsInTable) == self.tableWidget.rowCount():
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.item(i, 0).setCheckState(
                        QtCore.Qt.CheckState.Unchecked)
            else:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.item(i, 0).setCheckState(
                        QtCore.Qt.CheckState.Checked)
        except:
            logging.exception("An error has occured while toggling selection.")
            self.showErrorMessage(
                "An error occured while toggling selection.", "toggling")

    def reinitializeTable(self):
        try:
            if self.lw.downloading:
                return

            self.clearTable()
            self.resizeTable()
            self.entryDict = {}
        except:
            logging.exception(
                "An error has occured while reinitializing the table.")
            self.showErrorMessage(
                "An error occured while reinitializing the table.", "reinit")

    def startDownload(self, hd):
        if self.entryDict == {}:
            return
        directory = str(QFileDialog.getExistingDirectory(
            self, "Select download directory"))
        if directory != "":
            dh = DownloadHelper(list(self.entryDict.values()),
                                directory, hd, self.comboBox_2.currentText(),
                                self.getAnimeField())
            self.lw.setDownloadHelper(dh)
            self.lw.show()
            self.lw.downloading = True
            dh.start()

    def downloadHD(self):
        self.startDownload(True)

    def downloadSD(self):
        self.startDownload(False)

    def downloadMP3(self):
        self.startDownload(None)

    def showSelection(self):
        try:
            if self.lw.downloading:
                return

            self.clearTable()
            for songId in self.entryDict:
                self.addEntryToTable(self.entryDict[songId])
            self.resizeTable()
        except:
            logging.exception(
                "An error has occured while showing the selection.")
            self.showErrorMessage(
                "An error occured while showing the selection.", "selection")

    def entryClicked(self, item):
        if not isinstance(item, QEntryItem) or self.lw.downloading:
            return
        if item.checkState() == QtCore.Qt.CheckState.Checked:
            self.entryDict[item.entry["annSongId"]] = item.entry
            self.selectedItemsInTable[item.entry["annSongId"]] = item.entry
        else:
            self.entryDict.pop(item.entry["annSongId"], None)
            self.selectedItemsInTable.pop(item.entry["annSongId"], None)

    def resizeTable(self):
        self.tableWidget.resizeColumnsToContents()
        tableWidth = self.tableWidget.width() - (22 if self.tableWidget.rowCount() > 21 else 0)
        columnsWidth = 0
        for i in range(self.tableWidget.columnCount()):
            columnsWidth += self.tableWidget.horizontalHeader().sectionSize(i)
        scale = tableWidth / columnsWidth
        for i in range(self.tableWidget.columnCount()):
            self.tableWidget.setColumnWidth(i, math.floor(
                self.tableWidget.horizontalHeader().sectionSize(i) * scale))

    def clearTable(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def addEntryToTable(self, entry):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        songId = entry["annSongId"]

        checkbox = QEntryItem(entry)
        checkbox.setFlags(checkbox.flags() |
                          QtCore.Qt.ItemFlag.ItemIsUserCheckable)
        checkbox.setCheckState(
            QtCore.Qt.CheckState.Unchecked if songId not in self.entryDict else QtCore.Qt.CheckState.Checked)

        fields = ["annId", self.getAnimeField(), "songType",
                  "songName", "songArtist", "songDifficulty"]

        self.tableWidget.setItem(row, 0, checkbox)

        for i in range(1, 7):
            item = QtWidgets.QTableWidgetItem(str(entry[fields[i - 1]]))
            item.setFlags(item.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
            self.tableWidget.setItem(row, i, item)

    def searchButton(self):
        try:
            if self.lw.downloading:
                return

            self.selectedItemsInTable = {}

            reqObj = {
                "and_logic": not self.comboBox.currentIndex(),
                "ignore_duplicate": self.checkBox_8.isChecked(),
                "opening_filter": self.checkBox_5.isChecked(),
                "ending_filter": self.checkBox_6.isChecked(),
                "insert_filter": self.checkBox_7.isChecked(),
                "normal_broadcast": True,
                "dub": True,
                "rebroadcast": True,
                "standard": True,
                "instrumental": True,
                "chanting": True,
                "character": True
            }
            if self.lineEdit.text() != "":
                reqObj["anime_search_filter"] = {
                    "search": self.lineEdit.text(),
                    "partial_match": self.checkBox.isChecked()
                }
            if self.lineEdit_2.text() != "":
                reqObj["song_name_search_filter"] = {
                    "search": self.lineEdit_2.text(),
                    "partial_match": self.checkBox_2.isChecked()
                }
            if self.lineEdit_3.text() != "":
                reqObj["artist_search_filter"] = {
                    "search": self.lineEdit_3.text(),
                    "partial_match": self.checkBox_3.isChecked(),
                    "group_granularity": 0,
                    "max_other_artist": 99
                }
            if self.lineEdit_4.text() != "":
                reqObj["composer_search_filter"] = {
                    "search": self.lineEdit_4.text(),
                    "partial_match": self.checkBox_4.isChecked(),
                    "arrangement": True
                }

            x = session.post(requestURL, json=reqObj, headers=headers)
            data = json.loads(x.text)

            self.clearTable()

            for entry in data:
                self.addEntryToTable(entry)

            self.resizeTable()
        except:
            logging.exception("An error has occured while searching.")
            self.showErrorMessage(
                "An error occured while searching.", "searching")


app = QApplication([])

# if condition used to differentiate .exe use and python script use
if getattr(sys, 'frozen', False):
    # sys._MEIPASS is an env variable defined by pyinstaller
    app.setWindowIcon(QtGui.QIcon(
        os.path.join(sys._MEIPASS, "files/logo.png")))
else:
    app.setWindowIcon(QtGui.QIcon('files/logo.png'))

window = MainWindow()
window.show()

app.exec()
