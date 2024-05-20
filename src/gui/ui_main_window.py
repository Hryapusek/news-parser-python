# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 653)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.graphics_tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphics_tab.sizePolicy().hasHeightForWidth())
        self.graphics_tab.setSizePolicy(sizePolicy)
        self.graphics_tab.setObjectName("graphics_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.graphics_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.category_combobox = QtWidgets.QComboBox(self.graphics_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.category_combobox.sizePolicy().hasHeightForWidth())
        self.category_combobox.setSizePolicy(sizePolicy)
        self.category_combobox.setObjectName("category_combobox")
        self.horizontalLayout_5.addWidget(self.category_combobox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.stacked_plots = QtWidgets.QStackedWidget(self.graphics_tab)
        self.stacked_plots.setObjectName("stacked_plots")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stacked_plots.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stacked_plots.addWidget(self.page_2)
        self.verticalLayout_6.addWidget(self.stacked_plots)
        self.verticalLayout_4.addLayout(self.verticalLayout_6)
        self.tabs.addTab(self.graphics_tab, "")
        self.articles_tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.articles_tab.sizePolicy().hasHeightForWidth())
        self.articles_tab.setSizePolicy(sizePolicy)
        self.articles_tab.setObjectName("articles_tab")
        self.formLayout = QtWidgets.QFormLayout(self.articles_tab)
        self.formLayout.setObjectName("formLayout")
        self.splitter = QtWidgets.QSplitter(self.articles_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.articles_logs = QtWidgets.QTextEdit(self.layoutWidget)
        self.articles_logs.setReadOnly(True)
        self.articles_logs.setObjectName("articles_logs")
        self.verticalLayout.addWidget(self.articles_logs)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.from_date = QtWidgets.QDateEdit(self.layoutWidget1)
        self.from_date.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 5, 13), QtCore.QTime(0, 0, 0)))
        self.from_date.setDate(QtCore.QDate(2024, 5, 13))
        self.from_date.setObjectName("from_date")
        self.horizontalLayout_2.addWidget(self.from_date)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.to_date = QtWidgets.QDateEdit(self.layoutWidget1)
        self.to_date.setDate(QtCore.QDate(2024, 5, 13))
        self.to_date.setObjectName("to_date")
        self.horizontalLayout_3.addWidget(self.to_date)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.load_from_internet_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.load_from_internet_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.load_from_internet_btn.setObjectName("load_from_internet_btn")
        self.verticalLayout_3.addWidget(self.load_from_internet_btn)
        self.load_from_docs_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.load_from_docs_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.load_from_docs_btn.setObjectName("load_from_docs_btn")
        self.verticalLayout_3.addWidget(self.load_from_docs_btn)
        self.cancel_btn = QtWidgets.QPushButton(self.layoutWidget1)
        self.cancel_btn.setMinimumSize(QtCore.QSize(0, 30))
        self.cancel_btn.setObjectName("cancel_btn")
        self.verticalLayout_3.addWidget(self.cancel_btn)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10000000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.progress_bar = QtWidgets.QProgressBar(self.layoutWidget1)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.verticalLayout_2.addWidget(self.progress_bar)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.splitter)
        self.tabs.addTab(self.articles_tab, "")
        self.keywords_tab = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keywords_tab.sizePolicy().hasHeightForWidth())
        self.keywords_tab.setSizePolicy(sizePolicy)
        self.keywords_tab.setObjectName("keywords_tab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.keywords_tab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.keywords_logs = QtWidgets.QTextEdit(self.keywords_tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.keywords_logs.setFont(font)
        self.keywords_logs.setObjectName("keywords_logs")
        self.horizontalLayout_4.addWidget(self.keywords_logs)
        self.tabs.addTab(self.keywords_tab, "")
        self.verticalLayout_5.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        self.stacked_plots.setCurrentIndex(1)
        self.category_combobox.currentIndexChanged['int'].connect(self.stacked_plots.setCurrentIndex) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Обработка новостей"))
        self.tabs.setTabText(self.tabs.indexOf(self.graphics_tab), _translate("MainWindow", "Графики"))
        self.label.setText(_translate("MainWindow", "Информация о загрузке"))
        self.label_2.setText(_translate("MainWindow", "С какого момента"))
        self.label_3.setText(_translate("MainWindow", "По какой момент"))
        self.load_from_internet_btn.setText(_translate("MainWindow", "Загрузить из интернета"))
        self.load_from_docs_btn.setText(_translate("MainWindow", "Загрузить из документов"))
        self.cancel_btn.setText(_translate("MainWindow", "Отмена"))
        self.tabs.setTabText(self.tabs.indexOf(self.articles_tab), _translate("MainWindow", "Статьи"))
        self.tabs.setTabText(self.tabs.indexOf(self.keywords_tab), _translate("MainWindow", "Ключевые слова"))