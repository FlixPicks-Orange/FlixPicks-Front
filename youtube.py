import os
import json
from googleapiclient.discovery import build

API_KEY = 'AIzaSyCRw1YPWoQZc-mYaXUrOyNUvIe_mkyEugc'

def get_homepage_video_data():
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    videos = []

    # Call the API to get homepage videos
    request = youtube.videos().list(
        part='snippet',
        chart='mostPopular',
        regionCode='US',  # You can change the region code
        maxResults=10
    )
    response = request.execute()
    items = response['items']

    video_ids = [item['id']for item in items]
    video_titles = [item['snippet']['title']for item in items]
    video_thumbnails = [item['snippet']['thumbnails']['default']['url']for item in items]

    for id, title, thumbnail in zip(video_ids, video_titles, video_thumbnails):
        videos.append({'id': id, 'title': title, 'thumbnail':thumbnail})

    return videos  



    

