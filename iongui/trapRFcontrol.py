# program controls EOM frequency for locking to iodine cell

from PyQt4 import QtCore, QtGui
#from trapRFcontrol_ui import Ui_Dialog
from trapRFcontrol import KeithleyGenerator, keithley_control
import sys
import time
import serial

# Main widget
class MyForm():
    def __init__(self, parent=None):
        #print "GUI is called"
        #QtGui.QWidget.__init__(self, parent)
        #self.ui = Ui_Dialog()
        #self.ui.setupUi(self)

        self.set_GPIB_address()
        #self.trapRFopen = KeithleyGenerator(id = "COM19")
        #self.trapRFopen.keithley = keithley_control(id("usb0::0x05E6::0x3390::1373397::INSTR"))
        #self.trapRFopen.__init__()

        #QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.goto_amplitude)

    def set_GPIB_address(self):
        ser.write("++addr16\r")

    def goto_amplitude(self):
        print "change amplitude"
        #time.sleep(0.5)
        ser.write("FUNCtion?\r")
        if ser.read(3) == "SIN":
            ser.write("VOLTage?\r")
            getVoltage = float(ser.read(50))
            diff = getVoltage - float(4.4)
            stepsize=0.2
            steps = round(abs(diff)/stepsize)
            if diff > 0:
                for i in range(steps):
                    self.step_amplitude(stepsize)
            if diff < 0:
                for i in range(steps):
                    self.step_amplitude(-stepsize)


    def step_amplitude(self,stepsize):
        ser.write("VOLTage?\r")
        tempVolt=float(ser.read(50))-float(stepsize)
        ser.write("VOLTage "+str(tempVolt)+"\r")







        #print self.trapRFopen.keithley.get_description()






# execute this if we started this file
if __name__ == "__main__":

    ser = serial.Serial(18,
                        baudrate = 9600,
                        parity = 'N',
                        bytesize = 8,
                        stopbits = 1,
                        rtscts   = 0,
                        timeout  = 1)

    print ser

   # app = QtGui.QApplication(sys.argv)
   # myapp = MyForm()
    #myapp.show()
    #sys.exit(app.exec_())