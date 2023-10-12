from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time


class currentPlaying:
    def f(self):
        self.update()
        return

    def update(self):
        currentPlaying = sp.current_user_playing_track()
        # print(currentPlaying)

        if currentPlaying == "None":
            print("Nothing Playing")
            return None
        timeMs = int(currentPlaying["progress_ms"])
        self.timeSec = int((timeMs / 1000) % 60)
        if len(str(self.timeSec)) == 1:
            self.timeSec = "0" + str(self.timeSec)
        self.timeMin = int((timeMs / (1000 * 60)) % 60)
        self.title = currentPlaying["item"]["name"]
        self.artist = currentPlaying["item"]["artists"][0]["name"]
        self.cover_art = currentPlaying["item"]["album"]["images"][2][
            "url"
        ]  # 64x64, [0] for higher 300x300
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


cp = currentPlaying()
# while True:
if cp.update() != None:
    print(cp.cover_art)
    print(str(cp.timeMin) + ":" + str(cp.timeSec) + " " + cp.title + " " + cp.artist)
    # time.sleep(1)
