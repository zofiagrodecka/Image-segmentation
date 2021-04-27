import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image

if __name__ == "__main__":
    # Getting input from usr
    file_name = sys.argv[1]
    gray_scale_div = []
    for i in range(2, len(sys.argv)):
        parameter = sys.argv[i]
        gray_scale_div.append(int(parameter))

    image = Image(file_name, gray_scale_div)

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
