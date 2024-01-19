import os
import random
import tempfile

import cv2
from utils import File, Log

from face.Image import Image

log = Log('Video')


class Video(File):
    DEFAULT_NUM_FRAMES = 10

    @staticmethod
    def is_video(file_path: str) -> bool:
        if file_path.endswith('.mp4'):
            return True
        return False

    @staticmethod
    def from_file(file_path: str):
        if not Video.is_video(file_path):
            raise Exception(f'Not a video file: {file_path}')
        return Video(file_path)

    def get_random_images(
        self, num_frames: int = DEFAULT_NUM_FRAMES
    ) -> list[Image]:
        video = cv2.VideoCapture(self.path)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        log.debug(f'{total_frames=}')
        random_frames = random.sample(range(0, total_frames), num_frames)
        output_dir = tempfile.mkdtemp()
        log.debug(f'{output_dir=}')
        image_list = []
        for i, frame_num in enumerate(random_frames):
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = video.read()
            if ret:
                image_path = os.path.join(output_dir, f'frame_{i}.jpg')
                cv2.imwrite(image_path, frame)
                image = Image(image_path)
                image_list.append(image)

        video.release()
        return image_list
