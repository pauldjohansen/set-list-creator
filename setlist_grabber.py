import requests
from bs4 import BeautifulSoup
class SetlistGrabber:
    def __init__(self, setlist_url):
        self.setlist_url = setlist_url

    def get_song_names(self):
        response = requests.get(self.setlist_url)
        soup = BeautifulSoup(response.text, "html.parser")
        songs = soup.find_all("a", class_="songLabel")
        songs = [song.getText() for song in songs]
        return songs
