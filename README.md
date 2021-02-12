# Wim Hof Breathing Helper
## Description
Wim Hof Breathing Helper is a program designed to automate a few key components to a Wim Hof breathing session such as:

- Having Wim guide your breathing via mp3 files
- Playing a song during the breath hold
- Recording the hold times in a log file

# Easy access
To get started, just grab the single-file from the bin folder for your operating system

## Usage
`python wim-hof.py`

Then enter the number of iterations you want to go for. 3 is typical

`3`

`enter`

# Developer Instructions
## Setup
You may setup a venv

`python -m venv ./venv`

`pip install -r requirements.txt`

Then add songs into the song1, song2, and song3 folders. If you want to have more iterations to your Wim Hof experience, just make more folders!

## Compiling a distribution binary manually
`pip install pyinstaller`

`pyinstaller --paths ./libvlc --add-data 'audio:audio' --onefile wim-hof.py`

### Compiling binary with docker
First, create a spec file

`pyi-makespec --add-binary 'libvlc/*.dll:VLC' --add-data 'audio:audio' --onefile wim-hof.py`

Then run the following docker image command. It will create a dist dir with the binary

Linux: `docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python3`

Windows needs an updated docker file from the cdrx repo, so we will need to build a new one

`docker build -f Dockerfile-py3-win64 .`

and then do these changes: https://github.com/pyinstaller/pyinstaller/issues/4506

Windows: `docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python3`

## Known issues
- If you hold your breath beyond the duration of a song, another song will not begin playing
- The .tsv file can be corrupted by writing an empty line to it


# Licenses
Music by Ketsa, https://freemusicarchive.org/music/Ketsa, https://ketsa.uk/  and Siddhartha Corsus https://siddharthamusic.bandcamp.com/ used under the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) https://creativecommons.org/licenses/by-nc-nd/4.0/ license which can be found https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode