# anisongDB-Downloader
A program to download songs from [anisongdb](https://anisongdb.com) as MP3 files with title and artist ID3 tags or as webm files.  
Python depedencies: requests, BeautifulSoup, eyed3, PyQt6  
You can either run the script with Python3 or download the released EXE, which should be runnable without any of the dependencies installed.  
If you have any problem or question, feel free to contact me.

## Features
- Search songs from anisongdb  
- Select songs from search results  
- Keep songs selected in-between searches  
- Download selected songs as MP3 files or as high/low-quality webm files  

## IMPORTANT NOTE
> [!WARNING]  
When you download songs as MP3, if you selected songs that are only uploaded as video, the script will download them and convert them to mp3.  
I used ffmpeg in order to do this, so you will need to install it to make that work.  
Currently, if this happens and you haven't installed ffmpeg, the app will crash. I might add a check and a warning in the future, but be warned for now.  
[Here's a tutorial for its installation on Windows (wikihow).](https://www.wikihow.com/Install-FFmpeg-on-Windows)  
