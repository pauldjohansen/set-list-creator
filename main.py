from setlist_grabber import SetlistGrabber
from apple_music_client import AppleMusicClient
import urllib.parse
import pyperclip

URL="https://www.setlist.fm/setlist/crown-the-empire/2024/the-regent-theater-los-angeles-ca-7355f209.html"
ARTIST="Crown The Empire"

def prompt_for_next():
    input("Ready to continue?")

def prompt_for_MUT():
    pyperclip.copy(amc.mut_generator_url)
    print(f"URL copied to clipboard: {amc.mut_generator_url}")
    prompt_for_next()
    pyperclip.copy(amc.developer_token)
    print(f"Developer token copied to clipboard: {amc.developer_token}")
    prompt_for_next()
    pyperclip.copy(amc.app_id)
    print(f"App Id to clipboard: {amc.app_id}")
    amc.set_music_user_token(input("Enter your Music User Token"))

# grabber = SetlistGrabber(URL)
# songs = grabber.get_song_names()


amc = AppleMusicClient()
amc.get_all_playlists()



# for song in songs:
#     print(song)
#     amc.search_for_song(song, ARTIST)



