import pathlib

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QHBoxLayout
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
        # create the label that holds the image
        self.image_label = QLabel(self)
        # create a text label
        self.textLabel = QLabel('Label')

        self.layout = QVBoxLayout()
        # load the test image - we really should have checked that this worked!
        # convert the image to Qt format
        self.qt_img = self.convert_cv_qt(image.cv_image)
        self.initialize()

        # don't need the grey image now
        # grey = QPixmap(self.disply_width, self.display_height)
        # grey.fill(QColor('darkGray'))
        # self.image_label.setPixmap(grey)


    def initialize(self):
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.textLabel)
        self.setLayout(self.layout)
        self.image_label.setPixmap(self.qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        gray_image = cv.cvtColor(cv_img, cv.COLOR_BGR2GRAY)
        h, w = gray_image.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(gray_image.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

