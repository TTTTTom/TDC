# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gauss_fit_ui.ui'
#
# Created: Fri Dec 09 15:48:37 2016
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Gauss_Fit_Dialog(object):
    def setupUi(self, Gauss_Fit_Dialog):
        Gauss_Fit_Dialog.setObjectName("Gauss_Fit_Dialog")
        Gauss_Fit_Dialog.resize(247, 244)
        self.formLayoutWidget = QtGui.QWidget(Gauss_Fit_Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 40, 208, 126))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.aSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.aSpinBox.setMaximum(512)
        self.aSpinBox.setObjectName("aSpinBox")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.aSpinBox)
        self.x0SpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.x0SpinBox.setMaximum(512)
        self.x0SpinBox.setObjectName("x0SpinBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.x0SpinBox)
        self.y0SpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.y0SpinBox.setMaximum(512)
        self.y0SpinBox.setObjectName("y0SpinBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.y0SpinBox)
        self.sigmaxSpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.sigmaxSpinBox.setObjectName("sigmaxSpinBox")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.sigmaxSpinBox)
        self.sigmaySpinBox = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.sigmaySpinBox.setObjectName("sigmaySpinBox")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.sigmaySpinBox)
        self.fitButton = QtGui.QPushButton(Gauss_Fit_Dialog)
        self.fitButton.setGeometry(QtCore.QRect(20, 190, 75, 23))
        self.fitButton.setObjectName("fitButton")
        self.doneButton = QtGui.QPushButton(Gauss_Fit_Dialog)
        self.doneButton.setGeometry(QtCore.QRect(140, 190, 75, 23))
        self.doneButton.setObjectName("doneButton")
        self.Formula = QtGui.QLabel(Gauss_Fit_Dialog)
        self.Formula.setGeometry(QtCore.QRect(20, 10, 190, 20))
        self.Formula.setObjectName("Formula")

        self.retranslateUi(Gauss_Fit_Dialog)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), Gauss_Fit_Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Gauss_Fit_Dialog)

    def retranslateUi(self, Gauss_Fit_Dialog):
        Gauss_Fit_Dialog.setWindowTitle(QtGui.QApplication.translate("Gauss_Fit_Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "x_0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "sigma_x", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "sigma_y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "y_0", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.fitButton.setShortcut(QtGui.QApplication.translate("Gauss_Fit_Dialog", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.doneButton.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "Done", None, QtGui.QApplication.UnicodeUTF8))
        self.Formula.setText(QtGui.QApplication.translate("Gauss_Fit_Dialog", "a*exp(-(x-x_0)**2/(2*sigma**2))", None, QtGui.QApplication.UnicodeUTF8))

