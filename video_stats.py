from pickle import NONE
import requests
import os
from dotenv import load_dotenv
from datetime import date
import json


load_dotenv()
api_key = os.getenv('api_key')

def get_channel_playlistID():
    try:
        channel= "MrBeast"

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel}&key={api_key}"

        response = requests.get(url)

        data = response.json()

        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        return channel_playlist_id
    except Exception as e:
        print("Error while retreiving channel ID: ", e)
        
def get_video_ids(playlistID):
    video_ids = []
    pageToken = None
    max_result = 50
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_result}&playlistId={playlistID}&key={api_key}"
    while True:
        try:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            data = response.json()
            for i in data.get('items', []):
                video_ids.append(i['contentDetails']['videoId'])
            
            pageToken = data.get('nextPageToken')
            if not pageToken:
                break
        except Exception as e:
            print("Error while retreiving video IDs: ", e)
            break
    return video_ids
def extract_video_stats(video_ids):
    extracted_data =[]
    def batch_list(video_ids,maxResult):
        for i in range(0,len(video_ids),maxResult):
            yield video_ids[i:i+maxResult]
    try:
        for batch in batch_list(video_ids,50):
            video_ids = ','.join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids}&key={api_key}"
            response = requests.get(url)
            data = response.json()
            for i in data.get('items', []):
                video_id = i['id']
                title = i.get('snippet').get('title', '')
                publishedAt = i.get('snippet').get('publishedAt', '')
                viewCount = i.get('statistics').get('viewCount', 0)
                likeCount = i.get('statistics').get('likeCount', 0)
                dislikeCount = i.get('statistics').get('dislikeCount', 0)
                commentCount = i.get('statistics').get('commentCount', 0)
                duration = i.get('contentDetails').get('duration', '')
                extracted_data.append({
                    'video_id': video_id,
                    'title': title,
                    'publishedAt': publishedAt,
                    'viewCount': viewCount,
                    'likeCount': likeCount,
                    'dislikeCount': dislikeCount,
                    'commentCount': commentCount,
                    'duration': duration,
                })
    except Exception as e:
        print("Error while retreiving video stats: ", e)
    return extracted_data

def save_to_json(extracted_data):
    file_path = os.path.join(os.getcwd(), "data", f"YT_data_{date.today()}.json")
    with open(file_path, 'w') as f:
        json.dump(extracted_data, f, indent=4)
if __name__=='__main__':
    print("Getting channel ID .....")
    channel_playlist_id = get_channel_playlistID()
    print("Getting video IDs .....")
    video_ids = get_video_ids(channel_playlist_id)
    print("Extracting video stats .....")
    extracted_data = extract_video_stats(video_ids)
    print("Extracted data: ", extracted_data)
    save_to_json(extracted_data)
