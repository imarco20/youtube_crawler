from apscheduler.schedulers.blocking import BlockingScheduler
from googleapiclient.discovery import build
import sys
import getopt
import os

from channel import Channel
from crawler import PlaylistCrawler, ChannelCrawler
from models import Video
from playlist import Playlist

scheduler = BlockingScheduler()

api_key = os.environ.get("api_key")

youtube_service = build('youtube', 'v3', developerKey=api_key)

channel_url = ""
playlist_url = ""

@scheduler.scheduled_job('interval', seconds=10)
def scheduled_job():
    if channel_url:
        channel = Channel(channel_url)
        crawler = ChannelCrawler(youtube_service, channel)
        Video.save_or_update(crawler.crawl())
    elif playlist_url:
        playlist = Playlist(playlist_url)
        crawler = PlaylistCrawler(youtube_service, playlist)
        Video.save_or_update(crawler.crawl())


def main(argv):
    global channel_url
    global playlist_url

    try:
        opts, args = getopt.getopt(argv, "c:p:")
    except getopt.GetoptError:
        print("Wrong Arguments. Please check the readme file again.")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-c']:
            print(arg)
            channel = arg
        elif opt in ['-p']:
            print(arg)
            playlist = arg
    scheduler.start()


if __name__ == "__main__":
    main(sys.argv[1:])

