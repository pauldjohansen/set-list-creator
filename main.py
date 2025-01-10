from setlist_grabber import SetlistGrabber
from apple_music_client import AppleMusicClient
import urllib.parse
import pyperclip

URL = "https://www.setlist.fm/setlist/beartooth/2024/alsterdorfer-sporthalle-hamburg-germany-7bab369c.html"
PLAYLIST_NAME= "Beartooth Homework"
ARTIST = "Beartooth"
prompt_for_MUT = True


def prompt_for_next():
    input("Ready to continue?")


def get_MUT():
    pyperclip.copy(amc.mut_generator_url)
    print(f"URL copied to clipboard: {amc.mut_generator_url}")
    prompt_for_next()
    pyperclip.copy(amc.developer_token)
    print(f"Developer token copied to clipboard: {amc.developer_token}")
    prompt_for_next()
    amc.set_music_user_token(input("Enter your Music User Token: "))


grabber = SetlistGrabber(URL)
songs = grabber.get_song_names()

amc = AppleMusicClient()
if prompt_for_MUT:
    get_MUT()

song_ids = []
for song in songs:
    try:
        song_id = amc.search_for_song_id(song, ARTIST)
        song_ids.append(song_id)
    except Exception as e:
        print(f"Error searching for song '{song}': {str(e)}")
        # You could also use logging instead of print:
        # logging.error(f"Error searching for song '{song}': {str(e)}")
        continue

amc.add_new_playlist(PLAYLIST_NAME, song_ids)
