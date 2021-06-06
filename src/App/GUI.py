from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QToolButton, QSlider, QPushButton, QApplication, QLineEdit, \
    QDesktopWidget, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import copy

from src.App.segmentation import change_threshold, change_blur
import tkinter.filedialog
import cv2 as cv
import numpy as np

from src.Objects.Image import Image
from src.Objects.JsonParser import JsonParser


class MainWindow(QWidget):
    def __init__(self, image):
        super().__init__()
        self.setWindowTitle("To-Bit-Map")
        self.launch_settings = JsonParser()

        self.display_width = 880
        self.display_height = 500

        self.height = int(self.display_height * 1.3)
        self.width = self.display_width * 2

        self.desktop = QApplication.desktop()
        self.x = (self.desktop.screenGeometry().width() - self.width) // 2
        self.y = (self.desktop.screenGeometry().height() - self.height) // 2

        self.input_label = QLabel(self)
        self.input_label.setText('Segments: ')
        self.input = QLineEdit(self)
        self.segments = None
        self.segments_label = QLabel(self)
        self.threshold_label = QLabel(self)
        self.blur_label = QLabel(self)
        self.blur_label.setText('Blur value: 10')
        self.pixels_label = QLabel(self)
        self.pixels_label.setText('Pixel Value: ')
        self.input_pixels = QLineEdit(self)
        self.pixels_accuracy_label = QLabel(self)
        self.pixels_accuracy_label.setText('Accuracy: ')
        self.input_accuracy = QLineEdit(self)
        self.no_pixels_label = QLabel()
        self.no_image_label = QLabel()

        self.ok_button = QPushButton('OK')
        self.ok_button2 = QPushButton('Show')
        self.left_button = QToolButton()
        self.right_button = QToolButton()
        self.reset_button = QPushButton('Reset')
        self.save_button = QPushButton('Save')
        self.remember_button = QPushButton('Remember')
        self.forget_button = QPushButton('Forget')
        self.load_button = QPushButton('Open')
        self.recent_button = QPushButton('Open recent')

        self.pixels_value = None
        self.pixels_accuracy = None
        self.current_blur = 10

        self.displayed_segment_index = 0
        self.image_label = QLabel(self)
        self.result_image_label = QLabel(self)
        self.image = image
        self.initial_image = None
        self.qt_image = self.convert_cv_qt(self.image.gray, self.image_label)
        self.res_image = self.convert_cv_qt(self.image.blurred, self.result_image_label)

        self.threshold_slider = QSlider(Qt.Horizontal)
        self.blur_slider = QSlider(Qt.Horizontal)

        self.dialog_window = QMessageBox()
        self.dialog_window.setIcon(QMessageBox.Warning)
        self.dialog_window.setWindowTitle("WARNING")

        self.layout = QGridLayout()
        self.initialize()

    def initialize(self):
        self.setGeometry(self.x, self.y, self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        if self.launch_settings.file_exists:
            res = self.launch_settings.import_from_json()
            self.input.setText(res[0])
            self.current_blur = res[1]
        else:
            self.input.setText("51 102 153 204")
        self.input_accuracy.setText("10")
        self.set_font_to_labels()
        qt_image_pixmap = QPixmap.fromImage(self.qt_image)
        self.image_label.setPixmap(qt_image_pixmap)
        res_image_pixmap = QPixmap.fromImage(self.res_image)
        self.result_image_label.setPixmap(res_image_pixmap)
        self.result_image_label.mousePressEvent = self.get_pixel
        self.initialize_sliders()
        self.initialize_buttons()

        # w k ( row span, col span )
        self.layout.addWidget(self.input_label, 1, 0, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.input, 1, 1, 1, 2)
        self.layout.addWidget(self.ok_button, 1, 3, 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.remember_button, 1, 3, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.pixels_label, 1, 4, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.input_pixels, 1, 5, 1, 2)
        self.layout.addWidget(self.forget_button, 2, 3, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.pixels_accuracy_label, 2, 4, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.input_accuracy, 2, 5, 1, 2)
        self.layout.addWidget(self.ok_button2, 1, 7, 2, 1, Qt.AlignLeft)
        self.layout.addWidget(self.segments_label, 2, 0, 1, 1)
        self.layout.addWidget(self.left_button, 2, 1, 1, 1, Qt.AlignRight)
        self.layout.addWidget(self.right_button, 2, 2, 1, 1, Qt.AlignLeft)
        self.layout.addWidget(self.no_image_label, 4, 0, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.image_label, 4, 0, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.no_pixels_label, 4, 4, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.result_image_label, 4, 4, 1, 4, Qt.AlignCenter)
        self.layout.addWidget(self.threshold_slider, 5, 0, 1, 4)
        self.layout.addWidget(self.blur_slider, 5, 4, 1, 4)
        self.layout.addWidget(self.threshold_label, 6, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.reset_button, 6, 1, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.blur_label, 6, 4, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.save_button, 6, 5, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.load_button, 6, 6, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.recent_button, 6, 7, 1, 1, Qt.AlignCenter)
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
        self.remember_button.setToolTip('Remember segments')
        self.remember_button.clicked.connect(self.remember_settings)
        self.forget_button.setToolTip('Forget remembered segments')
        self.forget_button.clicked.connect(self.forget_settings)
        self.load_button.setToolTip('Load new image')
        self.load_button.clicked.connect(lambda: self.load_image())
        self.recent_button.setToolTip('Open the last image to which segmentation was applied')
        self.recent_button.clicked.connect(self.open_recent)

    def initialize_sliders(self):
        self.threshold_slider.setRange(0, 255)
        self.threshold_slider.setValue(0)
        self.threshold_slider.valueChanged[int].connect(self.change_threshold_value)
        self.threshold_slider.setDisabled(True)
        self.blur_slider.setRange(1, 50)
        self.blur_slider.setValue(self.current_blur)
        self.change_blur_value(self.current_blur)
        self.blur_slider.valueChanged[int].connect(self.change_blur_value)

    def set_font_to_labels(self):
        self.input_label.setFont(QFont('Times', 11))
        self.segments_label.setFont(QFont('Times', 11))
        self.threshold_label.setFont(QFont('Times', 11))
        self.blur_label.setFont(QFont('Times', 11))
        self.pixels_label.setFont(QFont('Times', 11))
        self.pixels_accuracy_label.setFont(QFont('Times', 11))
        self.no_pixels_label.setFont(QFont('Times', 16))
        self.no_image_label.setFont(QFont('Times', 16))

    def convert_cv_qt(self, cv_img, label):
        h, w = cv_img.shape
        bytes_per_line = w
        convert_to_Qt_format = QtGui.QImage(cv_img.data, w, h, bytes_per_line, QtGui.QImage.Format_Grayscale8)
        scaled = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        label.resize(scaled.width(), scaled.height())
        return scaled

    def get_pixel(self, event):
        x = event.pos().x()
        y = event.pos().y()
        pixels_accuracy = int(self.input_accuracy.text())
        pixels_value = QColor(self.res_image.pixel(x, y)).value()
        self.show_pixels(pixels_value, pixels_accuracy)
        self.input_pixels.setText(str(pixels_value))

    def get_input_pixels_value(self):
        try:
            pixels_value = int(self.input_pixels.text())
            pixels_accuracy = int(self.input_accuracy.text())
            if pixels_value < 0 or pixels_value > 255:
                print("You entered a number:", pixels_value, "that is out of range [0, 255]")
                self.show_warning_window("You entered a number: " + str(pixels_value) + " that is out of range [0, 255]")
            elif pixels_accuracy < 0 or pixels_accuracy > 255:
                print("You entered a number:", pixels_accuracy, "that is out of range [0, 255]")
                self.show_warning_window("You entered a number: " + str(pixels_accuracy) + " that is out of range [0, 255]")
            else:
                self.show_pixels(pixels_value, pixels_accuracy)
        except ValueError as ve:
            print(type(ve), ve)
            self.show_warning_window("You entered a non-numeric value")
        except AssertionError as ae:
            print(type(ae), ae)

    def show_pixels(self, value, accuracy):
        counter = 0
        for x in range(self.image.height):
            for y in range(self.image.width):
                if abs(self.image.blurred.item(x, y) - value) <= accuracy:
                    self.image.blurred.itemset((x, y), 255)  # koloruje piksel na bialo
                    counter += 1
        self.update_image(self.res_image, self.image.blurred, self.result_image_label)
        self.image.blurred = change_blur(self.image.gray, self.current_blur)
        if counter == 0:
            self.update_label(self.no_pixels_label,
                              "<font color='red'><b>No pixels of value: </b></font>" +
                              str(value) +
                              " +- " + str(accuracy))
            self.no_pixels_label.setStyleSheet("background-color: white")
        else:
            self.update_label(self.no_pixels_label, "")

    def get_input_segments(self):
        num_in_range = True
        input_text = self.input.text()
        try:
            if len(self.input.text().split()) == 0:
                self.show_warning_window("Enter non-blank segmentation values")
                return
            if input_text[0] == '0':
                self.segments = [int(i) for i in input_text.split()]
            else:
                self.segments = [0] + [int(i) for i in input_text.split()]

            if self.segments[len(self.segments)-1] != 255:
                self.segments.append(255)

            self.segments.sort()

            for num in self.segments:
                if num < 0 or num > 255:
                    error_value = num
                    num_in_range = False

            if num_in_range:
                self.image.set_divisions(self.segments)
                self.image.apply_segmentation()
                self.initial_image = copy.deepcopy(self.image)
                self.displayed_segment_index = 0
                if self.image.threshold_values[self.displayed_segment_index] is None:
                    self.show_black_image()
                else:
                    self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
                    self.update_image(self.res_image, self.image.result, self.result_image_label)
                    self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])

                self.update_label(self.segments_label,
                                  'Tones in range: ' + str(self.segments[self.displayed_segment_index]) + ' - '
                                  + str(self.segments[self.displayed_segment_index + 1]) + ' ')
                self.update_label(self.no_pixels_label, "")
                self.enable_widgets()
                self.launch_settings.export_image(self.image.full_path)
            else:
                print("You entered a number:", error_value, "that is out of range [0, 255]")
                self.show_warning_window("You entered a number: " + str(error_value) + " that is out of range [0, 255]")
        except ValueError as ve:
            print(ve)
            self.show_warning_window("You entered a non-numeric value in: " + self.input.text())

    def enable_widgets(self):
        self.reset_button.setDisabled(False)
        self.right_button.setDisabled(False)
        self.left_button.setDisabled(False)
        self.threshold_slider.setDisabled(False)

    def disable_widgets(self):
        self.reset_button.setDisabled(True)
        self.right_button.setDisabled(True)
        self.left_button.setDisabled(True)
        self.threshold_slider.setDisabled(True)

    def left_on_click(self):
        if self.displayed_segment_index > 0:
            self.displayed_segment_index -= 1
            if self.image.thresholded[self.displayed_segment_index] is None:
                self.show_black_image()
            else:
                self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
                self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])
                self.threshold_slider.setDisabled(False)
                self.reset_button.setDisabled(False)
                self.update_label(self.no_image_label, "")
            self.update_label(self.segments_label,
                              'Tones in range: ' + str(self.segments[self.displayed_segment_index]) + ' - '
                              + str(self.segments[self.displayed_segment_index + 1]) + ' ')

    def right_on_click(self):
        if self.displayed_segment_index < self.image.n_segments-1:  # indeksowane od 0
            self.displayed_segment_index += 1
            if self.image.thresholded[self.displayed_segment_index] is None:
                self.show_black_image()
            else:
                self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
                self.threshold_slider.setValue(self.image.threshold_values[self.displayed_segment_index])
                self.threshold_slider.setDisabled(False)
                self.reset_button.setDisabled(False)
                self.update_label(self.no_image_label, "")
            self.update_label(self.segments_label,
                              'Tones in range: ' + str(self.segments[self.displayed_segment_index]) + ' - '
                              + str(self.segments[self.displayed_segment_index + 1]) + ' ')

    def show_black_image(self):
        black_image = np.zeros((self.image.height, self.image.width))
        self.update_image(self.qt_image, black_image, self.image_label)
        self.threshold_slider.setDisabled(True)
        self.reset_button.setDisabled(True)
        self.update_label(self.no_image_label,
                          "<font color='white'><b>No pixels with value in this range</b></font>")

    def change_threshold_value(self, value):
        before_change = self.image.masked[self.displayed_segment_index]
        changed_image = change_threshold(before_change, value)
        self.image.thresholded[self.displayed_segment_index] = changed_image
        self.update_image(self.qt_image, self.image.thresholded[self.displayed_segment_index], self.image_label)
        self.image.threshold_values[self.displayed_segment_index] = value
        self.image.update_result()
        self.update_image(self.res_image, self.image.result, self.result_image_label)
        self.update_label(self.threshold_label, 'Threshold value: ' + str(value))

    def change_blur_value(self, value):
        self.current_blur = value
        self.image.blurred = change_blur(self.image.gray, value)
        self.res_image = self.convert_cv_qt(self.image.blurred, self.result_image_label)
        self.result_image_label.setPixmap(QPixmap.fromImage(self.res_image))
        self.update_label(self.blur_label, 'Blur value: ' + str(value))

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
        elif f is not None and self.image.result is None:
            cv.imwrite(f.name, self.image.blurred)

    def load_image(self, file_name=None):
        if file_name is None:
            file_name = tkinter.filedialog.askopenfilename(initialdir="../Photos")
        if file_name:
            self.image = Image(file_name, explore_files=True)
            self.qt_image = self.convert_cv_qt(self.image.gray, self.image_label)
            self.res_image = self.convert_cv_qt(self.image.blurred, self.result_image_label)
            qt_image_pixmap = QPixmap.fromImage(self.qt_image)
            self.image_label.setPixmap(qt_image_pixmap)
            res_image_pixmap = QPixmap.fromImage(self.res_image)
            self.result_image_label.setPixmap(res_image_pixmap)
            self.change_blur_value(self.current_blur)
            self.disable_widgets()
            self.update_label(self.threshold_label, '')

    def open_recent(self):
        path = self.launch_settings.import_image()
        self.load_image(path)

    def show_warning_window(self, message):
        self.dialog_window.setText(message)
        self.dialog_window.exec()

    def remember_settings(self):
        self.launch_settings.export_to_json(self.input.text(), self.current_blur)

    def forget_settings(self):
        self.launch_settings.delete_file()
