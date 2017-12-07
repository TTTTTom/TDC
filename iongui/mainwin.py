# -*- coding:utf-8 -*-
"""
Created on May 1, 2011

@author: Dima
"""
import csv
import sys
import json
from json import JSONEncoder

sys.path.insert(0, '..')
sys.path.insert(0, '..\\DDS')
print sys.path

from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
from mainion import Ui_MainWindow
from timeseq import TimeSeqWindow

#from jsoncoder import IonJSONEncoder


from delayscan import DelayScan
from freqscan import FreqScan
from simplescan import SimpleScan
from iondata import IonData
from ddsdevice import PhaseModulation

from ddsdevice import DDSGenerator
from n5183a import N5183AGenerator
from fit import sine_fit, freq_fit

#import jsonsaver

# Main application for the data processing
class IonApp(QtGui.QMainWindow):
    SIMPLE, FREQ, DELAY = range(3)
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ion_data    = IonData(self.ui)
        self.simple_scan = SimpleScan(self.ui)
        self.freq_scan   = FreqScan(self.ui)
        self.delay_scan  = DelayScan(self.ui)

#        self.phase_modulation = PhaseModulation(self.ui)
        try:
            self.phase_modulation   = PhaseModulation(self.ui)
        except KeyError:
            print "None of the DDS boards are connected"
        
        self.active_plot  = self.SIMPLE
        self.run_button   = self.ui.scan_Button
        self.pause_button = self.ui.pause_Button     
        self.scan_method  = self.ui.scan_method

        self.scan_method.addItems(["Linear", "Random"])

        self.filepath     = ""
        
        # Connect menu signals
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.save_slot)
        QtCore.QObject.connect(self.ui.SaveSettings, QtCore.SIGNAL("triggered()"), self.savesettings_slot)
        QtCore.QObject.connect(self.ui.LoadSettings, QtCore.SIGNAL("triggered()"), self.loadsettings_slot)
        QtCore.QObject.connect(self.ui.actionCounters, QtCore.SIGNAL("triggered()"), self.counter_config_slot)
        QtCore.QObject.connect(self.ui.actionSave_Histogram, QtCore.SIGNAL("triggered()"), self.save_with_histogram_slot)
        QtCore.QObject.connect(self.ui.actionFrequency_Fit, QtCore.SIGNAL("triggered()"), self.freq_fit_slot)
        QtCore.QObject.connect(self.ui.actionSine_Fit, QtCore.SIGNAL("triggered()"), self.sin_fit_slot)
        QtCore.QObject.connect(self.ui.actionControl_Window, QtCore.SIGNAL("triggered()"), self.phase_modulation_slot)


        # connect scan control buttons
        self.run_button.clicked.connect(self.run_slot)
        self.pause_button.clicked.connect(self.pause_slot)

    # User pressed Control Window for the phase modulation
    def phase_modulation_slot(self):
        self.phase_modulation.show()

    # User pressed frequency fit menu
    def freq_fit_slot(self):
        self.freq_scan.fit_menu()
    
    # User chose sine fit menu
    def sin_fit_slot(self):
        self.delay_scan.fit_menu()

    def counter_config_slot(self):
        self.ion_data.show_counter_config()

    # User pressed run button
    def run_slot(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if (self.run_button.isChecked()):
            if (current_tab == 0):
                self.simple_scan.setActive(True)
                self.simple_scan.run_slot()
            elif(current_tab == 1):
                self.freq_scan.setActive(True)
                self.freq_scan.run_slot()
            elif(current_tab == 2):
                self.delay_scan.setActive(True)
                self.delay_scan.run_slot()
        else:
            self.run_stopped_slot()
   
    
        # Change scan / Stop button label
        if (self.run_button.isChecked()):
            self.run_button.setText("Stop")
        else:
            self.run_button.setText("Scan")
            
    # Emitted when scan is finished, clean up everything
    def run_stopped_slot(self):
        self.run_button.setChecked(False)
        self.run_button.setText("Scan")

        self.pause_button.setChecked(False)
        self.pause_button.setText("Pause")
               
        self.simple_scan.setActive(False)
        self.freq_scan.setActive(False)        
        self.delay_scan.setActive(False)

    
    # User pressed pause button
    def pause_slot(self):
        if (self.simple_scan.isActive()): # Simple alignment scan
            self.simple_scan.setActive(False)
            self.run_button.setChecked(False)
            self.run_button.setText("Scan")
            self.pause_button.setChecked(False)
            self.pause_button.setText("Pause")
        elif (self.freq_scan.isActive()):
            if (self.pause_button.isChecked()): # Frequency scan
                self.freq_scan.pause()
                self.pause_button.setText("Resume")
            else:
                self.freq_scan.resume()
                self.pause_button.setText("Pause")
        elif (self.delay_scan.isActive()): # Delay scan
            if (self.pause_button.isChecked()):
                self.delay_scan.pause()
                self.pause_button.setText("Resume")
            else:
                self.delay_scan.resume()
                self.pause_button.setText("Pause")
        else:
            self.pause_button.setChecked(False)
            self.pause_button.setText("Pause")

# Loads the settings for the program from file
    def loadsettings_slot(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Load Settings', self.filepath)
        if ( filename == '' ):
            return
        finfo = QtCore.QFileInfo(filename)
        self.filepath = finfo.path()

        with open(filename, mode='r') as f:
            data = json.load(f)
        f.closed
        print data
        self.load_settings(data)

# Saves settings for the program to file in JSON format (because it is more readable than pickle)
    def savesettings_slot(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save Settings', self.filepath)
        finfo = QtCore.QFileInfo(filename)
        self.filepath = finfo.path()
        if ( filename == '' ):
            return

#        jsonsaver.json_settings.save(self, filename)
        self.json_dump(filename)

    # writes settings to file in the JSON format
    def json_dump(self, filename):
        with open(filename, mode='w') as f:
            json.dump(self, f, sort_keys = False, indent = 4, cls=IonJSONEncoder, skipkeys=True)


    def save_slot(self):
        # Open file and save the data                
#        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', self.filepath)
        if ( filename == '' ):
            return
        finfo = QtCore.QFileInfo(filename)
        self.filepath = finfo.path()

        # Determine active tab
        current_tab = self.ui.tabWidget.currentIndex()
        if (current_tab == 0):
            self.simple_scan.scandata.save(filename)
        elif (current_tab == 1):
            self.freq_scan.scandata.save(filename)
        elif (current_tab == 2):
            self.delay_scan.scandata.save(filename)

        # Save current settings in addition to the data
        self.json_dump(filename + ".set")
        self.emit(QtCore.SIGNAL("saveJSONTimeSeq"), filename + ".seq")

        
    def save_with_histogram_slot(self):
        # Open file and save the data
#        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', self.filepath)
        if ( filename == '' ):
            return
        finfo = QtCore.QFileInfo(filename)
        self.filepath = finfo.path()

        # Determine active tab
        current_tab = self.ui.tabWidget.currentIndex()
        if (current_tab == 0):
            self.simple_scan.scandata.save_with_histogram(filename)
        elif (current_tab == 1):
            self.freq_scan.scandata.save_with_histogram(filename)
        elif (current_tab == 2):
            self.delay_scan.scandata.save_with_histogram(filename)

        # Save current settings in addition to the data
        self.json_dump(filename + ".set")
        self.emit(QtCore.SIGNAL("saveJSONTimeSeq"), filename + ".seq")

        
    # New data ready slot
    def new_data_slot(self):
        # Update histogram and calculate value to plot
        (value, histogram) = self.ion_data.new_histogram()
        
        # Add point to a corresponding graph
        if (self.simple_scan.isActive()):
            self.simple_scan.add_point(value, histogram) 
        elif(self.freq_scan.isActive()):
            self.freq_scan.add_point(value, histogram)
        elif(self.delay_scan.isActive()):
            self.delay_scan.add_point(value, histogram)

    def set_histrogram(self, hist):
        self.ion_data.set_histogram(hist)

    # loads setting from the data structure that we read from the settings file
    def load_settings(self, d):
        try:
            method = d["scan_method"]
            if (method[1] == self.scan_method.itemText(method[0])):
                self.scan_method.setCurrentIndex(method[0])

            self.ion_data.load_settings(d["ion_data"])
            self.delay_scan.load_settings(d["delay_scan"])
            self.freq_scan.load_settings(d["freq_scan"])

        except KeyError:
            print "Unexpected key in the settings data"

    # Parse program settings from the object loaded from JSON file and update appropriate variables
    def json_load(self, d):
        self.load_settings(d)


# Encoder class to save the program data to a more readable format
class IonJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, IonApp):
            return{
              '__type__'   : 'IonApp',
              'ion_data'   : obj.ion_data,
              'simple_scan': obj.simple_scan,
              'freq_scan'  : obj.freq_scan,
              'delay_scan' : obj.delay_scan,
              'scan_method': obj.scan_method,
            }
        elif isinstance(obj, DelayScan):
            return {
                '__type__' : 'DelayScan',
                'chapter'  : obj.chapter,
                'delay'    : obj.delay,
                'start'    : obj.start,
                'stop'     : obj.stop,
                'step'     : obj.step,
                'line'     : obj.line,
                'delaynow' : obj.delaynow,
                'fit'      : obj.fit.fit,
                'run_once' : obj.run_once
            }
        elif isinstance(obj, FreqScan):
            return {
                '__type__'   : 'FreqScan',
                'devices'    : obj.devices,
                'deviceidx'  : obj.deviceidx,
                'propertyidx': obj.propertyidx,
                'fit'        : obj.fit.fit,
                'start'      : obj.start,
                'stop'       : obj.stop,
                'step'       : obj.step
            }
        elif isinstance(obj, IonData):
            return {
                '__Type__':  'IonData',
                "number":    obj.number,
                "applyth":   obj.applyth,
                "nrep":      obj.nrep,
                "threshold": obj.threshold
        }
        elif isinstance(obj, DDSGenerator) or isinstance(obj, N5183AGenerator):
            return{
                "name"        : obj.name,
                "description" : obj.description,
                "properties"  : obj.properties,
                "min"         : obj.min,
                "max"         : obj.max,
                "value"       : obj.value,
                "default"     : obj.default,
                "minscan"     : obj.minscan,
                "maxscan"     : obj.maxscan,
                "stepscan"    : obj.stepscan
        }
        elif isinstance(obj,  freq_fit):
            return {
                "a"    :  obj.a,
                "b"    :  obj.b,
                "freq" :  obj.freq,
                "Tpi"  :  obj.Tpi,
                "T"    :  obj.T
            }
        elif isinstance(obj, sine_fit):
            return {
                "a"    :  obj.a,
                "b"    :  obj.b,
                "Tpi"  :  obj.Tpi
            }
        elif isinstance(obj, SimpleScan):
            return
        elif isinstance(obj, QtGui.QLCDNumber ):
            return obj.value()
        elif isinstance(obj, QtGui.QSpinBox):
            return obj.value()
        elif isinstance(obj, QtGui.QDoubleSpinBox):
            return obj.value()
        elif isinstance(obj, QtGui.QCheckBox):
            return obj.isChecked()
        elif isinstance(obj, QtGui.QRadioButton):
            return obj.isChecked()
        elif isinstance(obj, QtGui.QComboBox):
            return [obj.currentIndex(), str(obj.currentText())]
        elif isinstance(obj,  QtGui.QLabel):
            return str(obj.text())
        else:
            return vars(obj)


# main function to test GUI
#def main():

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    
    ionmain = IonApp()
    ionmain.show()
    
    ionseq = TimeSeqWindow()
    ionseq.show()   
    

    # Connect stuff together
    ionmain.set_histrogram(ionseq.fpga.hist)
    ionmain.ion_data.nrep.valueChanged.connect(ionseq.nrep_changed_slot)
    ionmain.ion_data.counter_config.mask_changed.connect(ionseq.mask_changed_slot)
    
    ionseq.fpga.hready.connect(ionmain.new_data_slot)

    # Traditional signals, things are messy here
    QtCore.QObject.connect(ionmain.simple_scan, QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
    QtCore.QObject.connect(ionmain.freq_scan,   QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
    QtCore.QObject.connect(ionmain.delay_scan,  QtCore.SIGNAL("scanDelayRequest"),  ionseq.scan_delay_slot)
    QtCore.QObject.connect(ionseq           ,   QtCore.SIGNAL("scanLineChanged"),   ionmain.delay_scan.scan_line_slot)
    
    QtCore.QObject.connect(ionmain.freq_scan,   QtCore.SIGNAL("scanFinished"),      ionmain.run_stopped_slot)
    QtCore.QObject.connect(ionmain.delay_scan,  QtCore.SIGNAL("scanFinished"),      ionmain.run_stopped_slot)

    QtCore.QObject.connect(ionmain,             QtCore.SIGNAL("saveJSONTimeSeq"),   ionseq.sequence.json_dump_slot)


    # 
    #ionseq.fpga.hist

    sys.exit(app.exec_())

#if __name__ == "__main__":
    # sys.path.append('C:\\Users\\dzmitry123\\Desktop\\software\\src')
#    main()

