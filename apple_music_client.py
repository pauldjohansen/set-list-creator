import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import jwt
import json

load_dotenv()

key_id = os.environ.get("APPLE_KEY_ID")
team_id = os.environ.get("APPLE_TEAM_ID")
KEY_FILE_LOCATION = "keys/AuthKey_YJQZ9U3UTA.p8"

MUT_GENERATOR = "https://d1skmsh1xucp4e.cloudfront.net/index.html"
BASE_API_URL = "https://api.music.apple.com/v1/"
TEST_API_ENDPOINT = BASE_API_URL + "test"
SEARCH_API_ENDPOINT = BASE_API_URL + "catalog/us/search"
MUSIC_USER_TOKEN = "AmxtjdXEbzvLiq2+DYqUHgEbcJo/weuLRGWda2aH6l4hn4y/MOwcSh4A6mvGrMLlPBEAP2c+P9YEPWLaE4qIAd+ad+l6NASY79e8F2DGIli9+SB8+MO6tMfwm0Erb4g5UIx2JmwrfESEyhuXUyEtzHxWU5lbfLzm/DnRRnpCCMLsInSCMYsNlavzVZybsoTcrxrnEB1RVYrvPibi2174XiQZznzydyXOtOSMtVmPUu2248ffRA=="
PLAYLISTS_API_ENDPOINT = BASE_API_URL + "me/library/playlists"
APP_ID = "VHARX7K299.media.johansenet.setlisttoplaylist"


class AppleMusicClient:
    def __init__(self):
        self.developer_token = ""
        self._alg = "ES256"
        with open(KEY_FILE_LOCATION, "r") as f:
            self.private_key = f.read()
        self._generate_am_token(12)
        self.mut_generator_url = MUT_GENERATOR
        self.app_id = APP_ID
        self.music_user_token = MUSIC_USER_TOKEN

    def generate_headers(self, include_music_user_token: bool, include_content_type: bool):
        playlist_headers = {}
        playlist_headers["Authorization"] = f"Bearer {self.developer_token}"
        if include_music_user_token:
            playlist_headers["Music-User-Token"] = self.music_user_token
        if include_content_type:
            playlist_headers["Content-Type"] = "application/json"
        return playlist_headers

    def search_for_song_id(self, song_title, artist):
        search_url = SEARCH_API_ENDPOINT + "?"
        search_term = f"{song_title}+{artist}".replace(" ", "+")
        params = f"types=songs&term={search_term}"
        search_url = search_url + params

        response = requests.get(
            url=search_url,
            headers=self.generate_headers(False, False),
        )
        response.raise_for_status()
        search_results = response.json()
        return search_results["results"]["songs"]["data"][0]["id"]

    def run_test(self):
        response = requests.get(
            url=TEST_API_ENDPOINT,
            headers=self.generate_headers(False, False),
        )
        response.raise_for_status()
        print(response.status_code)

    def set_music_user_token(self, token):
        self.music_user_token = token

    def _generate_am_token(self, session_length):
        token_exp_time = datetime.now() + timedelta(hours=session_length)
        headers = {"alg": self._alg, "kid": key_id}
        payload = {
            'iss': team_id,
            'iat': int(datetime.now().timestamp()),  # issued at
            'exp': int(token_exp_time.timestamp()),  # expiration time
        }
        self.token_valid_until = token_exp_time
        token = jwt.encode(payload, self.private_key, algorithm=self._alg, headers=headers)
        self.developer_token = token if type(token) is not bytes else token.decode()

    def get_all_playlists(self):
        playlist_url = PLAYLISTS_API_ENDPOINT
        playlist_url = playlist_url

        playlist_headers = self.generate_headers(True, False)

        response = requests.get(
            url=playlist_url,
            headers=playlist_headers,
        )
        response.raise_for_status()
        search_results = response.json()
        print(response.text)

    def add_new_playlist(self, playlist_name, track_ids):
        payload = {
            "attributes": {
                "name": playlist_name
            },
            "relationships": {
                "tracks": {
                    "data": [{"id": track_id, "type": "songs"} for track_id in track_ids]
                }
            }
        }

        headers = self.generate_headers(True, True)

        response = requests.post(PLAYLISTS_API_ENDPOINT, headers=headers, data=json.dumps(payload))

        if response.status_code == 201:
            print("Playlist created successfully!")
            print("Playlist details:", response.json())
        else:
            print(f"Failed to create playlist: {response.status_code}")
            print("Response:", response.json())
