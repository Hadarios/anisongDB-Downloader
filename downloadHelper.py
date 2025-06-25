import os
import subprocess
import sys
import logging

import eyed3
import requests
from PyQt6.QtCore import QThread, pyqtSignal
from os import path


class DownloadHelper(QThread):
    progressChanged = pyqtSignal(int)
    messageChanged = pyqtSignal(str)
    doneSignal = pyqtSignal(bool)

    def __init__(self, source, directory, hd, host, animeField):
        super().__init__()
        self.source = source
        self.directory = directory
        self.hd = hd
        self.host = "https://" + host + "dist.animemusicquiz.com/"
        self.running = False
        self.animeField = animeField

    def run(self):
        try:
            self.running = True
            if self.hd is None:
                self.downloadMP3(self.source, self.directory)
            else:
                self.downloadVideo(self.source, self.directory, self.hd)
            self.doneSignal.emit(True)
        except:
            logging.exception("An error has occured while downloading.")
            self.doneSignal.emit(False)

    def fetchSong(self, anime, L, url, directory, video):
        print("Downloading " + L['songName'] + " from catbox.moe")
        self.messageChanged.emit(
            "Downloading " + L['songName'] + " from catbox.moe")
        response = requests.get(url)
        songType = L['songType']

        name = anime + " - " + songType + \
               " (" + L['songName'] + " by " + \
               L['songArtist'] + ") " + str(L["annSongId"])
        namefile = ""
        for i in range(len(name)):
            if name[i] not in ["/", "\\", "*", "|", ":", "?", "\"", "<", ">"]:
                namefile += name[i]
        namefile = os.path.join(directory, namefile +
                                (".webm" if video else ".mp3"))
        return response, namefile, name, songType

    def downloadMP3(self, source, directory):
        progress = 0
        total = len(source)

        i = 0
        while self.running and i < len(source):
            L = source[i]
            i += 1
            mp3 = True
            if L['audio']:
                url = L['audio']
            elif L['MQ']:
                url = L["MQ"]
                mp3 = False
            else:
                url = L['HQ']
                mp3 = False
            if url:
                url = self.host + url

                if not mp3:
                    print("No mp3 uploaded, converting a video...")
                    self.messageChanged.emit(
                        "No mp3 uploaded, converting a video...")

                anime = L[self.animeField]

                response, namefile, name, songType = self.fetchSong(
                    anime, L, url, directory, False)
                if not mp3:
                    open("temp.webm", "wb").write(response.content)

                    sys.path.append(path.abspath(path.dirname(__file__)))

                    cmdline = f'ffmpeg -i temp.webm "{namefile}"'
                    r = subprocess.run(
                        cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    logging.info(f'{cmdline}": %r', r.stdout.decode(errors="replace"))
                    os.remove("temp.webm")
                    print("Complete")
                    self.messageChanged.emit("Complete")
                else:
                    print("Writing to file...")
                    self.messageChanged.emit("Writing to file...")
                    open(namefile, "wb").write(response.content)
                    print("Written")
                    self.messageChanged.emit("Written")

                print('Adding metadata')
                self.messageChanged.emit('Adding metadata')
                audiofile = eyed3.load(namefile)
                if not audiofile.tag:
                    audiofile.initTag()

                audiofile.tag.artist = L['songArtist']
                audiofile.tag.title = L['songName'] + \
                                      " (" + anime + " - " + songType + ")"
                audiofile.tag.track_num = L["annSongId"]
                audiofile.tag.save(version=(2, 4, 0), encoding='utf-8')

                print("Added")
                self.messageChanged.emit("Added")
                progress += 1

                progress_msg = f"{name} complete, to next song! {progress}/{len(source)} ({round(progress / len(source) * 100, 2)}%)\n"
                print(progress_msg)
                self.messageChanged.emit(progress_msg)
            else:
                progress += 1
                progress_msg = f"No upload found for {L['songArtist']} - {L['songName']}, skipping. {progress}/{len(source)} ({round(progress / len(source) * 100, 2)}%)\n"
                print(progress_msg)
                self.messageChanged.emit(progress_msg)
            self.progressChanged.emit(int(progress / total * 100))

    def downloadVideo(self, source, directory, hd):
        progress = 0
        total = len(source)

        i = 0
        while self.running and i < len(source):
            L = source[i]
            i += 1
            url = self.host
            if hd:
                if L['HQ']:
                    url += L['HQ']
                else:
                    url += L['MQ']
            else:
                if L['MQ']:
                    url += L['MQ']
                else:
                    url += L['HQ']

            response, namefile, _, _ = self.fetchSong(
                L[self.animeField], L, url, directory, True)
            print("Writing to file...")
            self.messageChanged.emit("Writing to file...")
            open(namefile, "wb").write(response.content)
            print("Written")
            self.messageChanged.emit("Written")
            progress += 1
            self.progressChanged.emit(int(progress / total * 100))

    def stop(self):
        self.running = False
