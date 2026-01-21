import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = 'IGN'

def get_playslist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'
        response = requests.get(url)
        response.raise_for_status()
        #print(response)
        data = response.json()
        #print(json.dumps(data, indent=4))
        channel_items = data['items'][0]
        playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        return playlist_id
    except requests.exceptions.RequestException as e:
        raise e
    
if __name__ == "__main__":
    playlist_id = get_playslist_id()
    print(f'Playlist ID for channel - {CHANNEL_HANDLE}: {playlist_id}')
