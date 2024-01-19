import os
import random
import shutil
import sys

from utils import Log

from face import Video

log = Log('face')
random.seed(0)


def main(dir_path: str):
    dir_face = dir_path + '-face'
    if not os.path.exists(dir_face):
        os.makedirs(dir_face)

    i = 0
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if not Video.is_video(file_path):
            continue
        log.debug(f'Processing {file_path}')

        dir_video = os.path.join(dir_face, file_name + '-files')

        if os.path.exists(dir_video):
            shutil.rmtree(dir_video)
        os.makedirs(dir_video)

        video = Video.from_file(file_path)
        image_list = video.get_random_images()
        for j, image in enumerate(image_list):
            image_path = os.path.join(dir_video, f'{j:03d}.png')
            image.moveto(image_path)
            image.get_faces()
        i += 1
        if i >= 5:
            break

    os.startfile(dir_face)


if __name__ == '__main__':
    dir_path = sys.argv[1]
    main(dir_path)
