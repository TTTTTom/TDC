# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guibyte.ui'
#
# Created: Tue Jun 14 13:58:48 2016
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TimeSeqWindow(object):
    def setupUi(self, TimeSeqWindow):
        TimeSeqWindow.setObjectName("TimeSeqWindow")
        TimeSeqWindow.resize(1378, 862)
        self.centralwidget = QtGui.QWidget(TimeSeqWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(10, 20, 75, 23))
        self.saveButton.setObjectName("saveButton")
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(420, 20, 75, 23))
        self.exitButton.setObjectName("exitButton")
        self.runButton = QtGui.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(220, 20, 75, 23))
        self.runButton.setObjectName("runButton")
        self.configButton = QtGui.QPushButton(self.centralwidget)
        self.configButton.setGeometry(QtCore.QRect(320, 20, 75, 23))
        self.configButton.setObjectName("configButton")
        self.loadButton = QtGui.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(120, 20, 75, 23))
        self.loadButton.setObjectName("loadButton")
        self.labelUSB = QtGui.QLabel(self.centralwidget)
        self.labelUSB.setGeometry(QtCore.QRect(530, 20, 141, 16))
        self.labelUSB.setObjectName("labelUSB")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 70, 1351, 831))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.add_tab_button = QtGui.QPushButton(self.centralwidget)
        self.add_tab_button.setGeometry(QtCore.QRect(730, 20, 31, 23))
        self.add_tab_button.setObjectName("add_tab_button")
        self.remove_tab_button = QtGui.QPushButton(self.centralwidget)
        self.remove_tab_button.setGeometry(QtCore.QRect(760, 20, 31, 23))
        self.remove_tab_button.setObjectName("remove_tab_button")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(720, 50, 91, 16))
        self.label.setObjectName("label")
        self.savetabButton = QtGui.QPushButton(self.centralwidget)
        self.savetabButton.setGeometry(QtCore.QRect(10, 40, 75, 23))
        self.savetabButton.setObjectName("savetabButton")
        TimeSeqWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TimeSeqWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1378, 21))
        self.menubar.setObjectName("menubar")
        TimeSeqWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TimeSeqWindow)
        self.statusbar.setObjectName("statusbar")
        TimeSeqWindow.setStatusBar(self.statusbar)

        self.retranslateUi(TimeSeqWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.exitButton, QtCore.SIGNAL("clicked()"), TimeSeqWindow.close)
        QtCore.QMetaObject.connectSlotsByName(TimeSeqWindow)

    def retranslateUi(self, TimeSeqWindow):
        TimeSeqWindow.setWindowTitle(QtGui.QApplication.translate("TimeSeqWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Save All", None, QtGui.QApplication.UnicodeUTF8))
        self.exitButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.runButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Run", None, QtGui.QApplication.UnicodeUTF8))
        self.configButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Configure", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.labelUSB.setText(QtGui.QApplication.translate("TimeSeqWindow", "USB Sequencer status", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("TimeSeqWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))
        self.add_tab_button.setText(QtGui.QApplication.translate("TimeSeqWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.remove_tab_button.setText(QtGui.QApplication.translate("TimeSeqWindow", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TimeSeqWindow", "Add / Remove tab", None, QtGui.QApplication.UnicodeUTF8))
        self.savetabButton.setText(QtGui.QApplication.translate("TimeSeqWindow", "Save Tab", None, QtGui.QApplication.UnicodeUTF8))

