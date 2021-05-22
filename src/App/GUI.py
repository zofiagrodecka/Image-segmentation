from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolButton, QSlider, QPushButton, QApplication, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import copy
from src.App.segmentation import change_threshold
import tkinter.filedialog
import cv2 as cv


class MainWindow(QWidget):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("Image segmentation")
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
        self.segments = None
        self.segments_label = QLabel(self)
        self.segments_label.setText('Showed tones in range: None')
        self.result_label = QLabel(self)
        self.result_label.setText('Result: ')
        self.threshold_label = QLabel(self)
        self.threshold_label.setText('Threshold value: None')
        self.pixels_label = QLabel(self)
        self.pixels_label.setText('Show pixels with value: ')
        self.input_pixels = QLineEdit(self)
        self.pixels_accuracy_label = QLabel(self)
        self.pixels_accuracy_label.setText(' + - ')
        self.input_accuracy = QLineEdit(self)

        self.default_text_button = QPushButton('Remember input')
        self.ok_button = QPushButton('OK')
        self.ok_button2 = QPushButton('OK')
        self.left_button = QToolButton()
        self.right_button = QToolButton()
        self.reset_button = QPushButton('Reset')
        self.save_button = QPushButton('Save')
        self.blurred_button = QPushButton('Blurred image')

        self.pixels_value = None
        self.pixels_accuracy = None

        self.displayed_segment_index = 0
        self.image_label = QLabel(self)
        self.result_image_label = QLabel(self)
        self.image = image
        self.initial_image = None
        self.qt_image = self.convert_cv_qt(self.image.gray, self.image_label)
        # self.qt_image_pixmap = QPixmap.fromImage(self.qt_image)
        self.res_image = self.convert_cv_qt(self.image.blurred, self.result_image_label)
        # self.res_image_pixmap = QPixmap.fromImage(self.res_image)

        self.threshold_slider = QSlider(Qt.Horizontal)

        self.layout = QGridLayout()
        self.initialize()

    def initialize(self):
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.input.setText("51 102 153 204")
        self.input_accuracy.setText("0")
        self.set_font_to_labels()
        qt_image_pixmap = QPixmap.fromImage(self.qt_image)
        self.image_label.setPixmap(qt_image_pixmap)
        res_image_pixmap = QPixmap.fromImage(self.res_image)
        self.result_image_label.setPixmap(res_image_pixmap)
        self.result_image_label.mousePressEvent = self.get_pixel
        self.initialize_slider()
        self.initialize_buttons()
        self.layout.addWidget(self.input_label, 0, 0, 1, 2)  # w k ( row span, col span)
        self.layout.addWidget(self.input, 1, 0, 1, 2)
        self.layout.addWidget(self.ok_button, 1, 2, Qt.AlignLeft)
        self.layout.addWidget(self.result_label, 2, 2, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.segments_label, 3, 0, Qt.AlignLeft)
        self.layout.addWidget(self.left_button, 3, 0, Qt.AlignRight)
        self.layout.addWidget(self.right_button, 3, 1, Qt.AlignLeft)
        self.layout.addWidget(self.pixels_label, 3, 2)
        self.layout.addWidget(self.input_pixels, 3, 3, Qt.AlignLeft)
        self.layout.addWidget(self.pixels_accuracy_label, 3, 3, Qt.AlignRight)
        self.layout.addWidget(self.input_accuracy, 3, 4, Qt.AlignCenter)
        self.layout.addWidget(self.ok_button2, 3, 5, Qt.AlignLeft)
        self.layout.addWidget(self.image_label, 4, 0, 1, 2)
        self.layout.addWidget(self.result_image_label, 4, 2, 1, 4)
        self.layout.addWidget(self.threshold_slider, 5, 0, 1, 2)
        self.layout.addWidget(self.threshold_label, 6, 1, Qt.AlignRight)
        self.layout.addWidget(self.reset_button, 6, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.save_button, 6, 2, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.blurred_button, 6, 4, 1, 2, Qt.AlignCenter)
        self.setLayout(self.layout)

    def initialize_buttons(self):
        self.ok_button.setToolTip('Confirm settings')
        self.ok_button.clicked.connect(self.get_input_segments)
        self.ok_button2.setToolTip('Confirm pixel values to be shown')
        self.ok_button2.clicked.connect(self.get_input_pixels_value)
        self.left_button.setToolTip('Previous segment')
        self.left_button.setArrowType(Qt.LeftArrow)
        self.left_button.clicked.connect(self.left_on_click)
        self.left_button.setDisabled(True)
        self.right_button.setToolTip('Next segment')
        self.right_button.setArrowType(Qt.RightArrow)
        self.right_button.clicked.connect(self.right_on_click)
        self.right_button.setDisabled(True)
        self.reset_button.setToolTip('Reset settings')
        self.reset_button.clicked.connect(self.reset_calculations)
        self.reset_button.setDisabled(True)
        self.save_button.setToolTip('Save the result')
        self.save_button.clicked.connect(self.save_result)
        self.blurred_button.setToolTip('Show blurred image')
        self.blurred_button.clicked.connect(self.show_blurred)

    def initialize_slider(self):
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(0)
        self.threshold_slider.valueChanged[int].connect(self.change_threshold_value)
        self.threshold_slider.setDisabled(True)

    def set_font_to_labels(self):
        self.input_label.setFont(QFont('Times', 11))
        self.segments_label.setFont(QFont('Times', 11))
        self.result_label.setFont(QFont('Times', 12))
        self.threshold_label.setFont(QFont('Times', 11))
        self.pixels_label.setFont(QFont('Times', 11))

    def convert_cv_qt(self, cv_img, label):
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        label.resize(p.width(), p.height())
        return p

    def show_blurred(self):
        self.update_image(self.res_image, self.image.blurred, self.result_image_label)

    def get_pixel(self, event):
        x = event.pos().x()
        y = event.pos().y()
        pixels_accuracy = int(self.input_accuracy.text())
        pixels_value = QColor(self.res_image.pixel(x, y)).value()
        self.show_pixels(pixels_value, pixels_accuracy)
        print(pixels_value, x, y)

    def get_input_pixels_value(self):
        pixels_value = int(self.input_pixels.text())
        pixels_accuracy = int(self.input_accuracy.text())
        self.show_pixels(pixels_value, pixels_accuracy)

    def show_pixels(self, value, accuracy):
        for x in range(self.image.height):
            for y in range(self.image.width):
                if abs(self.image.blurred.item(x, y) - value) <= accuracy:
                    self.image.blurred.itemset((x, y), 255)  # koloruje piksel na bialo
        self.update_image(self.res_image, self.image.blurred, self.result_image_label)
        self.image.reblur()

    def get_input_segments(self):
        if self.input.text()[0] == '0':
            self.segments = [int(i) for i in self.input.text().split(' ')]
        else:
            self.segments = [0] + [int(i) for i in self.input.text().split(' ')]

        if self.segments[len(self.segments)-1] != 255:
            self.segments.append(255)

        self.image.set_divisions(self.segments)
        self.image.apply_segmentation()
        self.initial_image = copy.deepcopy(self.image)
        self.displayed_segment_index = 0
        self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
        self.update_image(self.res_image, self.image.result, self.result_image_label)
        self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])
        self.update_label(self.segments_label,
                          'Showed tones in range: [' + str(self.segments[self.displayed_segment_index]) + ', '
                          + str(self.segments[self.displayed_segment_index + 1]) + ']')
        self.enable_widgets()

    def enable_widgets(self):
        self.reset_button.setDisabled(False)
        self.right_button.setDisabled(False)
        self.left_button.setDisabled(False)
        self.threshold_slider.setDisabled(False)

    def left_on_click(self):
        if self.displayed_segment_index > 0:
            self.update_image(self.qt_image, self.image.thresholded[self.prev_segment_index()], self.image_label)
            self.displayed_segment_index -= 1
            self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])
            self.update_label(self.segments_label,
                              'Showed tones in range: [' + str(self.segments[self.displayed_segment_index]) + ', '
                              + str(self.segments[self.displayed_segment_index + 1]) + ']')

    def right_on_click(self):
        if self.displayed_segment_index < self.image.n_segments-1:  # indeksowane od 0
            self.update_image(self.qt_image, self.image.thresholded[self.next_segment_index()], self.image_label)
            self.displayed_segment_index += 1
            self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])
            self.update_label(self.segments_label,
                              'Showed tones in range: [' + str(self.segments[self.displayed_segment_index]) + ', '
                              + str(self.segments[self.displayed_segment_index + 1]) + ']')

    def change_threshold_value(self, value):
        before_change = self.image.masked[self.displayed_segment_index]
        changed_image = change_threshold(before_change, value)
        self.image.thresholded[self.displayed_segment_index] = changed_image
        self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
        self.image.threshold_values[self.displayed_segment_index] = value
        self.image.update_result()
        self.update_image(self.res_image, self.image.result, self.result_image_label)
        self.update_label(self.threshold_label, 'Threshold value: ' + str(value))

    def prev_segment_index(self):
        return self.displayed_segment_index-1

    def next_segment_index(self):
        return self.displayed_segment_index+1

    def update_image(self, old_image, new_image, label):
        old_image = self.convert_cv_qt(new_image, label)
        pixmap = QPixmap.fromImage(old_image)
        label.setPixmap(pixmap)

    def update_label(self, label, text):
        label.setText(text)

    def reset_calculations(self):
        self.image.thresholded[self.displayed_segment_index] = self.initial_image.thresholded[self.displayed_segment_index]
        self.change_threshold_value(self.initial_image.threshold_values[self.displayed_segment_index])
        self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

    def save_result(self):
        f = tkinter.filedialog.asksaveasfile(mode='wb', defaultextension='png', initialdir="../Results")
        if f is not None and self.image.result is not None:
            cv.imwrite(f.name, self.image.result, [cv.IMWRITE_PNG_BILEVEL, 1])
            f.close()
        elif self.image.result is None:
            cv.imwrite(f.name, self.image.blurred)
