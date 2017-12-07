from PyQt4 import QtCore, QtGui
from simplescan import SimpleScan
from pylab import *
from test_coil_serial import CoilSerial
from test_coil_ui import Ui_MainWindow

class TestCoil(QtGui.QMainWindow):
    def __init__(self, parent=None):
        print "GUI is called"
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.get_now)

        self.DisplayNumber = self.ui.current_label

        self.simple_scan = SimpleScan(self.ui)
        self.test_coil_serial = CoilSerial()

        self.run_button   = self.ui.scan_Button
        self.pause_button = self.ui.pause_Button

        self.run_button.clicked.connect(self.run_slot)
        self.pause_button.clicked.connect(self.pause_slot)

        self.run_delay_timer = QtCore.QTimer() # Timer to generate fake debugging data.
        self.run_delay_timer.setSingleShot(True)
        self.run_delay_timer.timeout.connect(self.new_data_slot)


    def get_now(self):
        value = CoilSerial.getinput()
        print value
        self.DisplayNumber.setText(str(value))

    def run_slot(self):
        if (self.run_button.isChecked()):
            self.simple_scan.setActive(True)
            self.simple_scan.run_slot()
        else:
            self.run_stopped_slot()

        # Change scan / Stop button label
        if (self.run_button.isChecked()):
            self.run_button.setText("Stop")
        else:
            self.run_button.setText("Scan")

    def pause_slot(self):
        # cancel timer if it is active
        if (self.run_delay_timer.isActive()):
            self.run_delay_timer.stop()
            self.new_data_slot()

        self.simple_scan.setActive(False)
        self.run_button.setChecked(False)
        self.run_button.setText("Scan")
        self.pause_button.setChecked(False)
        self.pause_button.setText("Pause")

    def run_stopped_slot(self):
        self.run_button.setChecked(False)
        self.run_button.setText("Scan")

        self.pause_button.setChecked(False)
        self.pause_button.setText("Pause")

        self.simple_scan.setActive(False)
#        self.freq_scan.setActive(False)
#        self.freq_scan.setActive2(False)
#        self.delay_scan.setActive(False)



    def new_data_slot(self):
        value = CoilSerial.getinput()
        print value
        histogram = []
        value2 = []
        fpga_data = []
        self.simple_scan.add_point(value, histogram, value2, fpga_data)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    testcoilmain = TestCoil()
    testcoilmain.show()

    #ionseq = TimeSeqWindow()
    #ionseq.show()

    sys.exit(app.exec_())



