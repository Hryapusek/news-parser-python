import multiprocessing
from PyQt5.QtWidgets import QApplication, qApp
from gui.main_window import MainWindow

if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    app = QApplication([])
    widget = MainWindow()
    qApp.setStyleSheet(open("./res/style2.qss").read())
    widget.show()
    app.exec()
