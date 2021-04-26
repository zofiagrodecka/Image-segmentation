import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image

if __name__ == "__main__":
    image = Image('TEST.jpg')

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
