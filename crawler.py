import re
import urllib.request
from datetime import timedelta

from downloader import ImageDownloader
from models import Video
from playlist import Playlist


class ChannelCrawler():

    def __init__(self, service, channel):
        self.service = service
        self.channel = channel
        self.request = self.service.channels()

    def get_playlist_id(self):
        response = self.request.list(
            part='contentDetails',
            forUsername=self.channel.name).execute()

        playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        return playlist_id

    def crawl(self):
        playlist_id = self.get_playlist_id()
        playlist = Playlist(playlist_id)
        playlist_crawler = PlaylistCrawler(self.service, playlist)
        videos = playlist_crawler.crawl()

        return videos


class PlaylistCrawler():

    def __init__(self, service, playlist: Playlist):
        self.service = service
        self.playlist = playlist
        self.request = self.service.playlistItems()
        self.video_request = self.service.videos()

    def crawl(self):
        thumbnails, originals = ImageDownloader.create_playlist_directory(self.playlist.id)
        videos = []
        next_page_token = None

        while True:
            response = self.request_playlist_page(next_page_token)

            for item in response['items']:
                video = Video()
                self.set_video_details(video, item, originals, thumbnails)
                videos.append(video)

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        self.set_video_stats(videos)

        return videos

    def set_video_details(self, video, item, originals, thumbnails):
        video.id = item['contentDetails']['videoId']
        video.title = item['snippet']['title']
        video.thumbnail_image_path, video.thumbnail_image_url = self.set_video_thumbnail(item, thumbnails,
                                                                                         video)
        video.fullsized_image_path, video.fullsized_image_url = self.set_video_original_image(item, originals,
                                                                                              video)
        video.url = "https://www.youtube.com/watch?v=" + item['contentDetails']['videoId']

    def set_video_original_image(self, item, originals, video):
        try:
            fullsized_url = item['snippet']['thumbnails']['maxres']['url']
            fullsized_path = originals + "/" + video.id + ".jpg"
            urllib.request.urlretrieve(fullsized_url, fullsized_path)

        except KeyError:
            fullsized_url = None
            fullsized_path = None
        return fullsized_path, fullsized_url

    def set_video_thumbnail(self, item, thumbnails, video):
        try:
            thumbnail_url = item['snippet']['thumbnails']['default']['url']
            thumbnail_path = thumbnails + "/" + video.id + ".jpg"
            urllib.request.urlretrieve(thumbnail_url, thumbnail_path)

        except KeyError:
            thumbnail_url = None
            thumbnail_path = None
        return thumbnail_path, thumbnail_url

    def request_playlist_page(self, next_page_token):
        response = self.request.list(
            part='snippet, contentDetails',
            playlistId=self.playlist.id,
            maxResults=50,
            pageToken=next_page_token).execute()

        return response

    def set_video_stats(self, videos):

        video_ids = [video.id for video in videos]

        i = 0
        while i < len(video_ids):

            ids = ','.join(video_ids[i:i + 50])

            response = self.request_video_stats(ids)

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

    def request_video_stats(self, ids):
        response = self.video_request.list(
            part='contentDetails, statistics',
            id=ids).execute()

        return response
