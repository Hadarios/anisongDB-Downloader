# anisongDB-Downloader
A program to download songs from [anisongdb](https://anisongdb.com) as MP3 files with title and artist ID3 tags or as webm files.  

## Features
- Search songs from anisongdb  
- Select songs from search results  
- Keep songs selected in-between searches  
- Download selected songs as MP3 files or as high/low-quality webm files  

## Run

To use anisongDB-Downloader, you can either:
- Run the script with Python3
- Download and run the [released EXE file](https://github.com/Hadarios/anisongDB-Downloader/releases)
- [Build](#build-an-exe-file) and run an EXE file

## Python depedencies

To run the script with Python3, you will need these packages:  

- requests
- BeautifulSoup
- eyed3
- PyQt6

To install all of them, you can directly run:  
```Bash
pip install -r requirements.txt
```

## Build an EXE file
You can build an EXE file yourself by running the following command:
```Bash
pyinstaller anisongDB-Downloader.spec
```
You can install pyinstaller through pip:
```Bash
pip install pyinstaller
```

## IMPORTANT NOTE
> [!WARNING]  
When you download songs as MP3, if you selected songs that are only uploaded as video, the script will download them and convert them to mp3.  
I used [ffmpeg](https://www.ffmpeg.org/) in order to do this. An [EXE file](files/ffmpeg.exe) is used when running on Windows, but you will need to install it yourself on MacOS and Linux.  
