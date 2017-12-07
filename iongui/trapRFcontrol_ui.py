# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trapRFcontrol_ui.ui'
#
# Created: Tue Nov 05 15:35:48 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 300)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(40, 40, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(Dialog)
        self.doubleSpinBox.setGeometry(QtCore.QRect(120, 40, 62, 22))
        self.doubleSpinBox.setMaximum(10.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Set Amplitude", None, QtGui.QApplication.UnicodeUTF8))

