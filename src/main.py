import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image
import tkinter.filedialog
from tkinter import Tk

if __name__ == "__main__":

    Tk().withdraw()
    file_name = tkinter.filedialog.askopenfilename(initialdir="../Photos")
    if len(file_name) == 0:
        sys.exit("You have to choose Image to proceed")
    image = Image(file_name, explore_files=True)

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
