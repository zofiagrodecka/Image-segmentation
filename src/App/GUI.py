from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolButton, QSlider, QPushButton, QApplication, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSlot
import copy
from src.segmentation import change_threshold


class MainWindow(QWidget):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Image segmentation")
        """self.palette = self.palette()
        self.palette.setColor(self.backgroundRole(), Qt.gray)
        self.setPalette(self.palette)"""
        self.desktop = QApplication.desktop()
        self.display_width = 640  # self.desktop.screenGeometry().width()/2
        self.display_height = 480  # self.desktop.screenGeometry().height()/2
        self.x = 20
        self.y = 50
        self.height = self.display_height + 10
        self.width = self.display_width*2

        self.input_label = QLabel(self)
        self.input_label.setText('Segments: ')
        self.input = QLineEdit(self)
        self.result_label = QLabel(self)
        self.result_label.setText('Result: ')

        self.ok_button = QPushButton('OK')
        self.left_button = QToolButton()
        self.right_button = QToolButton()
        self.reset_button = QPushButton('Reset')

        self.displayed_segment_index = 0
        self.image_label = QLabel(self)
        self.result_image_label = QLabel(self)
        self.image = image
        self.initial_image = None
        self.qt_image = self.convert_cv_qt(self.image.gray)
        self.res_image = self.convert_cv_qt(self.image.blurred)

        self.threshold_slider = QSlider(Qt.Horizontal)

        self.layout = QGridLayout()
        self.initialize()

    def initialize(self):
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.input.setText("51 102 153 204")
        self.result_label.setFont(QFont('Times', 12))
        self.image_label.setPixmap(self.qt_image)
        self.result_image_label.setPixmap(self.res_image)
        self.initialize_slider()
        self.initialize_buttons()
        self.layout.addWidget(self.input_label, 0, 0, 1, 2)  # w k ( row span, col span)
        self.layout.addWidget(self.input, 1, 0, 1, 2)
        self.layout.addWidget(self.ok_button, 1, 2, Qt.AlignLeft)
        self.layout.addWidget(self.left_button, 2, 0, Qt.AlignRight)
        self.layout.addWidget(self.right_button, 2, 1, Qt.AlignLeft)
        self.layout.addWidget(self.result_label, 2, 2, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.image_label, 3, 0, 1, 2)
        self.layout.addWidget(self.result_image_label, 3, 2, 1, 2)
        self.layout.addWidget(self.threshold_slider, 4, 0, 1, 2)
        self.layout.addWidget(self.reset_button, 5, 0, 1, 2, Qt.AlignCenter)
        self.setLayout(self.layout)

    def initialize_buttons(self):
        self.ok_button.setToolTip('Confirm settings')
        self.ok_button.clicked.connect(self.get_input)
        self.left_button.setToolTip('Previous segment')
        self.left_button.setArrowType(Qt.LeftArrow)
        self.left_button.clicked.connect(self.left_on_click)
        self.right_button.setToolTip('Next segment')
        self.right_button.setArrowType(Qt.RightArrow)
        self.right_button.clicked.connect(self.right_on_click)
        self.reset_button.setToolTip('Reset settings')
        self.reset_button.clicked.connect(self.reset_calculations)

    def initialize_slider(self):
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(0)
        self.threshold_slider.valueChanged[int].connect(self.change_threshold_value)

    def convert_cv_qt(self, cv_img):
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def get_input(self):
        print(self.input.text())
        segments = [int(i) for i in self.input.text().split(' ')]
        print(segments)
        self.image.set_divisions(segments)
        self.image.apply_segmentation()
        self.initial_image = copy.deepcopy(self.image)
        self.displayed_segment_index = 0  # ??
        self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
        self.update_image(self.res_image, self.image.result, self.result_image_label)
        self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

    def left_on_click(self):
        if self.displayed_segment_index > 0:
            self.qt_image = self.convert_cv_qt(self.image.thresholded[self.prev_segment_index()])
            self.displayed_segment_index -= 1
            self.image_label.setPixmap(self.qt_image)
            self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

    def right_on_click(self):
        if self.displayed_segment_index < self.image.n_segments-1:  # indeksowane od 0
            self.qt_image = self.convert_cv_qt(self.image.thresholded[self.next_segment_index()])
            self.displayed_segment_index += 1
            self.image_label.setPixmap(self.qt_image)
            self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

    def change_threshold_value(self, value):
        print(value)
        before_change = self.image.masked[self.displayed_segment_index]
        changed_image = change_threshold(before_change, value)
        self.image.thresholded[self.displayed_segment_index] = changed_image
        self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
        self.image.threshold_values[self.displayed_segment_index] = value
        self.image.update_result()
        self.update_image(self.res_image, self.image.result, self.result_image_label)

    def prev_segment_index(self):
        return self.displayed_segment_index-1

    def next_segment_index(self):
        return self.displayed_segment_index+1

    def update_image(self, old_image, new_image, label):
        old_image = self.convert_cv_qt(new_image)
        label.setPixmap(old_image)

    def reset_calculations(self):
        self.image.thresholded[self.displayed_segment_index] = self.initial_image.thresholded[self.displayed_segment_index]
        self.change_threshold_value(self.initial_image.threshold_values[self.displayed_segment_index])
        self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

