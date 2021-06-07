import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image
from tkinter import Tk, filedialog

if __name__ == "__main__":

    Tk().withdraw()
    file_name = filedialog.askopenfilename(initialdir="./Photos")
    if not file_name:
        sys.exit("You have to choose Image to proceed")
    image = Image(file_name, explore_files=True)

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
