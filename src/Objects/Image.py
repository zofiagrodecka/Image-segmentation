import cv2 as cv
from src.App.SegmentationManager import *


class Image:
    def __init__(self, file_name, explore_files=False):
        if explore_files:
            self.full_path = file_name
        else:
            self.full_path = self.set_path(file_name)
        self.cv_image = cv.imread(self.full_path)
        self.height = self.cv_image.shape[0]
        self.width = self.cv_image.shape[1]
        self.channels = self.cv_image.shape[2]
        self.manager = SegmentationManager()
        self.gray = self.manager.converting_to_gray_scale(self.cv_image)
        self.blurred = self.manager.gaussian_blurring(self.gray)
        self.divisions = []
        self.tones = []
        self.masked = []
        self.threshold_values = []
        self.thresholded = []
        self.result = None
        self.empty_tones = []
        self.n_segments = 0
        self.has_applied_segmentation = False

    @staticmethod
    def set_path(file_name):
        file_path = '..' + "\\Photos\\" + file_name
        return file_path

    def set_divisions(self, divisions):
        self.divisions = divisions

    def convert_to_gray_scale(self):
        return self.manager.converting_to_gray_scale(self.cv_image)

    def apply_segmentation(self):
        if self.divisions:
            self.tones = self.manager.split_into_tones(self.blurred, brackets=self.divisions)
            self.masked, self.threshold_values, self.thresholded, self.empty_tones = self.manager.apply_threshold(self.blurred, self.gray, self.tones)
            self.result = self.manager.merge_pictures(self.thresholded)
            self.n_segments = len(self.thresholded)
            self.has_applied_segmentation = True

    def update_result(self):
        self.result = self.manager.merge_pictures(self.thresholded)

