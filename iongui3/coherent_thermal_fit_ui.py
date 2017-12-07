# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coherent_thermal_fit_ui.ui'
#
# Created: Fri Jun 24 09:26:14 2016
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Coh_Th_Dialog(object):
    def setupUi(self, Coh_Th_Dialog):
        Coh_Th_Dialog.setObjectName("Coh_Th_Dialog")
        Coh_Th_Dialog.resize(257, 253)
        self.formLayoutWidget = QtGui.QWidget(Coh_Th_Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 80, 201, 126))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.aSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.aSpinBox.setDecimals(5)
        self.aSpinBox.setMaximum(9999.99)
        self.aSpinBox.setObjectName("aSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aSpinBox)
        self.nbarSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.nbarSpinBox.setMaximum(99.99)
        self.nbarSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.nbarSpinBox.setObjectName("nbarSpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nbarSpinBox)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_6)
        self.TpiSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.TpiSpinBox.setMaximum(99999.99)
        self.TpiSpinBox.setProperty("value", QtCore.QVariant(10.0))
        self.TpiSpinBox.setObjectName("TpiSpinBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.TpiSpinBox)
        self.gammaSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.gammaSpinBox.setDecimals(10)
        self.gammaSpinBox.setMaximum(1.0)
        self.gammaSpinBox.setProperty("value", QtCore.QVariant(0.0))
        self.gammaSpinBox.setObjectName("gammaSpinBox")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.gammaSpinBox)
        self.nSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.nSpinBox.setMinimum(1)
        self.nSpinBox.setProperty("value", QtCore.QVariant(10))
        self.nSpinBox.setObjectName("nSpinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.nSpinBox)
        self.doneButton = QtGui.QPushButton(Coh_Th_Dialog)
        self.doneButton.setGeometry(QtCore.QRect(150, 220, 75, 23))
        self.doneButton.setObjectName("doneButton")
        self.fitButton = QtGui.QPushButton(Coh_Th_Dialog)
        self.fitButton.setGeometry(QtCore.QRect(30, 220, 75, 23))
        self.fitButton.setObjectName("fitButton")
        self.label_4 = QtGui.QLabel(Coh_Th_Dialog)
        self.label_4.setGeometry(QtCore.QRect(50, 30, 151, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Coh_Th_Dialog)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), Coh_Th_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Coh_Th_Dialog)
        Coh_Th_Dialog.setTabOrder(self.fitButton, self.doneButton)
        Coh_Th_Dialog.setTabOrder(self.doneButton, self.aSpinBox)
        Coh_Th_Dialog.setTabOrder(self.aSpinBox, self.nbarSpinBox)
        Coh_Th_Dialog.setTabOrder(self.nbarSpinBox, self.TpiSpinBox)
        Coh_Th_Dialog.setTabOrder(self.TpiSpinBox, self.gammaSpinBox)
        Coh_Th_Dialog.setTabOrder(self.gammaSpinBox, self.nSpinBox)

    def retranslateUi(self, Coh_Th_Dialog):
        Coh_Th_Dialog.setWindowTitle(QtGui.QApplication.translate("Coh_Th_Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "n", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "nbar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "Tpi", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "gamma", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Coh_Th_Dialog", "Fit: \n"
"y = a/2 * (1 - ...)", None, QtGui.QApplication.UnicodeUTF8))

