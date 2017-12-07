'''
Created on 13-May-2011

@author: cqt
'''
from scandata import ScanData
from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
import numpy
from fit import sine_fit_gui, ramsey_fit_gui, coherent_fit_gui, thermal_fit_gui
from iterators import axis_range
from plot import ScanDataPlot

class DelayScan(QtCore.QObject):
    def __init__(self, ui):
        super(DelayScan, self).__init__()
#        self.plot     = ui.delay_scan_qwt_plot
#        self.run      = ui.delay_scan_Button
#        self.run_once = ui.delay_scan_once
        self.run      = ui.scan_Button
        self.run_once = ui.scan_once
        self.scan_method = ui.scan_method
        self.scandata    = ScanData()
        self.iter_num = 0
        self.ui = ui
        
        self.start    = ui.delay_start
        self.stop     = ui.delay_stop
        self.step     = ui.delay_step
        self.chapter  = ui.delay_chapter_line
        self.line     = ui.delay_line_number
        self.delaynow = ui.current_delay

        self.statusbar = ui.statusbar
        
        self.active   = False
        self.paused   = False

        self.plot = ScanDataPlot(ui.delay_scan_qwt_plot, self.scandata)
        self.fit = self.plot.add_fit(sine_fit_gui)
        self.ramseyfit = self.plot.add_fit(ramsey_fit_gui)
        self.coherent_fit = self.plot.add_fit(coherent_fit_gui)
        self.thermal_fit = self.plot.add_fit(thermal_fit_gui)

        self.delay    = 0.01
        self.scan_file_name = ""
        self.scan_file_path = ""

#       self.run.clicked.connect(self.run_slot)

        # setup signal to request more data
        # self.scanReqSig = QtCore.pyqtSignal(self.delay)

    # loads program settings
    def load_settings(self, data):
        try:
            if (data["__type__"] != "DelayScan"):
                return

            self.fit.load_settings(data["fit"])
            self.ramseyfit.load_settings(data["Ramsey fit"])
            self.step.setValue(data['step'])
            self.start.setValue(data['start'])
            self.stop.setValue(data['stop'])
            self.run_once.setChecked(data['run_once'])
        # Chapter is ignored for now
        except KeyError as e:
            print "Key error in input data: ", e

    def run_slot(self):
        if (self.isActive()):
            self.scandata.reset()
            self.iter_num = 0
            self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
            self.start_scan() 

    def scan_line_slot(self, name, line):
        self.chapter.setText(name)
        self.line.setText(str(line)) 

    # returns true if the scan is active
    def isActive(self):
#        return self.run.isChecked()
        return self.active


    # sets active status
    def setActive(self, active):
        if(self.active != active):
            self.statusbar.showMessage("Delay scan is stopped")
        self.active = active
        if (self.active == False):
            self.paused = False


    def set_scan_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(None, 'Open file', self.scan_file_path)
        if ( filename == '' ):
            return
        self.scan_file_name = filename
        finfo = QtCore.QFileInfo(filename)
        self.scan_file_path = finfo.path()

    # starts the scan
    def start_scan(self):
        scanrange = axis_range( (self.start.value(),), (self.stop.value(),), (self.step.value(),),
                                             self.scan_method.currentText())
        scanrange.set_file_name(self.scan_file_name)

        try:
            self.delay_iter = scanrange.get()
        except (ValueError, IOError):
             QtGui.QMessageBox.question(None, "File Error", "Error reading file " + self.scan_file_name, QtGui.QMessageBox.Ok)

        try:
            d = self.delay_iter.next()
            self.delay = d[0]
            self.delaynow.setText(str(self.delay))
#            self.emit(QtCore.SIGNAL("scanDelayRequest"), self.delay)             # request a scan from FPGA   
        except StopIteration:
            if self.run_once.isChecked():
                self.stop_scan()
            else:
                self.start_scan()
            return

#            self.stop_scan()
#            return
        
        # request a scan from FPGA
        self.emit(QtCore.SIGNAL("scanDelayRequest"), self.delay)
        self.statusbar.showMessage("Delay scan is active")

        
    
    def stop_scan(self):
        self.emit(QtCore.SIGNAL("scanFinished"))
        self.statusbar.showMessage("Delay scan is stopped")

        # pause the scan 
    def pause(self):
        #self.paused = True
        #self.statusbar.showMessage("Delay scan is paused")
        if not self.paused:
            self.paused = True
            self.statusbar.showMessage("Delay scan is paused")


    # resume the scan
    def resume(self):
        #self.paused = False
        if (self.isActive() and self.paused):
            self.paused = False
            self.emit(QtCore.SIGNAL("scanDelayRequest"), self.delay) # ask for next FPGA scan
            self.statusbar.showMessage("Delay scan is resumed")


    def fit_menu(self):
        self.fit.show()

    def ramsey_fit_menu(self):
        self.ramseyfit.show()

    def coherent_fit_menu(self):
        self.coherent_fit.show()

    def thermal_fit_menu(self):
        self.thermal_fit.show()

    def myroot(self, n, r):
        return float(max(numpy.real(numpy.roots([1]+[0]*(r-1)+[-n]))))
    
    def add_point(self, value, histogram, value2, fpga_data, root):
        # ignore last data point if program is paused.
        if self.paused:
            return

        scaled_value = self.myroot(value, root)
        self.scandata.add_pair(self.delay, scaled_value, histogram, value2, fpga_data)
        
        # add new         
        if (self.isActive()):
            try:
                d = self.delay_iter.next()
                self.delay = d[0]
                self.delaynow.setText(str(self.delay))
                if (not self.paused):
                    self.emit(QtCore.SIGNAL("scanDelayRequest"), self.delay) # ask for next FPGA scan
            except StopIteration:
                self.iter_num += 1
                if self.run_once.isChecked():
                    self.stop_scan()
                    self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
                else:
                    self.start_scan()
                    self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
        # replot the graph
        self.plot.replot()
