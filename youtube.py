import os
import json
from googleapiclient.discovery import build

API_KEY = 'AIzaSyCRw1YPWoQZc-mYaXUrOyNUvIe_mkyEugc'

def get_homepage_video_data():
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # Call the API to retrieve the list of videos from the homepage
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode='US',  # You can change the region code on your location
        maxResults=20
    )

    video_data = []

    response = request.execute()
    for item in response.get('items', []):
        video_id = item['id']
        video_title = item['snippet']['title']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        thumbnail_url = item['snippet']['thumbnails']['default']['url']  

        video_data.append({
            'video_id': video_id,
            'video_title': video_title,
            'video_url': video_url,
            'thumbnail_url': thumbnail_url
        })

    return video_data

if __name__ == '__main__':
    video_data_homepage = get_homepage_video_data()

    # Save the video data to a JSON file
    with open('homepage_video_data.json', 'w') as f:
        json.dump(video_data_homepage, f, indent=2)

    print(f'Total {len(video_data_homepage)} homepage videos data saved to homepage_video_data.json.')
