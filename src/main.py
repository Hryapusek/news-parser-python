from PyQt5.QtWidgets import QApplication, qApp
from gui.main_window import MainWindow


app = QApplication([])
widget = MainWindow()
qApp.setStyleSheet(open("./res/style2.qss").read())
widget.show()
app.exec()
