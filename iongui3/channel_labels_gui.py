# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channel_labels_gui.ui'
#
# Created: Thu Aug  1 19:00:48 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ChannelLabelsEditor(object):
    def setupUi(self, ChannelLabelsEditor):
        ChannelLabelsEditor.setObjectName(_fromUtf8("ChannelLabelsEditor"))
        ChannelLabelsEditor.resize(550, 668)
        self.buttonBox = QtGui.QDialogButtonBox(ChannelLabelsEditor)
        self.buttonBox.setGeometry(QtCore.QRect(190, 430, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tableWidget = QtGui.QTableWidget(ChannelLabelsEditor)
        self.tableWidget.setGeometry(QtCore.QRect(60, 30, 471, 500))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setMinimumSize(QtCore.QSize(471, 500))
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(40)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.buttonBox_2 = QtGui.QDialogButtonBox(ChannelLabelsEditor)
        self.buttonBox_2.setGeometry(QtCore.QRect(350, 590, 176, 27))
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))

        self.retranslateUi(ChannelLabelsEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChannelLabelsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChannelLabelsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ChannelLabelsEditor)

    def retranslateUi(self, ChannelLabelsEditor):
        ChannelLabelsEditor.setWindowTitle(_translate("ChannelLabelsEditor", "Dialog", None))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

