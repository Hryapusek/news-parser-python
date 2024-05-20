import matplotlib
matplotlib.use('Qt5Agg')

from articleloader.article_loader import ArticleLoader
from articleloader.exceptions import AlreadyRunningException, NotRunningException

from .ui_main_window import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QDate, QTimer

from datetime import datetime

from keywords.keywords_parser import KeywordsParser

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.load_from_internet_btn.clicked.connect(self.__load_from_internet_btn_clicked)
        self._ui.load_from_docs_btn.clicked.connect(self.__load_from_docs_btn_clicked)
        self._ui.cancel_btn.clicked.connect(self.__call_stop)
        self.categories = KeywordsParser.parse_file("keywords.txt")
        self.__init_plots()
        self.__print_keywords()
    
    def __init_plots(self):
        while self._ui.stacked_plots.count() > 0:
            self._ui.stacked_plots.removeWidget(self._ui.stacked_plots.widget(self._ui.stacked_plots.count() - 1))
        for category in self.categories:
            self._ui.category_combobox.addItem(category.name)
            self._ui.stacked_plots.addWidget(MplCanvas(self, width=5, height=4, dpi=100))

    # {date: [text, text, text]}
    # {subcategory: [word, word, word]}

    def __build_plots(self):
        pass

    def __print_keywords(self):
        if len(self.categories) == 0:
            self._ui.keywords_logs.append("No keywords were found!")
            return
        for cathegory in self.categories:
            self._ui.keywords_logs.append(f"# [{cathegory.name}]")
            if len(cathegory.subcategories) == 0:
                self._ui.keywords_logs.append(f"  No subcathegories were found!")
                continue
            for subcathegory in cathegory.subcategories:
                self._ui.keywords_logs.append(f"## [{subcathegory.name}]")
                self._ui.keywords_logs.append(f"  Keywords: {subcathegory.keywords}\n")

    def __load_from_internet_btn_clicked(self):
        from_date = __class__.__qdate_to_datetime(self._ui.from_date.date())
        to_date = __class__.__qdate_to_datetime(self._ui.to_date.date())
        if not self.__check_dates(from_date, to_date):
            return
        try:
            ArticleLoader.load_articles_from_internet(from_date, to_date)
            QTimer.singleShot(100, self.update_articles_status)
        except AlreadyRunningException:
            QMessageBox.critical(self, "Период времени", "Сначала дождитесь завершения выполнения прошлой загрузки.")
            return
        
    def __call_stop(self):
        try:
            ArticleLoader.call_stop()
        except NotRunningException:
            QMessageBox.information(self, "Остановка", "Остановка уже запрошена, пожалуйста подождите немного времени.")
            return

    @staticmethod
    def __qdate_to_datetime(date_value: QDate):
        return datetime(date_value.year(), date_value.month(), date_value.day(), 0, 0, 0)

    def __load_from_docs_btn_clicked(self):
        from_date = self._ui.from_date.date()
        to_date = self._ui.to_date.date()
        if not self.__check_dates(from_date, to_date):
            return
        try:
            ArticleLoader.load_articles_from_saved_files(from_date, to_date)
            QTimer.singleShot(100, self.update_articles_status)
        except AlreadyRunningException:
            QMessageBox.critical(self, "Период времени", "Сначала дождитесь завершения выполнения прошлой загрузки.")
            return

    def __check_dates(self, from_date, to_date):
        if from_date > to_date:
            QMessageBox.critical(self, "Период времени", "Дата начала должна быть меньше даты окончания.")
            return False
        if to_date > datetime.today():
            QMessageBox.critical(self, "Период времени", "Дата окончания должна быть не позднее текущей даты.")
            self._ui.to_date.setFocus()
            return False
        return True

    def update_articles_status(self):
        status, percantage = ArticleLoader.get_status()
        self._ui.articles_logs.append(f"{datetime.now()} {status}")
        self._ui.progress_bar.setValue(round(percantage))
        if not ArticleLoader.is_finished():
            QTimer.singleShot(100, self.update_articles_status)
            return
        else:
            self._ui.articles_logs.append(f"{datetime.now()} Finished!")
            self._ui.progress_bar.setValue(100)
            if not ArticleLoader.is_stop_called():
                self.__build_plots()
