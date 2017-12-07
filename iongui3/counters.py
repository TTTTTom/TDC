__author__ = 'cqt'

import sys
from PyQt4 import QtCore, QtGui
from counter_config import Ui_CounterConfigWindow
from actions import ion_conditions, ion_actions
from Bfieldcontrol import BfieldDAC
#from iondata import IonData

# Class to do all the math on histograms
class CounterData():
    def __init__(self):
        self.index = {'a': 0, 'b': 1, 'c': 2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7 }
        self.above_thr = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.average   = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.raw_data  = {}
        #self.threshold = IonData.threshold


    # Calculates histogram properties (average and above_thr)
    def properties(self, histogram):
        total = sum(histogram)

        # Average number of counts for a histogram and apply threshold

        #belowth = sum(histogram[0:self.threshold.value()])
        belowth = sum(histogram[0:2])
        above_thr = 1.0 - float(belowth) / float(total)

        # Average number of counts for the counter
        average = 0.0
        for i in range(0, len(histogram)):
            average += i * histogram[i]

        if (total > 0):
            average = average / total
        else:
            average = 0

        # above_thr of the count number
        #dispersion = 0.0
        #for i in range(0, len(histogram)):
        #    dispersion += (average - i) * (average - i) * histogram[i]

        #if (total > 0):
        #    dispersion = dispersion / total
        #else:
        #    dispersion = 0.0

        return above_thr, average

    # Calculate all the statistical properties for all the available data
    def process(self, data):
        self.raw_data = data
        for key in data.keys():
            idx = self.index[key]
            self.above_thr[idx], self.average[idx] = self.properties(data[key])

    def get_average(self):
        return self.average

    def get_above_thr(self):
        return self.above_thr

#
# Clas that takes care of display
class CounterConfig(QtGui.QMainWindow):

    mask_changed = QtCore.pyqtSignal(int)
    XTOPLEFT     = 20
    YTOPLEFT     = 20
    XBOTTOMRIGHT = 641
    YLINEHEIGHT  = 30

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_CounterConfigWindow()
        self.ui.setupUi(self)

        self.counter_data = CounterData()

        self.camera_data = 0

        self.checkboxes = [self.ui.ch1box, self.ui.ch2box, self.ui.ch3box, self.ui.ch4box,
                           self.ui.ch5box, self.ui.ch6box, self.ui.ch7box, self.ui.ch8box]

        self.average    = [self.ui.ch1av, self.ui.ch2av, self.ui.ch3av, self.ui.ch4av,
                           self.ui.ch5av, self.ui.ch6av, self.ui.ch7av, self.ui.ch8av]

        self.above_thr  = [self.ui.ch1disp, self.ui.ch2disp, self.ui.ch3disp, self.ui.ch4disp,
                           self.ui.ch5disp, self.ui.ch6disp, self.ui.ch7disp, self.ui.ch8disp]

        for box in self.checkboxes:
            box.clicked.connect(self.checkbox_slot)

        self.rules = [Rule(self.ui.gridLayoutWidget_3, self.ui.rulesLayout, 0)]

        self.ui.gridLayoutWidget_3.setGeometry(QtCore.QRect(self.XTOPLEFT, self.YTOPLEFT, self.XBOTTOMRIGHT,
                                                            self.YTOPLEFT+ len(self.rules) * self.YLINEHEIGHT))

        self.ui.addButton.clicked.connect(self.add_line)
        self.ui.removeButton.clicked.connect(self.remove_line)

        try:
            self.bfield_dac         = BfieldDAC()
        except:
            print "BField_Dac error: ", sys.exc_info()[0]

        self.BfieldCoarse       = self.ui.CoarseB_Entry
        self.BfieldFine         = self.ui.FineB_Entry
        self.BfieldFineStepSize = self.ui.FineBStepSize_Entry
        QtCore.QObject.connect(self.ui.SetBField_Button,    QtCore.SIGNAL('clicked()'), self.bfield_set_voltage)
        QtCore.QObject.connect(self.ui.IncreaseB_Button,    QtCore.SIGNAL('clicked()'), self.bfield_increase)
        QtCore.QObject.connect(self.ui.DecreaseB_Button,    QtCore.SIGNAL('clicked()'), self.bfield_decrease)

        QtCore.QObject.connect(ion_actions["Increase B Field"], QtCore.SIGNAL("increaseBActionRequest"), self.bfield_increase)
        QtCore.QObject.connect(ion_actions["Decrease B Field"], QtCore.SIGNAL("decreaseBActionRequest"), self.bfield_decrease)

    # def get_camera_int(self, value):
    #     self.camera_data = value

    def bfield_set_voltage(self):
        self.bfield_dac.setcoarse(self.BfieldCoarse.value())
        self.BfieldFine.setValue(self.BfieldCoarse.value() * 1000)

    def bfield_increase(self):
        if self.BfieldFine.value() < 4096:
            self.bfield_dac.setfine(self.BfieldFine.value() + self.BfieldFineStepSize.value())
            self.BfieldFine.setValue(self.BfieldFine.value() + self.BfieldFineStepSize.value())
            print "increase B"

    def bfield_decrease(self):
        if self.BfieldFine.value() >= 0:
            self.bfield_dac.setfine(self.BfieldFine.value() - self.BfieldFineStepSize.value())
            self.BfieldFine.setValue(self.BfieldFine.value() - self.BfieldFineStepSize.value())
            print "decrease B"


    # set checkboxes according to mask values
    def set_mask(self, mask):
        for key in mask.keys():
            self.checkboxes[key].setChecked(mask[key] > 0)

    def get_mask(self):
        mask = {}
        for idx, box in enumerate(self.checkboxes):
            if box.isChecked():
                mask[idx] = 1
            else:
                mask[idx] = 0

        return mask

    # Slot for checkbox clicked event
    def checkbox_slot(self):
        mask = self.get_mask()
        bitmask = 0
        for key in mask.keys():
            bitmask += mask[key] * (1 << key)
        print bitmask
        self.mask_changed.emit(bitmask)

    # Process all the incoming histograms and update the display
    def process(self, data, new_inten):
        # update data statistics
        self.counter_data.process(data)

        # Update display for the average
        av = self.counter_data.get_average()
        for idx, lbl in enumerate(self.average):
            lbl.setText(str(av[idx]))

        # Update display for the above_thr
        above_thr = self.counter_data.get_above_thr()
        for idx, lbl in enumerate(self.above_thr):
            lbl.setText(str(above_thr[idx]))

        self.check_conditions()
        # self.update_cam_data(new_inten)
        self.camera_data = new_inten
        self.check_cam_conditions()

    # def update_cam_data(self, inten):
    #     self.camera_data = inten

    # check all if any of the conditions are met and trigger the appropriate action
    def check_conditions(self):
        for rule in self.rules:
            if rule.get_type() == "Histogram":
                rule.check(self.counter_data)

    def check_cam_conditions(self):
        for rule in self.rules:
            if rule.get_type() == "Camera":
                rule.check_cam(self.camera_data)

    def add_line(self):
        index = len(self.rules)
        self.rules.append(Rule(self.ui.gridLayoutWidget_3, self.ui.rulesLayout, index))
        self.ui.gridLayoutWidget_3.setGeometry(QtCore.QRect(self.XTOPLEFT, self.YTOPLEFT, self.XBOTTOMRIGHT,
                                                            self.YTOPLEFT+ len(self.rules) * self.YLINEHEIGHT))

    def remove_line(self):
        if len(self.rules) <= 1:
            return
        rule = self.rules.pop()
        del(rule)
        self.ui.gridLayoutWidget_3.setGeometry(QtCore.QRect(self.XTOPLEFT, self.YTOPLEFT, self.XBOTTOMRIGHT,
                                                            self.YTOPLEFT+ len(self.rules) * self.YLINEHEIGHT))

class Rule():
    def __init__(self, widget, layout, index):
        self.widget   = widget
        self.layout   = layout
        self.index    = index

        self.conditions = ion_conditions
        self.actions    = ion_actions

        self.ui_checkBox = QtGui.QCheckBox(self.widget)
        self.ui_checkBox.setObjectName("checkBox")
        self.ui_checkBox.setText("Active")
        self.layout.addWidget(self.ui_checkBox, self.index, 0, 1, 1)

        self.ui_property = QtGui.QComboBox(self.widget)
        self.ui_property.setObjectName("property")
        self.layout.addWidget(self.ui_property, self.index, 1, 1, 3)

        self.ui_value = QtGui.QDoubleSpinBox(self.widget)
        self.ui_value.setMaximum(1999.99)
        self.ui_value.setObjectName("value")
        self.layout.addWidget(self.ui_value, self.index, 4, 1, 1)

        self.ui_action = QtGui.QComboBox(self.widget)
        self.ui_action.setObjectName("action")
        self.layout.addWidget(self.ui_action, self.index, 5, 1, 2)

        for a in self.actions.values():
            self.ui_action.addItem(a.description())

        for c in self.conditions:
            self.ui_property.addItem(c.description())

        self.active = self.ui_checkBox.isChecked()
        self.value  = self.ui_value.value()
        self.condition_idx = self.ui_property.currentIndex()
        self.action_name   = self.ui_action.currentText()

        self.ui_checkBox.clicked.connect(self.checkbox_slot)
        self.ui_value.valueChanged.connect(self.value_changed_slot)
        self.ui_property.currentIndexChanged.connect(self.condition_combobox_slot)
        self.ui_action.currentIndexChanged.connect(self.action_combobox_slot)


    def __del__(self):
        self.ui_checkBox.deleteLater()
        self.ui_property.deleteLater()
        self.ui_value.deleteLater()
        self.ui_action.deleteLater()

    def checkbox_slot(self):
        self.active = self.ui_checkBox.isChecked()

    def value_changed_slot(self, value):
        self.value  = value

    def condition_combobox_slot(self, idx):
        self.condition_idx = idx

    def action_combobox_slot(self, idx):
        self.action_name = self.ui_action.currentText()

    # Check is selected condition is satisfied, and run appropriate action if True
    def check(self, data):
        if (not self.active):
            return

        condition = self.conditions[self.condition_idx]
        if (condition.check(data, self.value)):
            act =  self.actions[str(self.action_name)]
            act.act()

    def check_cam(self, data):
        if (not self.active):
            return

        condition = self.conditions[self.condition_idx]
        if (condition.check_cam(data, self.value)):
            act =  self.actions[str(self.action_name)]
            act.act()

    def get_type(self):
        condition = self.conditions[self.condition_idx]
        return condition.type()


# main function to test GUI
def main():
    app = QtGui.QApplication(sys.argv)

    window = CounterConfig()
    window.show()


    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
