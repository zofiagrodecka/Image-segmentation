import pathlib

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject
import sys
import cv2 as cv


class MainWindow(QWidget):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Image segmentation")
        self.display_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.result_image_label = QLabel(self)
        self.text_label = QLabel('Label')

        self.layout = QGridLayout()
        self.qt_img = self.convert_cv_qt(image.gaussed)
        # cv_im = cv.imread('image.jpg', cv.IMREAD_GRAYSCALE)
        self.res_img = self.convert_cv_qt(image.result)
        self.initialize()

        # don't need the grey image now
        # grey = QPixmap(self.disply_width, self.display_height)
        # grey.fill(QColor('darkGray'))
        # self.image_label.setPixmap(grey)

    def initialize(self):
        self.layout.addWidget(self.image_label, 0, 0)
        self.layout.addWidget(self.result_image_label, 0, 1)
        self.layout.addWidget(self.text_label, 1, 0)
        self.setLayout(self.layout)
        self.image_label.setPixmap(self.qt_img)
        self.result_image_label.setPixmap(self.res_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        # gray_image = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

