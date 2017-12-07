'''
Created on May 28, 2013

@author: cqt
'''

from PyQt4 import QtCore, QtGui

from sideband_cooling_config import Ui_SidebandCoolingDialog

import sys, math


class sideband_ui_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_SidebandCoolingDialog()
        self.ui.setupUi(self)

        self.pumping_time  = 1  # default optical puming time (microseconds)
        self.raman_pi_time = 1  # raman pi time for the sideband transition (\eta \Omega)
        self.n_phonons     = 10 # initial number of phonons
        self.n_cycles      = 40 # initial number of the optical pumping cycles
        self.n_lines       = 2
        
        QtCore.QObject.connect(self.ui.buttonBox, QtCore.SIGNAL('accepted()'), self.on_ok)


    def on_ok(self):
#        self.pumping_time  = self.ui.pump_time.value()  # default optical puming time (microseconds)
#        self.raman_pi_time = self.ui.raman_time.value() # raman pi time for the sideband transition (\eta \Omega)
        self.n_phonons     = self.ui.nphonon.value()    # initial number of phonons
        self.n_cycles      = self.ui.nreps.value()      # initial number of the optical pumping cycles
        self.n_lines       = self.ui.nlines.value()

        print self.pumping_time, self.raman_pi_time, self.n_phonons, self.n_cycles, self.n_lines

    def on_plus(self):
        pass
    
    def on_minus(self):
        pass
        
    # set the values for the controls and show the dialog
    def show(self):
#        self.ui.raman_time.setValue(self.raman_pi_time)
#        self.ui.pump_time.setValue(self.pumping_time)
        self.ui.nphonon.setValue(self.n_phonons)
        self.ui.nreps.setValue(self.n_cycles)
        self.ui.nlines.setValue(self.n_lines)
        
        # Call the parent class
        super(sideband_ui_dialog, self).show()


class TestWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        self.widget = QtGui.QWidget(self)
        self.widget.setObjectName("widget")

#        self.sideband = SidebandSeq(self.widget)
        self.sideband = SidebandChapter(self.widget)

#        self.line   = SeqLine(self.widget)


# main function to test the module
def main():

    app = QtGui.QApplication(sys.argv)
    myapp = TestWindow()
    myapp.show()   
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
