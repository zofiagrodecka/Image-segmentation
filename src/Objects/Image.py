import pathlib
import cv2 as cv
from src.segmentation import *


def set_path(file_name):
    file_path = '..' + "\\Photos\\" + file_name
    return file_path


class Image:
    def __init__(self, file_name, divisions):
        self.full_path = set_path(file_name)
        self.cv_image = cv.imread(self.full_path)
        self.height = self.cv_image.shape[0]
        self.width = self.cv_image.shape[1]
        self.channels = self.cv_image.shape[2]
        self.gray = self.convert_to_gray_scale()
        self.gaussed = gaussian_blurring(self.gray)
        self.tones = split_into_tones(self.gaussed, brackets=divisions)
        self.masked, self.thresholded = apply_threshold(self.gaussed, self.gray, self.tones)  # listy
        self.result = merge_pictures(self.thresholded)
        self.n_segments = len(self.thresholded)

    def convert_to_gray_scale(self):
        return cv.cvtColor(self.cv_image, cv.COLOR_BGR2GRAY)

