import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image

if __name__ == "__main__":
    # Getting input from usr
    file_name = sys.argv[1]
    image = Image(file_name)

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
