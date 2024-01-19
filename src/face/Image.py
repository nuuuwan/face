import shutil

import cv2
from utils import File, Log

log = Log('Image')


class Image(File):
    def moveto(self, path: str):
        shutil.move(self.path, path)
        self.path = path

    @property
    def img(self):
        return cv2.imread(self.path)

    def get_faces(self) -> list['Image']:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_profileface.xml'
        )

        img = self.img

        grayscale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            grayscale_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        if len(faces) > 0:
            log.debug(f'Found {len(faces)} faces in {self.path}.')
        image_list = []
        for i, (x, y, w, h) in enumerate(faces):
            face = img[y: y + h, x: x + w]

            face_image_path = self.path + f'-face_{i:02d}.png'
            cv2.imwrite(face_image_path, face)
            image = Image(face_image_path)
            image_list.append(image)
        return image_list
