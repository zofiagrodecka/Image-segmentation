import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image

if __name__ == "__main__":
    # Getting input from usr
    file_names = []
    for i in range(1, len(sys.argv)):
        parameter = sys.argv[i]
        file_names.append(parameter)

    images = []
    for file_name in file_names:
        print(file_name)
        image = Image(file_name)
        images.append(image)

    app = QApplication([])
    window = MainWindow(images)
    window.show()
    sys.exit(app.exec_())
