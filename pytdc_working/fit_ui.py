# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fit_ui.ui'
#
# Created: Mon Sep 24 14:26:06 2012
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(289, 251)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(50, 40, 201, 126))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.aSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.aSpinBox.setMaximum(999.99)
        self.aSpinBox.setObjectName("aSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aSpinBox)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.bSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.bSpinBox.setMaximum(999.99)
        self.bSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.bSpinBox.setObjectName("bSpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bSpinBox)
        self.TpiSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.TpiSpinBox.setMaximum(9999.99)
        self.TpiSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.TpiSpinBox.setObjectName("TpiSpinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.TpiSpinBox)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.TSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.TSpinBox.setMaximum(9999.99)
        self.TSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.TSpinBox.setObjectName("TSpinBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.TSpinBox)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.freqSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.freqSpinBox.setDecimals(6)
        self.freqSpinBox.setMaximum(99999.99)
        self.freqSpinBox.setSingleStep(0.1)
        self.freqSpinBox.setProperty("value", QtCore.QVariant(100.0))
        self.freqSpinBox.setObjectName("freqSpinBox")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.freqSpinBox)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.fitButton = QtGui.QPushButton(Dialog)
        self.fitButton.setGeometry(QtCore.QRect(50, 190, 75, 23))
        self.fitButton.setObjectName("fitButton")
        self.doneButton = QtGui.QPushButton(Dialog)
        self.doneButton.setGeometry(QtCore.QRect(170, 190, 75, 23))
        self.doneButton.setObjectName("doneButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Pulse time, us", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Frequency, MHz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Pi time, us", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("Dialog", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("Dialog", "Done", None, QtGui.QApplication.UnicodeUTF8))

