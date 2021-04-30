import os


class ImageDownloader:
    base_dir = os.path.join(os.path.expanduser('~'), 'Downloads') + "/" + "Crawler"

    @classmethod
    def create_playlist_directory(cls, playlist_id):
        cls.create_dir(cls.base_dir)

        playlist_dir = cls.base_dir + "/" + playlist_id
        cls.create_dir(playlist_dir)

        thumbnails = playlist_dir + "/thumbnails"
        originals = playlist_dir + "/original_images"

        cls.create_dir(thumbnails)
        cls.create_dir(originals)

        return thumbnails, originals

    @classmethod
    def create_dir(cls, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
