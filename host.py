from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import time
import os
import serial


# Spotify API
class currentPlaying:
    def __init__(self):
        self.title = None
        self.artist = None
        self.cover_art = None
        self.album_id = None

    def __str__(self) -> str:
        return str(self.title) + " - " + str(self.artist)

    def empty(self):
        self.title = None
        self.artist = None
        self.cover_art = None
        self.album_id = None
        return self

    def update(self):
        currentPlaying = sp.current_user_playing_track()
        if currentPlaying == None:
            return self.empty()

        # Song Info

        self.title = currentPlaying["item"]["name"]
        self.artist = currentPlaying["item"]["artists"][0]["name"]
        # 64x64, [0] for higher 300x300
        self.cover_art = currentPlaying["item"]["album"]["images"][2]["url"]
        self.album_id = currentPlaying["item"]["album"]["uri"].split(":")[2]

        return self


# Take from creds.json file in same directory
with open("creds.json") as f:
    data = json.load(f)
    client_id = data["client_id"]
    client_secret = data["client_secret"]
    callback_uri = data["callback_uri"]

scope = "user-read-currently-playing"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=callback_uri,
    )
)


# Image Handling
cover_art_path = "cover_art/"
bmp_cover_art_path = "cover_art/bmp/"

if not os.path.exists(cover_art_path):
    os.makedirs(cover_art_path)
if not os.path.exists(bmp_cover_art_path):
    os.makedirs(bmp_cover_art_path)


def download_cover_art_and_convert_to_32x32_bmp(url, filename):
    if not os.path.exists(cover_art_path + filename + ".jpg"):
        download_cover_art(url, filename)
        convert_cover_art_to_32x32_bmp(filename)
        print("Downloaded cover art: " + filename)
        return True
    else:
        # print("File already exists: " + filename)
        return False


def download_cover_art(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(cover_art_path + filename + ".jpg", "wb") as f:
            f.write(response.content)
    else:
        print("Error downloading cover art: " + response)


def convert_cover_art_to_32x32_bmp(filename):
    img = Image.open(cover_art_path + filename + ".jpg")
    img = img.resize((32, 32))
    img.save(bmp_cover_art_path + filename + ".bmp")


# RPI Handling
def copy_file_to_rpi(filename):
    # copy to /Volumes/CIRCUITPY/bmp
    print("Copying " + filename + " to RPI")
    localBmpDir = bmp_cover_art_path + filename + ".bmp"
    rpiBmpDir = "/Volumes/CIRCUITPY/bmp/" + filename + ".bmp"
    os.system("cp " + localBmpDir + " " + rpiBmpDir)


print("Starting")
ser = serial.Serial("/dev/tty.usbmodem101", baudrate=9600, timeout=0.5)
print("Using", ser.name)
ser.read(100)

cp = currentPlaying()
while True:
    cp.update()
    if cp != None:
        print(cp.title + " - " + cp.artist)
        downloaded = download_cover_art_and_convert_to_32x32_bmp(
            cp.cover_art,
            cp.album_id,
        )
        if downloaded:
            copy_file_to_rpi(cp.album_id)
        ser.write("1 {cp.album_id};".format(cp=cp).encode())
        time.sleep(1)
    else:
        print("Nothing Playing")
        ser.write(b"0")
        time.sleep(1)
