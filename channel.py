class Channel:

    def __init__(self, url):
        self.name = self.get_channel_name(url)

    def get_channel_name(self, url):
        url = url.split("/")
        return url[-2]
