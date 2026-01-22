import requests
import json

from datetime import date
import airflow
from airflow.models import Variable
from airflow.decorators import dag, task


API_KEY = Variable.get('API_KEY')
CHANNEL_HANDLE = Variable.get('CHANNEL_HANDLE')
maxResults = 50

@task
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

@task
def get_videoIDs(playlist_id):
    videoIDs = []
    pageToken = None
    BaseUrl = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    try:
        while True:
            print(f"Collected {len(videoIDs)} IDs so far...", end="\r")
            url = BaseUrl
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            #print(response)
            data = response.json()
            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                videoIDs.append(video_id)
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        return videoIDs
    except requests.exceptions.RequestException as e:
        raise e

@task
def extract_video_data(video_ids):
    extracted_data = []
    def batch_videoIDs(videoID_lst, batch_size=50):
        for video_id in range(0,len(videoID_lst), batch_size):
            yield videoID_lst[video_id:video_id + batch_size]

    try:
        for batch in batch_videoIDs(video_ids,maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    'video_id': video_id,
                    'title': snippet.get('title'),
                    'publishedAt': snippet.get('publishedAt'),
                    'duration': contentDetails.get('duration'),
                    'viewCount': statistics.get('viewCount', None),
                    'likeCount': statistics.get('likeCount', None),
                    'commentCount': statistics.get('commentCount', None)
                }
                extracted_data.append(video_data)
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

@task
def save_to_json(extracted_data):
    filepath = f'./data/{CHANNEL_HANDLE}_{date.today()}.json'
    with open(filepath, 'w', encoding='utf-8') as json_output:
        json.dump(extracted_data, json_output, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlist_id = get_playslist_id()
    #print(f'Playlist ID for channel - {CHANNEL_HANDLE}: {playlist_id}')
    videos_id = get_videoIDs(playlist_id)
    extract_video_data(videos_id)    
    #print(f'Total videos found: {len(videos_id)}')
    video_data = extract_video_data(videos_id)
    #print(f'Total videos data extracted: {len(video_data)}')
    save_to_json(video_data)
