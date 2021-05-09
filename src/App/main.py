import sys
from PyQt5.QtWidgets import QApplication
from src.App.GUI import MainWindow
from src.Objects.Image import Image
import tkinter.filedialog  #import askopenfilename
from tkinter import Tk

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.exit("This program needs arguments: Photo_FILEname(obligatory) or \"explore\", [Thresholds](optional)")

    if sys.argv[1] == "explore":
        Tk().withdraw()
        file_name = tkinter.filedialog.askopenfilename(initialdir="./")
        image = Image(file_name, explore_files=True)
        print(file_name)
    else:
        file_name = sys.argv[1]
        image = Image(file_name)

    app = QApplication([])
    window = MainWindow(image)
    window.show()
    sys.exit(app.exec_())
