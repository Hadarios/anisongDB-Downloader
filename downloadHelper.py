import requests
from bs4 import BeautifulSoup
import os
import eyed3
import subprocess

def fetchSong(anime, L, url, directory, ins):
    print("Downloading " + L['songName'] + " from catbox.moe")
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

def downloadMP3(source, directory):
    ins = 1
    global loadProgress
    progress = 0
    total = len(source)
    ann = ""
    anime = ""

    for L in source:
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
            url = "https://nl.catbox.video/" + url
            if ann != str(L['annId']):
                print("Fetching next ANN entry")
                ann = str(L['annId'])
                r = requests.get("https://www.animenewsnetwork.com/encyclopedia/anime.php?id=" + ann)
                soup = BeautifulSoup(r.content, 'html.parser')
                anime = soup.select_one('#page_header').text.strip()
                print("Fetched " + anime)
                ins = 1

            if not mp3:
                print("No mp3 uploaded, converting a video...")

            response, namefile, name, songType = fetchSong(anime, L, url, directory, ins)

            if not mp3:
                open("temp.webm", "wb").write(response.content)
                subprocess.run('ffmpeg -i temp.webm "{0}"'.format(namefile), shell=True)
                os.remove("temp.webm")
                print("Complete")
            else:
                print("Writing to file...")
                open(namefile, "wb").write(response.content)
                print("Written")
    
            print('Adding metadata')
            audiofile = eyed3.load(namefile)
            if not audiofile.tag:
                audiofile.initTag()
    
            audiofile.tag.artist = L['songArtist']
            audiofile.tag.title = L['songName'] + " (" + anime + " - " + songType + ")"
            audiofile.tag.save(version=(2,3,0))
            print("Added")
            progress+=1
            print("{0} complete, to next song! {1}/{2} ({3}%)\n".format(name, progress, len(source), round(progress/len(source)*100), 2))
        else:
            progress+=1
            print("No upload found for {0} - {1}, skipping. {2}/{3} ({4}%)\n".format(L['songArtist'], L['songName'], progress, len(source), round(progress/len(source)*100), 2))

def downloadVideo(source, directory, hd):
    progress = 0

    for L in source:
        url = "https://nl.catbox.video/"
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

        response, namefile, _, _ = fetchSong(L["animeJPName"], L, url, directory, None)

        print("Writing to file...")
        open(namefile, "wb").write(response.content)
        print("Written")
        progress += 1