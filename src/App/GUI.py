from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSlot


class MainWindow(QWidget):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Image segmentation")
        self.display_width = 640
        self.display_height = 480
        self.x = 20
        self.y = 40
        self.height = self.display_height + 10
        self.width = self.display_width*2
        self.left_button = QToolButton()
        self.right_button = QToolButton()
        self.image_label = QLabel(self)
        self.result_image_label = QLabel(self)
        self.text_label = QLabel('Label')
        self.displayed_segment_index = 0

        self.layout = QGridLayout()
        self.image = image
        self.qt_image = self.convert_cv_qt(self.image.thresholded[self.displayed_segment_index])
        self.res_image = self.convert_cv_qt(self.image.result)
        self.initialize()

    def initialize(self):
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.image_label.setPixmap(self.qt_image)
        self.result_image_label.setPixmap(self.res_image)
        self.initialize_buttons()
        self.layout.addWidget(self.left_button, 1, 0, Qt.AlignRight)  # w 0 wierszu będzie input z przedzialami
        self.layout.addWidget(self.right_button, 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.image_label, 2, 0, 1, 2)  # w k ( row span, col span)
        self.layout.addWidget(self.result_image_label, 2, 2, 1, 2)
        self.layout.addWidget(self.text_label, 3, 0)
        self.setLayout(self.layout)

    def initialize_buttons(self):
        self.left_button.setToolTip('Previous segment')
        self.left_button.setArrowType(Qt.LeftArrow)
        self.left_button.clicked.connect(self.left_on_click)
        self.right_button.setToolTip('Next segment')
        self.right_button.setArrowType(Qt.RightArrow)
        self.right_button.clicked.connect(self.right_on_click)

    def convert_cv_qt(self, cv_img):
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    @pyqtSlot()
    def left_on_click(self):
        if self.displayed_segment_index > 0:
            self.qt_image = self.convert_cv_qt(self.image.thresholded[self.prev_segment_index()])
            self.displayed_segment_index -= 1
            self.image_label.setPixmap(self.qt_image)

    @pyqtSlot()
    def right_on_click(self):
        if self.displayed_segment_index < self.image.n_segments-1:  # indeskowane od 0
            self.qt_image = self.convert_cv_qt(self.image.thresholded[self.next_segment_index()])
            self.displayed_segment_index += 1
            self.image_label.setPixmap(self.qt_image)

    def prev_segment_index(self):
        return self.displayed_segment_index-1

    def next_segment_index(self):
        return self.displayed_segment_index+1
