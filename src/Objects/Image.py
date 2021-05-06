import pathlib
import cv2 as cv
from src.segmentation import *


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
        self.gray = self.convert_to_gray_scale()
        self.blurred = gaussian_blurring(self.gray)
        self.divisions = []
        self.tones = []
        self.masked = []
        self.threshold_values = []
        self.thresholded = []
        self.result = None
        self.n_segments = 0

    def set_divisions(self, divisions):
        self.divisions = divisions

    def convert_to_gray_scale(self):
        return cv.cvtColor(self.cv_image, cv.COLOR_BGR2GRAY)

    def apply_segmentation(self):
        if self.divisions:  # tu mozna dodac jakis exception czy cos jesli ktos najpierw nie zrobi set_divisions
            self.tones = split_into_tones(self.blurred, brackets=self.divisions)
            self.masked, self.threshold_values, self.thresholded = apply_threshold(self.blurred, self.gray, self.tones)  # listy
            self.result = merge_pictures(self.thresholded)
            self.n_segments = len(self.thresholded)

    def update_result(self):
        self.result = merge_pictures(self.thresholded)

