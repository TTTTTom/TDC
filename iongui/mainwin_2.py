# -*- coding:utf-8 -*-
"""
Created on May 1, 2011

@author: Dima
"""
import csv
import sys
import serial
import time
import json
from json import JSONEncoder

sys.path.insert(0, '..')
sys.path.insert(0, '..\\DDS')
print sys.path

from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
from mainion_2 import Ui_MainWindow
from timeseq import TimeSeqWindow
from fpgaseq import SeqLine

#from jsoncoder import IonJSONEncoder


from delayscan import DelayScan
from freqscan import FreqScan
from simplescan import SimpleScan
from iondata import IonData
from ddsdevice import Modulation
from iodineeom import IodineEOM

from ddsdevice import DDSGenerator
from n5183a import N5183AGenerator
from fit import sine_fit, freq_fit, RamseyFit

from actions import ion_actions
from counters import CounterConfig, Rule

from dds import DDS_list

#from MyCam import MyCam #44, 61, 96, 125, 126

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
        #self.time_seq    = TimeSeqWindow()
        self.phase_modulation = Modulation(self.ui)
        #self.camera = MyCam()
#        try:
#            self.phase_modulation = Modulation(self.ui)
#        except KeyError:
#            print "None of the DDS boards are connected"
#            self.phase_modulation = Modulation(self.ui)
        
        self.active_plot  = self.SIMPLE
        self.run_button   = self.ui.scan_Button
        #self.run_button.setShortcut(QtGui.QApplication.translate("MainWindow", "F11", None, QtGui.QApplication.UnicodeUTF8))
        self.pause_button = self.ui.pause_Button     
        self.scan_method  = self.ui.scan_method

        self.scan_method.addItems(["Linear", "Random", "From File"])

        self.filepath     = ""

        self.run_delay_timer = QtCore.QTimer() # Timer to generate fake debugging data.
        self.run_delay_timer.setSingleShot(True)
        self.run_delay_timer.timeout.connect(self.new_data_slot)


        # Connect menu signals
        QtCore.QObject.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"), self.save_slot)
        QtCore.QObject.connect(self.ui.SaveSettings, QtCore.SIGNAL("triggered()"), self.savesettings_slot)
        QtCore.QObject.connect(self.ui.LoadSettings, QtCore.SIGNAL("triggered()"), self.loadsettings_slot)
        QtCore.QObject.connect(self.ui.actionSave_Histogram, QtCore.SIGNAL("triggered()"), self.save_with_histogram_slot)
        QtCore.QObject.connect(self.ui.actionFrequency_Fit, QtCore.SIGNAL("triggered()"), self.freq_fit_slot)
        QtCore.QObject.connect(self.ui.actionSine_Fit, QtCore.SIGNAL("triggered()"), self.sin_fit_slot)
        QtCore.QObject.connect(self.ui.actionRamsey_Fit, QtCore.SIGNAL("triggered()"), self.ramsey_fit_slot)
        QtCore.QObject.connect(self.ui.actionAnticrossing_Fit, QtCore.SIGNAL("triggered()"), self.anticrossing_fit_slot)
        QtCore.QObject.connect(self.ui.actionCoherent_Fit, QtCore.SIGNAL("triggered()"), self.coherent_fit_slot)
        QtCore.QObject.connect(self.ui.actionThermal_Fit, QtCore.SIGNAL("triggered()"), self.thermal_fit_slot)
        QtCore.QObject.connect(self.ui.actionControl_Window, QtCore.SIGNAL("triggered()"), self.phase_modulation_slot)
        QtCore.QObject.connect(self.ui.actionCounters, QtCore.SIGNAL("triggered()"), self.counters_settings_slot)
        QtCore.QObject.connect(self.ui.actionCounters_Plot, QtCore.SIGNAL("triggered()"), self.counters_plot_slot)
        QtCore.QObject.connect(self.ui.actionSet_Scan_File, QtCore.SIGNAL("triggered()"), self.set_scan_file_slot)
        QtCore.QObject.connect(self.ui.actionEOM_GUI, QtCore.SIGNAL("triggered()"), self.eom_gui_slot)
        #QtCore.QObject.connect(self.ui.actionOpenCam, QtCore.SIGNAL("triggered()"), self.open_cam_slot)



        # connect scan control buttons
        self.run_button.clicked.connect(self.run_slot)
        self.pause_button.clicked.connect(self.pause_slot)
        self.ui.resume_Button.clicked.connect(self.pause_slot)

        # serial connection
        #self.ser = serial.Serial(3,
        #                baudrate = 9600,
        #                parity = 'N',
        #                bytesize = 8,
        #                stopbits = 1,
        #                rtscts   = 0,
        #                timeout  = 1)



        self.iodine       = IodineEOM()
        #self.iodine.show()
        self.AOM_crystallize0 = self.ui.crystallize_doubleSpinBox0
        self.AOM_crystallize1 = self.ui.crystallize_doubleSpinBox1

        #self.ser_set_GPIB_address()

        QtCore.QObject.connect(self.ui.crystallize_button0, QtCore.SIGNAL('clicked()'), self.need_to_crystallize)
        QtCore.QObject.connect(self.ui.crystallize_button1, QtCore.SIGNAL('clicked()'), self.crystallized)

    #def open_cam_slot(self):
        #self.camera.show()

    def eom_gui_slot(self):
        self.iodine.show()
        self.iodine.initialize()

    # Ask for confirmation if user wants to close the window
    def closeEvent(self, event):
        answer = QtGui.QMessageBox.question(self, "Close window confirmation",
                                            "Are you sure you want to close this window ?",
                                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Cancel)
        if answer == QtGui.QMessageBox.Ok:
            event.accept() # let the window close
        else:
            event.ignore() # Ignore the attempt to close window


    # hq added eom freq controls

    def need_to_crystallize(self):
        # Set button colors to show what is going on
        self.ui.crystallize_button0.setStyleSheet("background-color: red")
        self.ui.crystallize_button1.setStyleSheet("background-color: lightgray")

        ## change iodine cell EOM frequency
        #self.iodine.goto_freq10272MHz()
        ##self.ser_goto_amplitude(4.2) #to control trap RF Agilent with computer
        ## change AOM efficiency
        dev = self.freq_scan.devices[1] #DDSQ0012
        prlist = dev.getPropertiesList()
        prop = prlist[10] #Ch 1 Amplitude
        dev.setProperty(prop,self.AOM_crystallize0.value())
        gs = ionseq.sequence_get()
        gs2 = gs[0].bitarray
        if (self.ui.Lower_Trap_checkBox.isChecked()):
            gs2[8] = 0 #set to low RF trap voltage
        # deprecated gs2[16] = 0 #set to open shutter for strong beam
        current = gs2
        current = ionseq.fpga.bound(current)
        ionseq.fpga.fpgaseq = []
        ionseq.fpga.fpgaseq.append(SeqLine(gs[0].delay, gs[0].scanned, current.copy() ) )
        # the rest of the lines
        for l in gs[1:]:
            current = ionseq.fpga.nextline(current, l.bitarray)
            ionseq.fpga.fpgaseq.append(SeqLine(l.delay, l.scanned, current.copy()))
        ionseq.fpga.seqString()
        ionseq.fpga.write()
#        ionseq.fpga.usb.write(ionseq.fpga.fpgastr)
        #self.time_seq.fpga.setSeq(self.time_seq.sequence_get())


    def crystallized(self):
        # Set button colors to show what is going on
        self.ui.crystallize_button0.setStyleSheet("background-color: lightgray")
        self.ui.crystallize_button1.setStyleSheet("background-color: green")

        #self.iodine.goto_freq10262MHz()
        ##self.ser_goto_amplitude(6.0) #to control trap RF Agilent with computer
        dev = self.freq_scan.devices[1] #DDSQ0012
        prlist = dev.getPropertiesList()
        prop = prlist[10] #Ch 1 Amplitude
        dev.setProperty(prop,self.AOM_crystallize1.value())
        gs = ionseq.sequence_get()
        gs2 = gs[0].bitarray
        gs2[8] = 1 #set to high RF trap voltage
        # deprecated gs2[16] = 1 #set to close shutter for strong beam
        current = gs2
        current = ionseq.fpga.bound(current)
        ionseq.fpga.fpgaseq = []
        ionseq.fpga.fpgaseq.append(SeqLine(gs[0].delay, gs[0].scanned, current.copy() ) )
        # the rest of the lines
        for l in gs[1:]:
            current = ionseq.fpga.nextline(current, l.bitarray)
            ionseq.fpga.fpgaseq.append(SeqLine(l.delay, l.scanned, current.copy()))
        ionseq.fpga.seqString()
        ionseq.fpga.write()
#        ionseq.fpga.usb.write(ionseq.fpga.fpgastr)

    def pause_and_crystallize_slot(self):
        self.external_pause_slot()
        self.need_to_crystallize()

    # hq added serial connections
    #def ser_set_GPIB_address(self):
    #    self.ser.write("++addr10\r")

    #def ser_goto_amplitude(self,setPoint):
    #    print "change amplitude"
    #    self.ser.write("FUNCtion?\r")
    #    if self.ser.read(3) == "SIN":
    #        self.ser.write("VOLTage?\r")
    #        getVoltage = float(self.ser.read(50))
    #        diff = getVoltage - float(setPoint)
    #        stepsize=0.3
    #        steps = int(round(abs(diff)/stepsize))
    #        print steps
    #        if diff > 0:
    #            for i in range(steps):
    #                self.ser_step_amplitude(stepsize)
    #        if diff < 0:
    #            for i in range(steps):
    #                self.ser_step_amplitude(-stepsize)


    #def ser_step_amplitude(self,stepsize):
    #    self.ser.write("VOLTage?\r")
    #    tempVolt=float(self.ser.read(50))-float(stepsize)
    #    self.ser.write("VOLT "+str(tempVolt)+"\r")
    #    time.sleep(0.2)


    def phase_modulation_slot(self):
        self.iodine.show()

    # User pressed Control Window for the phase modulation
    def phase_modulation_slot(self):
        self.phase_modulation.show()

    # User pressed frequency fit menu
    def freq_fit_slot(self):
        self.freq_scan.fit_menu()
    
    # User chose sine fit menu
    def sin_fit_slot(self):
        self.delay_scan.fit_menu()

    # User chose ramsey fit menu
    def ramsey_fit_slot(self):
        self.delay_scan.ramsey_fit_menu()

    def anticrossing_fit_slot(self):
        self.freq_scan.anticrossing_fit_menu()

    def coherent_fit_slot(self):
        self.delay_scan.coherent_fit_menu()

    def thermal_fit_slot(self):
        self.delay_scan.thermal_fit_menu()

    # Set the file with the scan parameters
    def set_scan_file_slot(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if(current_tab == 1):
            self.freq_scan.set_scan_file()
        elif(current_tab == 2):
            self.delay_scan.set_scan_file()

    # User pressed run button
    def run_slot(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if (self.run_button.isChecked()):
            print "Run button checked"
            if (current_tab == 0):
                self.simple_scan.setActive(True)
                self.simple_scan.run_slot()
            elif(current_tab == 1):
                self.freq_scan.setActive(True)
#                self.freq_scan.setActive2(True)
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

    # Other function inside the program (not a user) wants to pause
    def external_pause_slot(self):
        if (self.pause_button.isChecked()):
            self.pause_button.setChecked(False)
        #     self.pause_button.setText("Pause")
        else:
            self.pause_button.setChecked(True)
        #     self.pause_button.setText("Resume")
        self.pause_slot()

    # Emitted when scan is finished, clean up everything
    def run_stopped_slot(self):
        self.run_button.setChecked(False)
        self.run_button.setText("Scan")

        self.pause_button.setChecked(False)
        # self.pause_button.setText("Pause")
        self.ui.resume_Button.setChecked(False)
               
        self.simple_scan.setActive(False)
        self.freq_scan.setActive(False)
#        self.freq_scan.setActive2(False)
        self.delay_scan.setActive(False)

    
    # User pressed pause button
    def pause_slot(self):
        # cancel timer if it is active
        if (self.run_delay_timer.isActive()):
            self.run_delay_timer.stop()
            self.new_data_slot()

        if (self.simple_scan.isActive()): # Simple alignment scan
            if self.ui.resume_Button.isChecked():
                self.ui.resume_Button.setChecked(False) # Nothing happens
            elif self.pause_button.isChecked():
                self.simple_scan.setActive(False)
                self.run_button.setChecked(False)
                self.run_button.setText("Scan")
                self.pause_button.setChecked(False)
                # self.pause_button.setText("Pause")
                self.ui.resume_Button.setChecked(False)
            else:
                print "Error pausing or resuming"
        elif (self.freq_scan.isActive()):
            if (self.pause_button.isChecked()): # Frequency scan
                self.freq_scan.pause()
                self.pause_button.setChecked(False)
                # self.pause_button.setText("Resume")
            elif self.ui.resume_Button.isChecked():
                self.freq_scan.resume()
                self.ui.resume_Button.setChecked(False)
                # self.pause_button.setText("Pause")
            else:
                print "Error pausing or resuming"
        elif (self.delay_scan.isActive()): # Delay scan
            if (self.pause_button.isChecked()):
                self.delay_scan.pause()
                self.pause_button.setChecked(False)
                # self.pause_button.setText("Resume")
            elif self.ui.resume_Button.isChecked():
                self.delay_scan.resume()
                self.ui.resume_Button.setChecked(False)
                # self.pause_button.setText("Pause")
            else:
                print "Error pausing or resuming"
        else: # Nothing active, nothing happens
            self.pause_button.setChecked(False)
            # self.pause_button.setText("Pause")
            self.ui.resume_Button.setChecked(False)

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
#        print data
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

    # Counter item in settings menu triggers this
    def counters_settings_slot(self):
        self.ion_data.show_counter_config()

    # Show counter confog dialog when menu item is triggered
    def counters_plot_slot(self):
        current_tab = self.ui.tabWidget.currentIndex()
        if (current_tab == 0):
            self.simple_scan.plot.config_gui.show()
        elif(current_tab == 1):
           self.freq_scan.plot.config_gui.show()
        elif(current_tab == 2):
           self.delay_scan.plot.config_gui.show()


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


    # if necessary, introduce a delay before proceeding to the next point
    def new_data_delay_slot(self):
        delay = self.ion_data.counter_config.ui.expDelay.value()
        if delay == 0.0:
            self.new_data_slot()
        else:
            self.run_delay_timer.start(delay)
        
    # New data ready slot
    def new_data_slot(self):
        # Update histogram and calculate value to plot
        #(value, histogram, value2, fpga_data) = self.ion_data.new_histogram(self.camera.get_intensity())
        (value, histogram, value2, fpga_data) = self.ion_data.new_histogram()

        # Add point to a corresponding graph
        if (self.simple_scan.isActive()):
            self.simple_scan.add_point(value, histogram, value2, fpga_data, self.ui.ionnumberBox.value())
        elif(self.freq_scan.isActive()):
            self.freq_scan.add_point(value, histogram, value2, fpga_data, self.ui.ionnumberBox.value())
        elif(self.delay_scan.isActive()):
            self.delay_scan.add_point(value, histogram, value2, fpga_data, self.ui.ionnumberBox.value())

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
            self.phase_modulation.load_settings(d["dds"])

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
              'dds'        : obj.phase_modulation
            }
        elif isinstance(obj, Modulation):
            return {
                'ddslist'  : obj.copyDDSList
            }
        elif isinstance(obj, DDS_list):
            return obj.get_all_settings()
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
                'Ramsey fit'      : obj.ramseyfit.fit,
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
                'step'       : obj.step,
                'deviceidx2' : obj.deviceidx2,
                'propertyidx2': obj.propertyidx2,
                'start2'     : obj.start2,
                'stop2'      : obj.stop2,
                'step2'      : obj.step2,
                'checkbox2'  : obj.checkbox2
            }
        elif isinstance(obj, IonData):
            return {
                '__Type__':  'IonData',
                "number":    obj.number,
                "applyth":   obj.applyth,
                "nrep":      obj.nrep,
                "threshold": obj.threshold,
                "counter_config": obj.counter_config
        }
        elif isinstance(obj, CounterConfig):
            return {
                "checkboxes" :obj.checkboxes,
                "rules":      obj.rules
            }
        elif isinstance(obj, Rule):
            return {
                "index":         obj.index,
                "active":        obj.active,
                "value":         obj.value,
                "condition_idx": obj.condition_idx,
                "action_name":   obj.action_name,
                "ui_property":   obj.ui_property
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
        elif isinstance(obj, RamseyFit):
            return {
                "a"    :  obj.a,
                "b"    :  obj.b,
                "Frequency"  :  obj.f,
                "Decoherence time"  :  obj.decay
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
    
#    ionseq.fpga.hready.connect(ionmain.new_data_slot)
    ionseq.fpga.hready.connect(ionmain.new_data_delay_slot)

    # Traditional signals, things are messy here
    QtCore.QObject.connect(ionmain.simple_scan, QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
    QtCore.QObject.connect(ionmain.freq_scan,   QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
    QtCore.QObject.connect(ionmain.delay_scan,  QtCore.SIGNAL("scanDelayRequest"),  ionseq.scan_delay_slot)
    QtCore.QObject.connect(ionseq           ,   QtCore.SIGNAL("scanLineChanged"),   ionmain.delay_scan.scan_line_slot)
    
    QtCore.QObject.connect(ionmain.freq_scan,   QtCore.SIGNAL("scanFinished"),      ionmain.run_stopped_slot)
    QtCore.QObject.connect(ionmain.delay_scan,  QtCore.SIGNAL("scanFinished"),      ionmain.run_stopped_slot)

    QtCore.QObject.connect(ionmain,             QtCore.SIGNAL("saveJSONTimeSeq"),   ionseq.sequence_json_dump_slot)

# Triggered by various conditions (loss of ion, etc)
    QtCore.QObject.connect(ion_actions["Pause"], QtCore.SIGNAL("pauseActionRequest"), ionmain.external_pause_slot)
    QtCore.QObject.connect(ion_actions["Pause for 5 sec"], QtCore.SIGNAL("pauseActionRequest"), ionmain.external_pause_slot)
    #QtCore.QObject.connect(ionmain.ion_data.counter_config, QtCore.SIGNAL("crystallizeActionRequest"), ionmain.pause_and_crystallize_slot)
    QtCore.QObject.connect(ion_actions["Pause & Crystallize"], QtCore.SIGNAL("crystallizeActionRequest"), ionmain.pause_and_crystallize_slot)



    sys.exit(app.exec_())

#if __name__ == "__main__":
    # sys.path.append('C:\\Users\\dzmitry123\\Desktop\\software\\src')
#    main()

