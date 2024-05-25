from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


app = QApplication([])
widget = MainWindow()
widget.show()
app.exec()
