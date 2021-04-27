import pathlib
import cv2 as cv


def set_path(file_name):
    file_path = '..' + "\\Photos\\" + file_name
    return file_path


class Image:
    def __init__(self, file_name):
        self.full_path = set_path(file_name)
        self.cv_image = cv.imread(self.full_path)
        self.height = self.cv_image.shape[0]
        self.width = self.cv_image.shape[1]
        self.channels = self.cv_image.shape[2]

    def convert_to_gray_scale(self):
        pass

    def gaussian_blur(self):
        pass
