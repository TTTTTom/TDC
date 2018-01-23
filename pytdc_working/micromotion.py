__author__ = 'Roland'

import time
import pickle
import sys

from can_dll import can
from dac_gui import Ui_DACWindow

from PyQt4 import QtCore, QtGui


class DataForPlot():
    def __init__(self, maxsize=20):
        self.data = []
        self.maxsize = maxsize    # Max length of a plot

    # add point to the data
    def add(self, y):
        self.data.insert(0, y)
        if len(self.data) > self.maxsize:
            del self.data[self.maxsize:]

    # returns current data
    def getall(self):
        return self.data

    # returns single data
    def get(self, i):
        return self.data[i]

    # set max size of the data array
    def set_maxsize(self, maxsize):
        self.maxsize = maxsize

    def reset(self):
        self.data = []


# class VladimirDAC():
#     def __init__(self):
#         self.c = can()
#         try:
#             self.load_state()
#         except:
#             self.v = [0.0, 0.0, 0.0, 0.0]

#         for ch, voltage in enumerate(self.v):
#             self.set_voltage(ch, voltage)
#             time.sleep(0.1)

#     # sets output voltage for the given channel
#     def set_voltage(self, channel, voltage):

#         dac_value = self.voltage_to_dac_count(voltage)
#         lbyte = dac_value & 0xFF
#         hbyte = (dac_value >> 8) & 0xFF

#         if channel == 0:
#             cmd = self.c.CMD_CAN_SET_DAC0
#         elif channel == 1:
#             cmd = self.c.CMD_CAN_SET_DAC1
#         elif channel == 2:
#             cmd = self.c.CMD_CAN_SET_DAC2
#         else:
#             cmd = self.c.CMD_CAN_SET_DAC3

#         self.c.open("CAN1", 500)
#         time.sleep(0.05)
#         self.c.send_command(self.c.CAN_PID_device_ID, 0, cmd, lbyte, hbyte)
#         time.sleep(0.05)
#         self.c.close()

#         self.v[channel] = voltage
#         self.save_state()

#     # Convert voltage to dac counts
#     def voltage_to_dac_count(self, voltage):
#         if voltage < -10.0:
#             return -32767
#         elif voltage > 10.0:
#             return 32768
#         else:
#             return int(32767 * voltage / 10.0)

#     # saves DAC voltages to file
#     def save_state(self):
#         with open('dac_state.dat', 'w') as f:
#             pickle.dump(self.v, f)
#         f.closed

#     # loads voltage settings from file
#     def load_state(self):
#         with open('dac_state.dat', 'r') as f:
#             self.v = pickle.load(f)
#         f.closed

class VladimirDAC():
    def __init__(self):
        # self.c = can()
        self.c=0
        try:
            self.load_state()
        except:
            self.v = [0.0, 0.0, 0.0, 0.0]

        for ch, voltage in enumerate(self.v):
            self.set_voltage(ch, voltage)
            time.sleep(0.1)

    # sets output voltage for the given channel
    def set_voltage(self, channel, voltage):

        # dac_value = self.voltage_to_dac_count(voltage)
        # lbyte = dac_value & 0xFF
        # hbyte = (dac_value >> 8) & 0xFF

        # if channel == 0:
        #     cmd = self.c.CMD_CAN_SET_DAC0
        # elif channel == 1:
        #     cmd = self.c.CMD_CAN_SET_DAC1
        # elif channel == 2:
        #     cmd = self.c.CMD_CAN_SET_DAC2
        # else:
        #     cmd = self.c.CMD_CAN_SET_DAC3

        # self.c.open("CAN1", 500)
        # time.sleep(0.05)
        # self.c.send_command(self.c.CAN_PID_device_ID, 0, cmd, lbyte, hbyte)
        # time.sleep(0.05)
        # self.c.close()

        self.v[channel] = voltage
        self.save_state()

    # Convert voltage to dac counts
    def voltage_to_dac_count(self, voltage):
        if voltage < -10.0:
            return -32767
        elif voltage > 10.0:
            return 32768
        else:
            return int(32767 * voltage / 10.0)

    # saves DAC voltages to file
    def save_state(self):
        with open('dac_state.dat', 'w') as f:
            pickle.dump(self.v, f)
        f.closed

    # loads voltage settings from file
    def load_state(self):
        with open('dac_state.dat', 'r') as f:
            self.v = pickle.load(f)
        f.closed


class DACWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        print "DAC is ON"
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_DACWindow()
        self.ui.setupUi(self)

        self.dac = VladimirDAC()

        self.volt_sum = self.dac.v[0] + self.dac.v[1]
        self.volt_diff = self.dac.v[0] - self.dac.v[1]

        self.new_point = True   # First event of a new point
        self.points = 1e15      # High value to avoid the if condition in self.mmmm the very first time that code runs
        self.old_value0 = self.dac.v[0]     # Remember these values in case the run is stopped
        self.old_value1 = self.dac.v[1]

    # signal / slot connection

        self.ui.ch0SpinBox.setValue(self.dac.v[0])
        self.ui.ch1SpinBox.setValue(self.dac.v[1])
        self.ui.ch2SpinBox.setValue(self.dac.v[2])
        self.ui.ch3SpinBox.setValue(self.dac.v[3])


        QtCore.QObject.connect(self.ui.ch0SpinBox,  QtCore.SIGNAL('valueChanged (double)'), self.ch0changed)
        QtCore.QObject.connect(self.ui.ch1SpinBox,  QtCore.SIGNAL('valueChanged (double)'), self.ch1changed)
        QtCore.QObject.connect(self.ui.ch2SpinBox,  QtCore.SIGNAL('valueChanged (double)'), self.ch2changed)
        QtCore.QObject.connect(self.ui.ch3SpinBox,  QtCore.SIGNAL('valueChanged (double)'), self.ch3changed)
        QtCore.QObject.connect(self.ui.scanIntervalLength,  QtCore.SIGNAL('valueChanged (double)'), self.set_step)
        QtCore.QObject.connect(self.ui.numberPoints,  QtCore.SIGNAL('valueChanged (int)'), self.set_step)
        # You click once = signal (even though you did not toggle) -> do not like that
        QtCore.QObject.connect(self.ui.FixVDiffMMMM,  QtCore.SIGNAL('clicked()'), self.clicked)
        QtCore.QObject.connect(self.ui.FixVSumMMMM,  QtCore.SIGNAL('clicked()'), self.clicked)
        QtCore.QObject.connect(self.ui.NoMMMM,  QtCore.SIGNAL('clicked()'), self.clicked)
        # You toggled once = 2 signals -> will cause problems if you connect directly to self.mmmm
        # To our convenience, toggled is always called first, but I still do not know why.
        QtCore.QObject.connect(self.ui.FixVDiffMMMM,  QtCore.SIGNAL('toggled(bool)'), self.toggled)
        QtCore.QObject.connect(self.ui.FixVSumMMMM,  QtCore.SIGNAL('toggled(bool)'), self.toggled)
        QtCore.QObject.connect(self.ui.NoMMMM,  QtCore.SIGNAL('toggled(bool)'), self.toggled)
        QtCore.QObject.connect(self.ui.ChangeV,  QtCore.SIGNAL('clicked()'), self.change_V)
        QtCore.QObject.connect(self.ui.DC_value, QtCore.SIGNAL('valueChanged (double)'), self.ideal_ch3)

        self.timer = QtCore.QTimer()
        # self.connect(self.timer,  QtCore.SIGNAL("timeout()"), self.next_time_step)

        self.volt_axis = DataForPlot(self.ui.numberPoints.value())
        self.amplitude_data = DataForPlot(self.ui.numberPoints.value())
        self.phase_data = DataForPlot(self.ui.numberPoints.value())

        self.is_toggled = False
        self.to_optimize = False
        self.step = 1.0
        self.set_step()
        # self.is_V_changing = False

        # self.active_channel = 0
        self.time_span = 0
        self.time_step = 0
        self.v_small_step = 0
        self.value_at_start = 0
        self.final_value = 0

    #def ideal_ch3(self, DC_V):
    def ideal_ch3(self):
        self.ui.expectedCh3.setText("Ch3="+ str(self.ui.ch0SpinBox.value() - self.ui.ch2SpinBox.value() + self.ui.DC_value.value()) + " for DC=")

    def change_V(self):
        if self.ui.ChangeCh0.isChecked():
            self.ui.ch0SpinBox.setValue(self.dac.v[0] + self.ui.DeltaV.value())
        if self.ui.ChangeCh1.isChecked():
            self.ui.ch1SpinBox.setValue(self.dac.v[1] + self.ui.DeltaV.value())
        if self.ui.ChangeCh2.isChecked():
            self.ui.ch2SpinBox.setValue(self.dac.v[2] + self.ui.DeltaV.value())
        if self.ui.ChangeCh3.isChecked():
            self.ui.ch3SpinBox.setValue(self.dac.v[3] + self.ui.DeltaV.value())
        #self.ui.DeltaV.setValue(0.0)
        print "Voltage(s) shifted"
    #
    # def change_V_smoothly(self):
    #     if self.is_V_changing:
    #         self.ui.ChangeV.setText("Start")
    #         self.is_V_changing = False
    #         self.ui.FinalVoltValue.setDisabled(False)
    #         self.ui.TimeToGetThere.setDisabled(False)
    #         self.ui.ChangeCh0.setDisabled(False)
    #         self.ui.ChangeCh1.setDisabled(False)
    #         self.ui.ChangeCh2.setDisabled(False)
    #         self.ui.ChangeCh3.setDisabled(False)
    #         self.timer.stop()
    #     elif not self.is_V_changing:
    #         self.ui.ChangeV.setText("Stop")
    #         self.is_V_changing = True
    #         self.ui.FinalVoltValue.setDisabled(True)
    #         self.ui.TimeToGetThere.setDisabled(True)
    #         self.ui.ChangeCh0.setDisabled(True)
    #         self.ui.ChangeCh1.setDisabled(True)
    #         self.ui.ChangeCh2.setDisabled(True)
    #         self.ui.ChangeCh3.setDisabled(True)
    #         if self.ui.ChangeCh0.isChecked():
    #             self.change_smooth(0)
    #         elif self.ui.ChangeCh1.isChecked():
    #             self.change_smooth(1)
    #         elif self.ui.ChangeCh2.isChecked():
    #             self.change_smooth(2)
    #         elif self.ui.ChangeCh3.isChecked():
    #             self.change_smooth(3)
    #
    # def change_smooth(self, channel):
    #     self.active_channel = channel
    #     self.value_at_start = self.dac.v[channel]
    #     self.final_value = self.ui.FinalVoltValue.value()
    #     if self.value_at_start == self.final_value:
    #         print "Initial and final values are the same. Nothing to do."
    #         self.ui.ChangeV.click()
    #     else:
    #         self.time_span = self.ui.TimeToGetThere.value()
    #         if self.value_at_start < self.final_value:
    #             self.v_small_step = 0.001  # 0.0001 is too small
    #         elif self.value_at_start > self.final_value:
    #             self.v_small_step = -0.001
    #         self.time_step = self.v_small_step/((self.final_value-self.value_at_start)/self.time_span)
    #         self.timer.start(self.time_step*1000)
    #
    # def next_time_step(self):
    #     current_v_value = self.dac.v[self.active_channel]
    #     if self.active_channel == 0:
    #         self.ui.ch0SpinBox.setValue(current_v_value + self.v_small_step)
    #     elif self.active_channel == 1:
    #         self.ui.ch1SpinBox.setValue(current_v_value + self.v_small_step)
    #     elif self.active_channel == 2:
    #         self.ui.ch2SpinBox.setValue(current_v_value + self.v_small_step)
    #     elif self.active_channel == 3:
    #         self.ui.ch3SpinBox.setValue(current_v_value + self.v_small_step)
    #     current_v_value = self.dac.v[self.active_channel]
    #     if self.value_at_start < self.final_value:
    #         if current_v_value >= self.final_value:
    #             self.ui.ChangeV.click()
    #     elif self.value_at_start > self.final_value:
    #         if current_v_value <= self.final_value:
    #             self.ui.ChangeV.click()

    def clicked(self):
        if self.is_toggled:
            self.mmmm()

    def toggled(self):
        self.is_toggled = True


    def ch0changed(self, value):
        self.dac.set_voltage(0, value)
        self.volt_sum = self.ui.ch0SpinBox.value() + self.ui.ch1SpinBox.value()
        self.volt_diff = self.ui.ch0SpinBox.value() - self.ui.ch1SpinBox.value()
        self.ideal_ch3()

    def ch1changed(self, value):
        self.dac.set_voltage(1, value)
        self.volt_sum = self.ui.ch0SpinBox.value() + self.ui.ch1SpinBox.value()
        self.volt_diff = self.ui.ch0SpinBox.value() - self.ui.ch1SpinBox.value()

    def ch2changed(self, value):
        self.dac.set_voltage(2, value)
        self.ideal_ch3()

    def ch3changed(self, value):
        self.dac.set_voltage(3, value)

    def set_step(self):
        # There are n points and n-1 segments. The factor 1/2 accounts for the factor 2 that appears in volt_sum or
        # volt_diff
        npoints = self.ui.numberPoints.value()
        self.step = self.ui.scanIntervalLength.value()/(2*(npoints-1))
        output_string = str(self.step)
        self.ui.stepLength.setText(output_string[0:6])
        self.volt_axis.set_maxsize(npoints)
        self.amplitude_data.set_maxsize(npoints)
        self.phase_data.set_maxsize(npoints)

    # "mmmm" stands for 'MicroMotion Minimization Mode'
    def mmmm(self):
        self.is_toggled = False
        # Do not forget to implement any changes in FixVDiffMMMM also in FixVSumMMMM
        if self.ui.FixVDiffMMMM.isChecked():
            # if self.is_V_changing:
            #     self.change_V_smoothly()
            if self.points < self.ui.numberPoints.value():
                print "Run stopped, set old voltage values"
                self.ui.ch0SpinBox.setValue(self.old_value0)
                self.ui.ch1SpinBox.setValue(self.old_value1)
            self.reset_plots()
            print "Fixed-Voltage-Difference Micromotion-Minimization Mode selected"    # volt_diff keeps constant
            self.to_optimize = True
            self.new_point = True       # First event of a new point is next
            self.points = 0
            self.ui.ch0SpinBox.setDisabled(True)
            self.ui.ch1SpinBox.setDisabled(True)
            self.ui.countSpinBox.setDisabled(True)
            self.ui.numberPoints.setDisabled(True)
            self.ui.scanIntervalLength.setDisabled(True)
            self.ui.ChangeV.setDisabled(True)
            # Factor 1/4 makes us start the scan half interval behind where we were.
            initial_value0 = self.dac.v[0] - self.ui.scanIntervalLength.value()/4
            initial_value1 = self.dac.v[1] - self.ui.scanIntervalLength.value()/4
            self.old_value0 = self.dac.v[0]     # Remember these values in case the run is stopped
            self.old_value1 = self.dac.v[1]
            if initial_value0 < -10 or initial_value1 < -10:
                print "Voltage out of bound. Set to extremal point (+10 or -10 Volts)"
            self.ui.ch0SpinBox.setValue(initial_value0)
            self.ui.ch1SpinBox.setValue(initial_value1)
        elif self.ui.FixVSumMMMM.isChecked():
            # if self.is_V_changing:
            #     self.change_V_smoothly()
            if self.points < self.ui.numberPoints.value():
                print "Run stopped, set old voltage values"
                self.ui.ch0SpinBox.setValue(self.old_value0)
                self.ui.ch1SpinBox.setValue(self.old_value1)
            self.reset_plots()
            print "Fixed-Voltage-Sum Micromotion-Minimization Mode selected"      # volt_sum keeps constant
            self.to_optimize = True
            self.new_point = True       # First event of a new point is next
            self.points = 0
            self.ui.ch0SpinBox.setDisabled(True)
            self.ui.ch1SpinBox.setDisabled(True)
            self.ui.countSpinBox.setDisabled(True)
            self.ui.numberPoints.setDisabled(True)
            self.ui.scanIntervalLength.setDisabled(True)
            self.ui.ChangeV.setDisabled(True)
            # Factor 1/4 makes us start the scan half interval behind where we were.
            initial_value0 = self.dac.v[0] - self.ui.scanIntervalLength.value()/4
            initial_value1 = self.dac.v[1] + self.ui.scanIntervalLength.value()/4
            self.old_value0 = self.dac.v[0]     # Remember these values in case the run is stopped
            self.old_value1 = self.dac.v[1]
            if initial_value0 < -10 or initial_value1 > 10:
                print "Voltage range out of bound. Set to extremal point (+10 or -10 Volts)"
            self.ui.ch0SpinBox.setValue(initial_value0)
            self.ui.ch1SpinBox.setValue(initial_value1)
        elif self.ui.NoMMMM.isChecked():
            if self.points < self.ui.numberPoints.value():
                print "Run stopped, set old voltage values"
                self.ui.ch0SpinBox.setValue(self.old_value0)
                self.ui.ch1SpinBox.setValue(self.old_value1)
            print "No Micromotion Minimization selected"
            self.points = 1e15  # This allows to use the right voltages at the next toggle if they were changed manually
            self.to_optimize = False
            self.ui.ch0SpinBox.setDisabled(False)
            self.ui.ch1SpinBox.setDisabled(False)
            self.ui.countSpinBox.setDisabled(False)
            self.ui.numberPoints.setDisabled(False)
            self.ui.scanIntervalLength.setDisabled(False)
            self.ui.ChangeV.setDisabled(False)


    def reset_plots(self):
        self.volt_axis.reset()
        self.amplitude_data.reset()
        self.phase_data.reset()
        self.make_plots(self.volt_axis.getall(), self.amplitude_data.getall(), self.phase_data.getall(), "V_diff (V)",
                        "Amplitude (Counts)", "Phase (Degrees)")

    def make_plots(self, x_data, y1_data, y2_data, set_x_label, set_y1_label, set_y2_label):
        self.ui.AmplitudePlot.axes.set_xlabel(set_x_label)
        self.ui.AmplitudePlot.axes.set_ylabel(set_y1_label)
        self.ui.PhasePlot.axes.set_xlabel(set_x_label)
        self.ui.PhasePlot.axes.set_ylabel(set_y2_label)
        self.ui.AmplitudePlot.axes.plot(x_data, y1_data)
        self.ui.AmplitudePlot.draw()
        self.ui.PhasePlot.axes.plot(x_data, y2_data)
        self.ui.PhasePlot.draw()


# main function to test GUI
def main():

    sys.path.append('../')
    app = QtGui.QApplication(sys.argv)

    dac_win = DACWindow()
    dac_win.show()

    sys.exit(app.exec_())


# Call main if the file is started
if __name__ == "__main__":
    main()