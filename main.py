from setlist_grabber import SetlistGrabber
from apple_music_client import AppleMusicClient
import urllib.parse

APP_ID = "VHARX7K299.media.johansenet.setlisttoplaylist"



URL="https://www.setlist.fm/setlist/crown-the-empire/2024/lovedrafts-brewing-co-mechanicsburg-pa-6ba9a616.html"

grabber = SetlistGrabber(URL)
songs = grabber.get_song_names()


amc = AppleMusicClient()
amc.get_all_playlists()
# for song in songs:
#     print(song)
#     amc.search_for_song(song, "Crown The Empire")



