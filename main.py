import os
import re
from datetime import timedelta
from typing import List
import urllib.request
from googleapiclient.discovery import build
from sqlalchemy.orm import sessionmaker

from channel import Channel
from crawler import PlaylistCrawler, ChannelCrawler
from models import Video
from playlist import Playlist
from settings import engine

api_key = "AIzaSyAfsclKs6PdPUhK3utgJDJx1TN6cLkpAWE"

youtube_service = build('youtube', 'v3', developerKey=api_key)


def get_uploads_id(channel):
    request = youtube_service.channels().list(
        part='contentDetails',
        forUsername=channel)

    response = request.execute()
    playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    return playlist_id


def create_playlist_directory(playlist_id):
    base_dir = os.path.join(os.path.expanduser('~'), 'Downloads')+"/" + "Crawler"
    os.mkdir(base_dir)

    thumbnails = base_dir + "/thumbnails"
    originals = base_dir + "/original_images"

    os.mkdir(thumbnails)
    os.mkdir(originals)

    return thumbnails, originals


def get_playlist_videos(playlist_id):
    thumbnails, originals = create_playlist_directory(playlist_id)

    videos = []

    nextPageToken = None

    while True:

        request = youtube_service.playlistItems().list(
            part='snippet, contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken)

        response = request.execute()

        for item in response['items']:
            video = Video()

            video.id = item['contentDetails']['videoId']
            video.title = item['snippet']['title']

            try:
                thumbnail_url = item['snippet']['thumbnails']['default']['url']
                thumbnail_path = thumbnails + "/" + video.id + ".jpg"
                urllib.request.urlretrieve(thumbnail_url, thumbnail_path)

            except KeyError:
                thumbnail_url = None
            try:
                fullsized_url = item['snippet']['thumbnails']['maxres']['url']
                fullsized_path = originals + "/" + video.id + ".jpg"
                urllib.request.urlretrieve(fullsized_url, fullsized_path)

            except KeyError:
                fullsized_url = None

            video.thumbnail_image_url = thumbnail_url
            video.thumbnail_image_path = thumbnail_path
            video.fullsized_image_url = fullsized_url
            video.fullsized_image_path = fullsized_path

            video.url = "https://www.youtube.com/watch?v=" + item['contentDetails']['videoId']


            videos.append(video)

        nextPageToken = response.get('nextPageToken')

        if not nextPageToken:
            break

    return videos


def get_video_details(videos: List[Video]):
    video_ids = [video.id for video in videos]

    i = 0
    while i < len(video_ids):

        ids = ','.join(video_ids[i:i + 50])

        request = youtube_service.videos().list(
            part='contentDetails, statistics',
            id=ids)

        response = request.execute()

        hours_pattern = re.compile(r'(\d+)H')
        minutes_pattern = re.compile(r'(\d+)M')
        seconds_pattern = re.compile(r'(\d+)S')

        for item in response['items']:
            duration = item['contentDetails']['duration']

            hours = hours_pattern.search(duration)
            minutes = minutes_pattern.search(duration)
            seconds = seconds_pattern.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            seconds = int(seconds.group(1)) if seconds else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds).total_seconds()

            videos[i].duration_in_seconds = video_seconds
            videos[i].views = item['statistics']['viewCount']

            i += 1

    return videos


if __name__ == "__main__":
    playlist = Playlist("PL-osiE80TeTu2aEvTbK-OfBidUtbSiUTL")
    crawler = PlaylistCrawler(youtube_service, playlist)
    # channel = Channel('https://www.youtube.com/channel/UCd5bqin1l35NO3BqGYs1_6A/videos')
    # crawler = ChannelCrawler(youtube_service, channel)
    Video.save_or_update(crawler.crawl())

    # Session = sessionmaker(bind=engine)
    # session = Session()
    # playlistId = "PL-osiE80TeTu2aEvTbK-OfBidUtbSiUTL"
    # videos = get_playlist_videos(playlistId)
    # videos = get_video_details(videos)
    # session.add_all(videos)
    # session.commit()
    # session.close()
