import matplotlib

from utils.utils import daterange
matplotlib.use('Qt5Agg')

from articleloader.article_loader import ArticleLoader
from articleloader.exceptions import AlreadyRunningException, NotRunningException

from .ui_main_window import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDate, QTimer


from datetime import datetime, timedelta

from keywords.keywords_parser import KeywordsParser

from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig: Figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes: Axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.load_from_internet_btn.clicked.connect(self.__load_from_internet_btn_clicked)
        self._ui.load_from_docs_btn.clicked.connect(self.__load_from_docs_btn_clicked)
        self._ui.cancel_btn.clicked.connect(self.__call_stop)
        self.__categories = KeywordsParser.parse_file("keywords.txt")
        self.__init_plots()
        self.__print_keywords()
    
    def __init_plots(self):
        self.__plots: list[tuple[MplCanvas, QtWidgets.QTextEdit]] = []
        while self._ui.stacked_plots.count() > 0:
            self._ui.stacked_plots.removeWidget(self._ui.stacked_plots.widget(self._ui.stacked_plots.count() - 1))
        for category in self.__categories:
            self._ui.category_combobox.addItem(category.name)
            main_widget = QtWidgets.QWidget(self._ui.stacked_plots)
            vlayout = QVBoxLayout(main_widget)
            self._ui.stacked_plots.addWidget(main_widget)
            main_widget.setLayout(vlayout)
            canvas = MplCanvas(main_widget, width=5, height=4, dpi=100)
            plot_logs = QtWidgets.QTextEdit(main_widget)
            vlayout.addWidget(canvas)
            vlayout.addWidget(plot_logs)
            plot_logs.setReadOnly(True)
            plot_logs.setObjectName("articles_logs")
            self.__plots.append((canvas, plot_logs))

    # {date: [text, text, text]}
    # {subcategory: [word, word, word]}

    def __build_plots(self):
        begin_date, end_date = ArticleLoader.get_dates()[0], ArticleLoader.get_dates()[1]+timedelta(1) 
        x_dates = list(daterange(begin_date, end_date))
        date_articles = ArticleLoader.get_date_articles()
        for plot_no, category in enumerate(self.__categories):
            plot = self.__plots[plot_no][0]
            plot.axes.clear()
            for subcategory in category.subcategories:
                y_values = []
                for date in daterange(begin_date, end_date):
                    if date not in date_articles:
                        y_values.append(0)
                        continue
                    count_occurances = 0
                    for article in date_articles[date]:
                        count_occurances += self.__count_occurances(subcategory.keywords, article.tokens)
                    y_values.append(count_occurances/len(date_articles[date]))
                plot.axes.set_xlim(xmin=x_dates[0], xmax=x_dates[-1])
                plot.axes.plot(x_dates, y_values, label=subcategory.name)
                plot.axes.legend()
                plot.axes.set_xlabel("Дата")
                plot.axes.set_ylabel("Значение величины упоминаний")
                plot.draw()
    
    def __count_occurances(self, keywords: list[str], tokens: list[str]):
        count = 0
        for keyword in keywords:
            count += tokens.count(keyword)
        return count

    def __print_keywords(self):
        if len(self.__categories) == 0:
            self._ui.keywords_logs.append("No keywords were found!")
            return
        for cathegory in self.__categories:
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
        from_date = __class__.__qdate_to_datetime(self._ui.from_date.date())
        to_date = __class__.__qdate_to_datetime(self._ui.to_date.date())
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
