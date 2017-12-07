# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ramsey_fit_ui.ui'
#
# Created: Fri Jun 24 09:25:03 2016
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RamseyDialog(object):
    def setupUi(self, RamseyDialog):
        RamseyDialog.setObjectName("RamseyDialog")
        RamseyDialog.resize(257, 253)
        self.formLayoutWidget = QtGui.QWidget(RamseyDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 80, 201, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.aSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.aSpinBox.setMaximum(1.0)
        self.aSpinBox.setSingleStep(0.01)
        self.aSpinBox.setProperty("value", QtCore.QVariant(0.5))
        self.aSpinBox.setObjectName("aSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aSpinBox)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.bSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.bSpinBox.setMaximum(1.0)
        self.bSpinBox.setSingleStep(0.01)
        self.bSpinBox.setProperty("value", QtCore.QVariant(0.5))
        self.bSpinBox.setObjectName("bSpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bSpinBox)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.dSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.dSpinBox.setDecimals(3)
        self.dSpinBox.setMaximum(99999.99)
        self.dSpinBox.setProperty("value", QtCore.QVariant(500.0))
        self.dSpinBox.setObjectName("dSpinBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dSpinBox)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_5)
        self.fSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.fSpinBox.setDecimals(6)
        self.fSpinBox.setMaximum(10.0)
        self.fSpinBox.setSingleStep(0.0001)
        self.fSpinBox.setProperty("value", QtCore.QVariant(0.005))
        self.fSpinBox.setObjectName("fSpinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.fSpinBox)
        self.doneButton = QtGui.QPushButton(RamseyDialog)
        self.doneButton.setGeometry(QtCore.QRect(150, 190, 75, 23))
        self.doneButton.setObjectName("doneButton")
        self.fitButton = QtGui.QPushButton(RamseyDialog)
        self.fitButton.setGeometry(QtCore.QRect(30, 190, 75, 23))
        self.fitButton.setObjectName("fitButton")
        self.label_4 = QtGui.QLabel(RamseyDialog)
        self.label_4.setGeometry(QtCore.QRect(30, 30, 191, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(RamseyDialog)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), RamseyDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RamseyDialog)
        RamseyDialog.setTabOrder(self.fitButton, self.doneButton)
        RamseyDialog.setTabOrder(self.doneButton, self.aSpinBox)
        RamseyDialog.setTabOrder(self.aSpinBox, self.bSpinBox)
        RamseyDialog.setTabOrder(self.bSpinBox, self.dSpinBox)
        RamseyDialog.setTabOrder(self.dSpinBox, self.fSpinBox)

    def retranslateUi(self, RamseyDialog):
        RamseyDialog.setWindowTitle(QtGui.QApplication.translate("RamseyDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RamseyDialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("RamseyDialog", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("RamseyDialog", "d, us", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("RamseyDialog", "f, MHz", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("RamseyDialog", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("RamseyDialog", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("RamseyDialog", "Fit: \n"
"y = a + b Cos(t * 2 * pi * f) * exp(-t/d)", None, QtGui.QApplication.UnicodeUTF8))

