# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sine_fit_ui.ui'
#
# Created: Mon Jul 18 21:42:08 2016
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SineDialog(object):
    def setupUi(self, SineDialog):
        SineDialog.setObjectName("SineDialog")
        SineDialog.resize(215, 185)
        self.formLayoutWidget = QtGui.QWidget(SineDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 60, 130, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.aSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.aSpinBox.setMaximum(9999.99)
        self.aSpinBox.setObjectName("aSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aSpinBox)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.bSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.bSpinBox.setMaximum(9999.99)
        self.bSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.bSpinBox.setObjectName("bSpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.bSpinBox)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.TpiSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.TpiSpinBox.setMaximum(99999.99)
        self.TpiSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.TpiSpinBox.setObjectName("TpiSpinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.TpiSpinBox)
        self.doneButton = QtGui.QPushButton(SineDialog)
        self.doneButton.setGeometry(QtCore.QRect(130, 150, 75, 23))
        self.doneButton.setObjectName("doneButton")
        self.fitButton = QtGui.QPushButton(SineDialog)
        self.fitButton.setGeometry(QtCore.QRect(10, 150, 75, 23))
        self.fitButton.setObjectName("fitButton")
        self.label_4 = QtGui.QLabel(SineDialog)
        self.label_4.setGeometry(QtCore.QRect(30, 10, 151, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(SineDialog)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), SineDialog.close)
        QtCore.QMetaObject.connectSlotsByName(SineDialog)
        SineDialog.setTabOrder(self.fitButton, self.doneButton)
        SineDialog.setTabOrder(self.doneButton, self.aSpinBox)
        SineDialog.setTabOrder(self.aSpinBox, self.bSpinBox)
        SineDialog.setTabOrder(self.bSpinBox, self.TpiSpinBox)

    def retranslateUi(self, SineDialog):
        SineDialog.setWindowTitle(QtGui.QApplication.translate("SineDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SineDialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SineDialog", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SineDialog", "Pi time, us", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("SineDialog", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("SineDialog", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SineDialog", "Fit: \n"
"y = a + b Sin(t * pi / 2 Tpi)^2", None, QtGui.QApplication.UnicodeUTF8))

