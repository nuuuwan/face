import shutil

from utils import File


class Image(File):
    def moveto(self, path: str):
        shutil.move(self.path, path)
        self.path = path
