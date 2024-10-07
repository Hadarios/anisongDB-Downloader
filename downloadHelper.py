import os
import subprocess
import sys

import eyed3
import requests
from PyQt6.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup

class DownloadHelper(QThread):
    progressChanged = pyqtSignal(int)
    messageChanged = pyqtSignal(str)
    doneSignal = pyqtSignal(bool)

    def __init__(self, source, directory, hd, urlIndex):
        super().__init__()
        self.source = source
        self.directory = directory
        self.hd = hd
        self.host = "https://" + ("ladist1" if urlIndex == 0 else "nl" if urlIndex == 1 else "vhdist1") + ".catbox.video/"
        self.running = False

    def run(self):
        self.running = True
        if self.hd is None:
            self.downloadMP3(self.source, self.directory)
        else:
            self.downloadVideo(self.source, self.directory, self.hd)
        self.doneSignal.emit(True)

    def fetchSong(self, anime, L, url, directory, ins):
        print("Downloading " + L['songName'] + " from catbox.moe")
        self.messageChanged.emit("Downloading " + L['songName'] + " from catbox.moe")
        response = requests.get(url)
        if L['songType'][0] == "I":
            if ins is not None:
                songType = "Insert " + str(ins)
                ins += 1
            else:
                songType = "Insert"
        else:
            songType = L['songType']
    
        name = anime + " - " + songType + " (" + L['songName'] + " by " + L['songArtist'] + ")"
        namefile = ""
        for i in range(len(name)):
            if name[i] not in ["/", "\\", "*", "|", ":", "?", "\"", "<", ">"]:
                namefile += name[i]
        namefile = directory + "\\" + namefile + (".webm" if ins is None else ".mp3")
    
        return response, namefile, name, songType
    
    def downloadMP3(self, source, directory):
        ins = 1
        progress = 0
        total = len(source)
        ann = ""
        anime = ""

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
                if ann != str(L['annId']):
                    print("Fetching next ANN entry")
                    self.messageChanged.emit("Fetching next ANN entry")
                    ann = str(L['annId'])
                    r = requests.get("https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + ann)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    anime = soup.select_one('#page_header').text.strip()
                    print("Fetched " + anime)
                    self.messageChanged.emit("Fetched " + anime)
                    ins = 1
    
                if not mp3:
                    print("No mp3 uploaded, converting a video...")
                    self.messageChanged.emit("No mp3 uploaded, converting a video...")
    
                response, namefile, name, songType = self.fetchSong(anime, L, url, directory, ins)
    
                if not mp3:
                    open("temp.webm", "wb").write(response.content)
                    if sys.platform == 'win32':
                        subprocess.run('files/ffmpeg -i temp.webm "{0}"'.format(namefile), shell=True)
                    else:
                        subprocess.run('ffmpeg -i temp.webm "{0}"'.format(namefile), shell=True)
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
                audiofile.tag.title = L['songName'] + " (" + anime + " - " + songType + ")"
                audiofile.tag.save(version=(2,3,0))
                print("Added")
                self.messageChanged.emit("Added")
                progress+=1
                print("{0} complete, to next song! {1}/{2} ({3}%)\n".format(name, progress, len(source), round(progress/len(source)*100), 2))
                self.messageChanged.emit("{0} complete, to next song! {1}/{2} ({3}%)\n".format(name, progress, len(source), round(progress/len(source)*100), 2))
            else:
                progress+=1
                print("No upload found for {0} - {1}, skipping. {2}/{3} ({4}%)\n".format(L['songArtist'], L['songName'], progress, len(source), round(progress/len(source)*100), 2))
                self.messageChanged.emit("No upload found for {0} - {1}, skipping. {2}/{3} ({4}%)\n".format(L['songArtist'], L['songName'], progress, len(source), round(progress/len(source)*100), 2))
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
    
            response, namefile, _, _ = self.fetchSong(L["animeJPName"], L, url, directory, None)
    
            print("Writing to file...")
            self.messageChanged.emit("Writing to file...")
            open(namefile, "wb").write(response.content)
            print("Written")
            self.messageChanged.emit("Written")
            progress += 1
            self.progressChanged.emit(int(progress / total * 100))

    def stop(self):
        self.running = False