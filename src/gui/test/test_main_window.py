import unittest

from datetime import datetime
from PyQt5.QtWidgets import QApplication, qApp
from ..main_window import MainWindow


class TestMainWindow(unittest.TestCase):

    def test_default(self):
        app = QApplication([])
        widget = MainWindow()
        qApp.setStyleSheet(open("./res/style2.qss").read())
        widget.show()
        app.exec()
