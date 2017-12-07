'''
Created on 17-May-2011

@author: cqt
'''
import csv
from scandata import ScanData
from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
import numpy

from dummydevice import DummyGenerator

#try:
#from ddsdevice import DDSGenerator
#from ddsdevice import Modulation
#except: # If something is wrong with the libraries, load dummy module instead
#    from dummydevice import DummyGenerator as DDSGenerator

try:
    from keithley import KeithleyGenerator
except: # If something is wrong with the libraries, load dummy module instead
    from dummydevice import DummyGenerator as KeithleyGenerator


try:
    from n5183a import N5183AGenerator
except: # If something is wrong with the libraries, load dummy module instead
    from dummydevice import DummyGenerator as N5183AGenerator

#from windfreak rf generator import windfreakgenerator
#from windfreak_rf_generator import WindfreakGenerator

from fit import freq_fit_gui, anticrossing_fit_gui
from iterators import axis_range
from plot import ScanDataPlot


class FreqScan(QtCore.QObject):
    def __init__(self, ui):
        super(FreqScan, self).__init__()
#        self.plot       = ui.freq_scan_qwt_plot
#        self.run        = ui.freq_scan_Button
#        self.run_once   = ui.freq_scan_once
#        self.run_method = ui.freq_scan_method
        self.run         = ui.scan_Button
        self.run_once    = ui.scan_once
        self.scan_method = ui.scan_method
        self.scan_file_path = ""
        self.scan_file_name = ""
        self.ui = ui
        self.iter_num = 0

        self.scandata   = ScanData()

        self.start       = ui.freq_start
        self.stop        = ui.freq_stop
        self.step        = ui.freq_step
        self.devlist     = ui.freq_device
        self.property    = ui.freq_property
        self.current     = ui.freq_current
        self.default     = ui.freq_default
        self.checkbox2    = ui.freq_checkBox_2
        self.start2       = ui.freq_start_2
        self.stop2        = ui.freq_stop_2
        self.step2        = ui.freq_step_2
        self.devlist2     = ui.freq_device_2
        self.property2    = ui.freq_property_2
        self.current2     = ui.freq_current_2
        self.default2     = ui.freq_default_2
        self.description  = ui.freq_description
        self.statusbar    = ui.statusbar
        self.freq_iter  = axis_range(( self.start.value(), self.start2.value()),
                                     ( self.stop.value(), self.stop2.value()),
                                     ( self.step.value(), self.step2.value()),
                                     self.scan_method.currentText() ).get()

        self.freq  = 100.0 # Just to make sure this variable exist everywhere
        self.freq2 = 100.0 # Just to make sure this variable exist everywhere

     #   self.devices     = [DummyGenerator(),
     #                       DDSGenerator("QO0012"), DDSGenerator("QO0053"), DDSGenerator("QO0044"), DDSGenerator("QO0048"), DDSGenerator("QO0049"), DDSGenerator("QO0024"), DDSGenerator("QO0029"), DDSGenerator("QO0032"), DDSGenerator("QO0030"),
     #                       N5183AGenerator()]
        self.devices     = [DummyGenerator()]

        self.deviceidx   = 0
        self.propertyidx = 0
        self.deviceidx2   = 0
        self.propertyidx2 = 0

        self.active       = False
        self.paused       = False

        self.plot = ScanDataPlot(ui.freq_scan_qwt_plot, self.scandata)
        self.fit = self.plot.add_fit(freq_fit_gui)
        self.anticrossing_fit = self.plot.add_fit(anticrossing_fit_gui)

        # Signal / slot connections
        # self.run.clicked.connect(self.run_slot)
        self.devlist.activated.connect(self.device_activated_slot)
        self.property.activated.connect(self.property_activated_slot)
        self.default.valueChanged.connect(self.default_changed_slot)
        self.start.valueChanged.connect(self.scan_range_changed_slot)
        self.stop.valueChanged.connect(self.scan_range_changed_slot)
        self.step.valueChanged.connect(self.scan_range_changed_slot)

        self.devlist2.activated.connect(self.device_activated_slot2)
        self.property2.activated.connect(self.property_activated_slot2)
        self.default2.valueChanged.connect(self.default_changed_slot2)
        self.start2.valueChanged.connect(self.scan_range_changed_slot)
        self.stop2.valueChanged.connect(self.scan_range_changed_slot)
        self.step2.valueChanged.connect(self.scan_range_changed_slot)

        self.checkbox2.stateChanged.connect(self.double_scan_requested_slot)

        self.fill_device_list()


    # loads program setting from a dictionary
    def load_settings(self, data):
        self.fit.load_settings(data['fit'])
        # loads properties for all the generators connected to a computer
        for d in data['devices']:
            for dev in self.devices:
                devname = dev.getName()
                devdescription = dev.getDescription()
                if ( devname == d['name'] and  devdescription == d['description'] ):
                    print "Loading settings for " + d['name'] + " , " + d['description']
                    dev.load_settings(d)

        # Update display for the current property and current generator
        self.property_activated_slot(self.propertyidx)
        self.property_activated_slot2(self.propertyidx2)


    def run_slot(self):
        if (self.isActive()):
            self.scandata.reset()
            self.iter_num = 0
            self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
            self.start_scan()
        else:
            self.restoreDefault()

        if (self.checkbox2.isChecked() == False):
            self.restoreDefault2()

    def scan_line_slot(self, name, line):
        self.chapter.setText(name)
        self.line.setText(str(line))

# Slot when the user changes the
    def device_activated_slot(self, index):
        self.deviceidx = index
        dev = self.devices[index]
        self.property.clear()
        self.property.addItems(dev.getPropertiesList())
        self.property_activated_slot(0)
        self.description.setText(dev.getDescription())

    def device_activated_slot2(self, index):
            self.deviceidx2 = index
            dev = self.devices[index]
            self.property2.clear()
            self.property2.addItems(dev.getPropertiesList())
            self.property_activated_slot2(0)
            self.description.setText(dev.getDescription())


    def property_activated_slot(self, index):
        self.propertyidx = index
        dev     = self.devices[self.deviceidx]
        prlist  = dev.getPropertiesList()
        prop = prlist[index]
#        prop = self.propertyidx

        minprop, maxprop = dev.getPropertyLimits(prop)
        defprop = dev.getProperty(prop)
        minscan, maxscan, stepscan = dev.getScanRange(prop)

        self.current.setText(str( dev.getProperty(prop) ))
        self.default.setMinimum(minprop)
        self.default.setMaximum(maxprop)
        self.default.setValue(defprop)
#        self.default.setValue(dev.getDefault(prop))

        self.start.setMinimum(minprop)
        self.start.setMaximum(maxprop)
        self.start.setValue(minscan)

        self.stop.setMinimum(minprop)
        self.stop.setMaximum(maxprop)
        self.stop.setValue(maxscan)

        self.step.setValue(stepscan)

    def property_activated_slot2(self, index):
            self.propertyidx2 = index
            dev     = self.devices[self.deviceidx2]
            prlist  = dev.getPropertiesList()
            prop = prlist[index]
    #        prop = self.propertyidx

            minprop, maxprop = dev.getPropertyLimits(prop)
            defprop = dev.getProperty(prop)
            minscan, maxscan, stepscan = dev.getScanRange(prop)

            self.current2.setText(str( dev.getProperty(prop) ))
            self.default2.setMinimum(minprop)
            self.default2.setMaximum(maxprop)
            self.default2.setValue(defprop)
    #        self.default.setValue(dev.getDefault(prop))

            self.start2.setMinimum(minprop)
            self.start2.setMaximum(maxprop)
            self.start2.setValue(minscan)

            self.stop2.setMinimum(minprop)
            self.stop2.setMaximum(maxprop)
            self.stop2.setValue(maxscan)

            self.step2.setValue(stepscan)

# Default changed slot
    def default_changed_slot(self, value):
        dev = self.devices[self.deviceidx]
        prlist  = dev.getPropertiesList()
        prop = prlist[self.propertyidx]

        if ( not dev.setDefault(prop, value)):
            return

        if (not self.isActive()):  # Disable if board is in listplay mode!!!!
            dev.setProperty(prop, value)
            self.current.setText(str(dev.getProperty(prop)) )

    def default_changed_slot2(self, value):
            dev = self.devices[self.deviceidx2]
            prlist  = dev.getPropertiesList()
            prop = prlist[self.propertyidx2]

            if ( not dev.setDefault(prop, value)):
                return

            if (not self.isActive()):
                dev.setProperty(prop, value)
                self.current2.setText(str(dev.getProperty(prop)) )



# Slot called if any of scan range controls has changed
    def scan_range_changed_slot(self, value):
        dev = self.devices[self.deviceidx]
        prlist  = dev.getPropertiesList()
        prop = prlist[self.propertyidx]

        start = self.start.value()
        stop  = self.stop.value()
        step =  self.step.value()

        dev.setScanRange(prop, start, stop, step)

        start2 = self.start2.value()
        step2  = self.step2.value()
        if (step != 0):
            stop2 = start2 + step2 * (stop - start) / step
        else:
            stop2 = start2
        self.stop2.setValue(stop2)

        dev2 = self.devices[self.deviceidx2]
        prlist2  = dev.getPropertiesList()
        prop2 = prlist2[self.propertyidx2]

        dev2.setScanRange(prop2, start2, stop2, step2)


# Fit menu selected
    def fit_menu(self):
        self.fit.show()

    def anticrossing_fit_menu(self):
        self.anticrossing_fit.show()

    def double_scan_requested_slot(self):
        self.plot.enable_top_axis(self.checkbox2.isChecked())

    # fills the list of generators 
    def fill_device_list(self):
        list = []
        for dev in self.devices:
            name = dev.getName()
            if (name != ""):
                list.append(name)
            else:
                print "Something bad will happen" #The indices in list won't correspond the ones in self.devices
                list.append("Badness")
        self.devlist.addItems(list)
        self.devlist2.addItems(list)
        self.device_activated_slot(0)
        self.device_activated_slot2(0)


    def setProperty(self, value):
        dev = self.devices[self.deviceidx]
        prlist  = dev.getPropertiesList()
        prop = prlist[self.propertyidx]

        dev.setProperty(prop, value)
        self.current.setText(str(value) )

    def setProperty2(self, value):
        if (self.checkbox2.isChecked() == True):
            dev = self.devices[self.deviceidx2]
            prlist  = dev.getPropertiesList()
            prop = prlist[self.propertyidx2]

            dev.setProperty(prop, value)
            self.current2.setText(str(value) )

    def restoreDefault(self):
        dev = self.devices[self.deviceidx]
        prlist  = dev.getPropertiesList()
        prop = prlist[self.propertyidx]

        dev.setProperty(prop, dev.getDefault(prop))
        self.current.setText(str(dev.getProperty(prop)) )

    def restoreDefault2(self):
        if (self.checkbox2.isChecked() == True):
            dev = self.devices[self.deviceidx2]
            prlist  = dev.getPropertiesList()
            prop = prlist[self.propertyidx2]

            dev.setProperty(prop, dev.getDefault(prop))
            self.current2.setText(str(dev.getProperty(prop)) )

    # returns true if the scan is active
    def isActive(self):
        return self.active

    # sets active status
    def setActive(self, active):
        if(self.active != active):
            self.statusbar.showMessage("Frequency scan is stopped")
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
    def start_scan(self):  # Disable if board is in listplay mode!!!!
        if self.checkbox2.isChecked():
            scanrange = axis_range(( self.start.value(), self.start2.value()),
                                   ( self.stop.value(), self.stop2.value()),
                                   ( self.step.value(), self.step2.value()),
                                     self.scan_method.currentText() )
        else:
             scanrange  = axis_range(( self.start.value(), self.start.value()),
                                     ( self.stop.value(), self.stop.value()),
                                     ( self.step.value(), self.step.value()),
                                       self.scan_method.currentText() )

        scanrange.set_file_name(self.scan_file_name)

        try:
            self.freq_iter = scanrange.get()
        except (ValueError, IOError):
             QtGui.QMessageBox.question(None, "File Error", "Error reading file " + self.scan_file_name, QtGui.QMessageBox.Ok)


        try:
            freqs = self.freq_iter.next()
            self.freq = freqs[0]
            self.setProperty(self.freq)
            if (self.checkbox2.isChecked() == True):
                self.freq2 = freqs[1]
                self.setProperty2(self.freq2)
#            self.current.setText(str(self.freq))

        except StopIteration:
            if self.run_once.isChecked():
                self.stop_scan()
            else:
                self.start_scan()
            return


#            self.stop_scan()
#            return
        # request a scan from FPGA
        self.emit(QtCore.SIGNAL("scanSimpleRequest"), True)
        self.statusbar.showMessage("Frequency scan is active")


    # Stop the scan and restore default value
    def stop_scan(self):
        self.emit(QtCore.SIGNAL("scanFinished"))
        self.restoreDefault()
        if (self.checkbox2.isChecked() == True):
            self.restoreDefault2()
        self.statusbar.showMessage("Frequency scan is stopped")

    # pause the scan 
    def pause(self):
        self.paused = True
        self.statusbar.showMessage("Frequency scan is paused")

    # resume the scan
    def resume(self):
        self.paused = False
        if (self.isActive()):
            self.emit(QtCore.SIGNAL("scanSimpleRequest"), False)
            self.statusbar.showMessage("Frequency scan is resumed")

    def myroot(self, n, r):
        return float(max(numpy.real(numpy.roots([1]+[0]*(r-1)+[-n]))))

    # Adds a point to the plot and request next FPGA run if necessary 
    def add_point(self, value, histogram, counters, fpga_data, root):
        # ignore last data point if program is paused.
        if self.paused:
            return
        scaled_value = self.myroot(value, root)
        if (self.checkbox2.isChecked() == True):
            self.scandata.add_pair(self.freq, scaled_value, histogram, counters, fpga_data, self.freq2 )
        else:
            self.scandata.add_pair(self.freq, scaled_value, histogram, counters, fpga_data)

        # add new         
        if (self.isActive()):
            try:
                freqs = self.freq_iter.next()
                self.freq = freqs[0]
                self.setProperty(self.freq)
                if (self.checkbox2.isChecked() == True):
                    self.freq2 = freqs[1]
                    self.setProperty2(self.freq2)
                if (not self.paused):
                    self.emit(QtCore.SIGNAL("scanSimpleRequest"), False)
            except StopIteration:
                self.iter_num += 1
                if self.run_once.isChecked():
                    self.stop_scan()
                    self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
                else:
                    self.start_scan()
                    self.ui.scan_once.setText("(" + str(self.iter_num) + ") Scan Once")
                return

        # replot the graph
        self.rescale_top_axis()
        self.plot.replot()

    def rescale_top_axis(self):
        # We don't doo double scan
        if (self.checkbox2.isChecked() is False):
            return

        step   = self.step.value()
        step2  = self.step2.value()
        start  = self.start.value()
        start2 = self.start2.value()
        self.plot.rescale_top_axis(start, start2, step, step2)

