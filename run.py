from apscheduler.schedulers.blocking import BlockingScheduler
from googleapiclient.discovery import build
import sys
import getopt

from channel import Channel
from crawler import PlaylistCrawler, ChannelCrawler
from models import Video
from playlist import Playlist

scheduler = BlockingScheduler()

api_key = "AIzaSyAfsclKs6PdPUhK3utgJDJx1TN6cLkpAWE"

youtube_service = build('youtube', 'v3', developerKey=api_key)


def scheduled_job(channel_url, playlist_url):
    if channel_url:
        channel = Channel(channel_url)
        crawler = ChannelCrawler(youtube_service, channel)
        Video.save_or_update(crawler.crawl())
    elif playlist_url:
        playlist = Playlist(playlist_url)
        crawler = PlaylistCrawler(youtube_service, playlist)
        Video.save_or_update(crawler.crawl())


def main(argv):
    channel = ""
    playlist = ""

    try:
        opts, args = getopt.getopt(argv, "c:p:")
    except getopt.GetoptError:
        print("Wrong Arguments. Please check the readme file again.")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ['-c']:
            print(arg)
            channel = arg
            scheduler.add_job(scheduled_job(channel, playlist), 'interval', seconds=10)
            scheduler.start()
        elif opt in ['-p']:
            print(arg)
            playlist = arg
            scheduler.add_job(scheduled_job(channel, playlist), 'interval', seconds=10)
            scheduler.start()


if __name__ == "__main__":
    main(sys.argv[1:])

