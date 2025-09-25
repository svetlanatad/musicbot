# Guide on how to set up your own telegram bot that downloads music 

## What it can do

- Accept YouTube URLs via Telegram
- Convert video to high-quality MP3 (192 kbps)
- Send back the `.mp3` audio file to the user
- Asynchronous, efficient, and minimal logging

---

## Requirements

- Linux 
- Python 3.12+ (or 3.10+, adjust accordingly)
- `ffmpeg` compiled **with libmp3lame support**
- Telegram Bot Token
- `yt-dlp`, `python-telegram-bot`, `moviepy` (for audio processing, optional)

---

## 1. Install Required Packages

Create a **Python virtual environment**:

```
python3 -m venv myvenv
source myvenv/bin/activate

```

Then install the required packages: 
```
pip install -U yt-dlp python-telegram-bot moviepy
```
Now you need to install and configure ffmpeg. So it works, you have to compile it with libmp3lame support, you have to figure out how to compile and configure correctly based on your os. 
To check if your ffmpeg supports the library, run:

```
ffmpeg -codecs | grep libmp3lame
```

This is how I built with ffmpeg on gentoo:
downloaded the source code from https://ffmpeg.org/download.html
cd ffmpeg 
./configure --enable-gpl --enable-libmp3lame 
make 
make install 

Ok then, copy the executable to your virtual environment/bin directory 
Maybe you need to sett up path variable, do it with this command: 
```
export PATH="$HOME/ffmpeg_build/bin:$PATH"
```
3. Set Up Your Telegram Bot

Talk to @BotFather

Run /newbot

Set a name and username

You’ll receive a Bot Token, e.g., 123456789:ABCDEF...

Save this python code as whatever.py file 

Activate your virtual environment with this command:
source /path/to/your/venv/bin/activate

then just run the script and use! Have fun 




