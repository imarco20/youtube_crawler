class Channel:

    def __init__(self, url):
        self.name = self.get_channel_name(url)

    @staticmethod
    def get_channel_name(url):
        url = url.split("/")
        return url[-2]
