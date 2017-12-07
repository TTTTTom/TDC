# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sideband_cooling_config.ui'
#
# Created: Tue Oct  8 12:36:37 2013
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

class Ui_SidebandCoolingDialog(object):
    def setupUi(self, SidebandCoolingDialog):
        SidebandCoolingDialog.setObjectName(_fromUtf8("SidebandCoolingDialog"))
        SidebandCoolingDialog.resize(319, 253)
        self.buttonBox = QtGui.QDialogButtonBox(SidebandCoolingDialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 210, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(SidebandCoolingDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(40, 40, 265, 161))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.nphonon = QtGui.QDoubleSpinBox(self.formLayoutWidget)
        self.nphonon.setMaximum(999.99)
        self.nphonon.setProperty("value", 10.0)
        self.nphonon.setObjectName(_fromUtf8("nphonon"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.nphonon)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.nreps = QtGui.QSpinBox(self.formLayoutWidget)
        self.nreps.setMinimum(1)
        self.nreps.setMaximum(999)
        self.nreps.setProperty("value", 30)
        self.nreps.setObjectName(_fromUtf8("nreps"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.nreps)
        self.plusButton = QtGui.QPushButton(self.formLayoutWidget)
        self.plusButton.setObjectName(_fromUtf8("plusButton"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.plusButton)
        self.minusButton = QtGui.QPushButton(self.formLayoutWidget)
        self.minusButton.setObjectName(_fromUtf8("minusButton"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.minusButton)
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.nlines = QtGui.QSpinBox(self.formLayoutWidget)
        self.nlines.setMinimum(2)
        self.nlines.setMaximum(32)
        self.nlines.setObjectName(_fromUtf8("nlines"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nlines)
        self.label_5 = QtGui.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)

        self.retranslateUi(SidebandCoolingDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SidebandCoolingDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SidebandCoolingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SidebandCoolingDialog)

    def retranslateUi(self, SidebandCoolingDialog):
        SidebandCoolingDialog.setWindowTitle(_translate("SidebandCoolingDialog", "Dialog", None))
        self.label_3.setText(_translate("SidebandCoolingDialog", "Initial number of phonons", None))
        self.label_4.setText(_translate("SidebandCoolingDialog", "Number of cycles", None))
        self.plusButton.setText(_translate("SidebandCoolingDialog", "+", None))
        self.minusButton.setText(_translate("SidebandCoolingDialog", "-", None))
        self.label.setText(_translate("SidebandCoolingDialog", "Remove chapter line", None))
        self.label_2.setText(_translate("SidebandCoolingDialog", "Add chapter line", None))
        self.label_5.setText(_translate("SidebandCoolingDialog", "Lines per cooling step", None))

