from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import time
import os


class currentPlaying:
    def f(self):
        self.update()
        return self

    def update(self):
        currentPlaying = sp.current_user_playing_track()
        # print(currentPlaying)

        if currentPlaying == "None":
            print("Nothing Playing")
            return None

        # Playtime
        timeMs = int(currentPlaying["progress_ms"])
        self.timeSec = int((timeMs / 1000) % 60)
        if len(str(self.timeSec)) == 1:
            self.timeSec = "0" + str(self.timeSec)
        self.timeMin = int((timeMs / (1000 * 60)) % 60)

        # Song Info
        self.title = currentPlaying["item"]["name"]
        self.artist = currentPlaying["item"]["artists"][0]["name"]
        # 64x64, [0] for higher 300x300
        self.cover_art = currentPlaying["item"]["album"]["images"][2]["url"]
        self.album_id = currentPlaying["item"]["album"]["uri"].split(":")[2]

        return self


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
    # else:
    #     print("File already exists: " + filename)


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


cp = currentPlaying()
while True:
    now_playing = cp.update()
    if now_playing != None:
        # print(now_playing.cover_art)
        print(
            str(now_playing.timeMin)
            + ":"
            + str(now_playing.timeSec)
            + " "
            + now_playing.title
            + " "
            + now_playing.artist
        )
        download_cover_art_and_convert_to_32x32_bmp(
            now_playing.cover_art,
            now_playing.album_id,
        )
        time.sleep(1)
    else:
        print("Nothing Playing")
        time.sleep(1)
