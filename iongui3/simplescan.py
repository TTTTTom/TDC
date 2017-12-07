'''
Created on 13-May-2011

@author: cqt
'''

from scandata import ScanData
from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
from plot import ScanDataPlot
import numpy

# Alignment scan: repeats experiment indefinitely and and displays the histogram
class SimpleScan(QtCore.QObject):
    def __init__(self, ui):
        super(SimpleScan, self).__init__()
#        self.plot     = ui.simple_scan_plot
#        self.plot     = ui.simple_scan_qwt_plot
 #       self.run      = ui.runButton
        self.run      = ui.scan_Button
        self.reset    = ui.reset_scan_Button
        self.bar      = ui.progressBar
        self.average  = ui.averageNumber
        self.nexplabel= ui.scan_num_exp_label
        self.statusbar= ui.statusbar
        self.scandata = ScanData() 
        self.active   = False

        self.plot = ScanDataPlot(ui.simple_scan_qwt_plot, self.scandata)

        self.run.clicked.connect(self.run_slot)
        self.reset.clicked.connect(self.reset_slot)
              
        # QtCore.QObject.connect(self.run, QtCore.SIGNAL("clicked()"), self.run_slot)
        # self.run.clicked.connect(self.run_slot())


    # returns true if scan is active
    def isActive(self):
#        return self.run.isChecked()
        return self.active


    # Sets active status for the window
    def setActive(self, active):
        if(active == False and self.active == True):
            self.statusbar.showMessage("Alignment scan is stopped")
        self.active = active


    def run_slot(self):
#        if (self.run.isChecked()):
        if (self.active):
            self.emit(QtCore.SIGNAL("scanSimpleRequest"), True)
            self.statusbar.showMessage("Alignment scan is running")
        print "Run slot, simple scan" 

    def reset_slot(self):
#        print "reset clicked"
        self.scandata.reset()
        self.replot()
        
    def myroot(self, n, r):
        return float(max(numpy.real(numpy.roots([1]+[0]*(r-1)+[-n]))))

    def add_point(self, value, histogram, counters, fpga_data, root):
        if (self.run.isChecked()):
            # self.run.clicked.emit(True)
            self.emit(QtCore.SIGNAL("scanSimpleRequest"), False)
        else:
            self.statusbar.showMessage("Alignment scan is stopped")
        scaled_value = self.myroot(value, root)
        self.scandata.add(scaled_value, histogram, counters, fpga_data)
        self.bar.setValue(scaled_value)
        self.replot()

        
    def replot(self):
        self.plot.replot()
        
        # Display average value
        avg, nruns, nexp = self.scandata.get_running_avg()
        if (nexp != 0):
            self.average.display(avg / nruns)
        else :
            self.average.display(0.0)
            
        self.nexplabel.setText("over " + str(nexp) + " experiments")

# 