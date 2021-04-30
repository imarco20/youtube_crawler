class Playlist:

    def __init__(self, url):
        self.id = self.get_playlist_id_from_url(url)


    def get_playlist_id_from_url(self, url):
        url = url.split("=")[-1]
        return url
