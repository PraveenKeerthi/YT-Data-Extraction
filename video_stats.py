import requests
import os
from dotenv import load_dotenv


load_dotenv()

def get_channel_playlistID():
    try:
        api_key = os.getenv('api_key')
        print(api_key)
        channel= "MrBeast"

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel}&key={api_key}"

        response = requests.get(url)

        data = response.json()
        print(data)

        channel_items = data['items'][0]
        channel_playlist_id = channel_items['contentDetails']['relatedPlaylists']['uploads']
        return channel_playlist_id
    except Exception as e:
        print("Error while retreiving channel ID: ", e)

if __name__=='__main__':
    print("Getting channel ID executed")
    channel_playlist_id = get_channel_playlistID()
    print(channel_playlist_id)
