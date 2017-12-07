'''
Created on 19-May-2011

@author: cqt

v2 by Roland
'''
import time
from dds import DDS, DDS_list
from dummydevice import FreqGenerator
from dummydevice import DummyGenerator
import ddsgui
import csv

from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5

DDSList = DDS_list()
        
# DDS generator for debug purposes
class DDSGenerator(FreqGenerator):
    def __init__(self, SerNumber):
        FreqGenerator.__init__(self)
        try: 
            self.dds        = DDSList.GetBoard(SerNumber)        
            self.name       = "DDS" + str(SerNumber)
            self.description= "CQT DDS Generator: " + self.dds.GetDescription()
            self.properties = ["CH0, Frequency", "CH0, Amplitude", "CH0, Phase",
                               "CH0, FrequencyWord1", "CH0, FrequencyWord2", "CH0, FrequencyWord3",
                               "CH0, PhaseWord1", "CH0, PhaseWord2", "CH0, PhaseWord3",
                               "CH1, Frequency", "CH1, Amplitude", "CH1, Phase",
                               "CH1, FrequencyWord1", "CH1, FrequencyWord2", "CH1, FrequencyWord3",
                               "CH1, PhaseWord1", "CH1, PhaseWord2", "CH1, PhaseWord3"]
            self.min     = {"CH0, Frequency": 0.2,   "CH0, Amplitude" : 0,    "CH0, Phase" :0,
                            "CH0, FrequencyWord1": 0.2, "CH0, FrequencyWord2": 0.2, "CH0, FrequencyWord3": 0.2,
                            "CH0, PhaseWord1" :0, "CH0, PhaseWord2" :0, "CH0, PhaseWord3" :0,
                            "CH1, Frequency": 0.2,   "CH1, Amplitude" : 0,    "CH1, Phase" :0,
                            "CH1, FrequencyWord1": 0.2, "CH1, FrequencyWord2": 0.2, "CH1, FrequencyWord3": 0.2,
                            "CH1, PhaseWord1" :0, "CH1, PhaseWord2" :0, "CH1, PhaseWord3" :0}
            self.max     = {"CH0, Frequency": 200,   "CH0, Amplitude" : 1023,   "CH0, Phase" :360,
                            "CH0, FrequencyWord1": 200, "CH0, FrequencyWord2": 200, "CH0, FrequencyWord3": 200,
                            "CH0, PhaseWord1" :360, "CH0, PhaseWord2" :360, "CH0, PhaseWord3" :360,
                            "CH1, Frequency": 200,   "CH1, Amplitude" : 1023,   "CH1, Phase" :360,
                            "CH1, FrequencyWord1": 200, "CH1, FrequencyWord2": 200, "CH1, FrequencyWord3": 200,
                            "CH1, PhaseWord1" :360, "CH1, PhaseWord2" :360, "CH1, PhaseWord3" :360}
            self.minscan = {"CH0, Frequency": 99.0,   "CH0, Amplitude" : 0,    "CH0, Phase" :0,
                            "CH0, FrequencyWord1": 99.0, "CH0, FrequencyWord2": 99.0, "CH0, FrequencyWord3": 99.0,
                            "CH0, PhaseWord1" :0, "CH0, PhaseWord2" :0, "CH0, PhaseWord3" :0,
                            "CH1, Frequency": 99.0,   "CH1, Amplitude" : 0,    "CH1, Phase" :0,
                            "CH1, FrequencyWord1": 99, "CH1, FrequencyWord2": 0.2, "CH1, FrequencyWord3": 0.2,
                            "CH1, PhaseWord1" :0, "CH1, PhaseWord2" :0, "CH1, PhaseWord3" :0}
            self.maxscan = {"CH0, Frequency": 101.0,   "CH0, Amplitude" : 1023,   "CH0, Phase" :360,
                            "CH0, FrequencyWord1": 101.0, "CH0, FrequencyWord2": 101.0, "CH0, FrequencyWord3": 101.0,
                            "CH0, PhaseWord1" :360, "CH0, PhaseWord2" :360, "CH0, PhaseWord3" :360,
                            "CH1, Frequency": 101.0,   "CH1, Amplitude" : 1023,   "CH1, Phase" :360,
                            "CH1, FrequencyWord1": 101.0, "CH1, FrequencyWord2": 101.0, "CH1, FrequencyWord3": 101.0,
                            "CH1, PhaseWord1" :360, "CH1, PhaseWord2" :360, "CH1, PhaseWord3" :360}
            self.stepscan= {"CH0, Frequency": 0.1,   "CH0, Amplitude" : 1,    "CH0, Phase" :1,
                            "CH0, FrequencyWord1": 0.1, "CH0, FrequencyWord2": 0.1, "CH0, FrequencyWord3": 0.1,
                            "CH0, PhaseWord1" :1, "CH0, PhaseWord2" :1, "CH0, PhaseWord3" :1,
                            "CH1, Frequency": 0.1,   "CH1, Amplitude" : 1,    "CH1, Phase" :1,
                            "CH1, FrequencyWord1": 0.1, "CH1, FrequencyWord2": 0.1, "CH1, FrequencyWord3": 0.1,
                            "CH1, PhaseWord1" :1, "CH1, PhaseWord2" :1, "CH1, PhaseWord3" :1}
            self.value   = {"CH0, Frequency": 100,   "CH0, Amplitude" : 512,    "CH0, Phase" :0,
                            "CH0, FrequencyWord1": 100, "CH0, FrequencyWord2": 100, "CH0, FrequencyWord3": 100,
                            "CH0, PhaseWord1" :0, "CH0, PhaseWord2" :0, "CH0, PhaseWord3" :0,
                            "CH1, Frequency": 100,   "CH1, Amplitude" : 512,    "CH1, Phase" :0,
                            "CH1, FrequencyWord1": 100, "CH1, FrequencyWord2": 100, "CH1, FrequencyWord3": 100,
                            "CH1, PhaseWord1" :0, "CH1, PhaseWord2" :0, "CH1, PhaseWord3" :0}
            defaults     =   self.dds.GetSettings()
            self.default = {"CH0, Frequency": defaults["freq0"] / 1000000.0, "CH0, Amplitude" : defaults["ampl0"], "CH0, Phase" :defaults["phase0"],
                            "CH0, FrequencyWord1": defaults["freq1ch0"] / 1000000.0, "CH0, FrequencyWord2": defaults["freq2ch0"] / 1000000.0, "CH0, FrequencyWord3": defaults["freq3ch0"] / 1000000.0,
                            "CH0, PhaseWord1" :defaults["phase1ch0"], "CH0, PhaseWord2" :defaults["phase2ch0"], "CH0, PhaseWord3" :defaults["phase3ch0"],
                            "CH1, Frequency": defaults["freq1"] / 1000000.0, "CH1, Amplitude" : defaults["ampl1"], "CH1, Phase" :defaults["phase1"],
                            "CH1, FrequencyWord1": defaults["freq1ch1"] / 1000000.0, "CH1, FrequencyWord2": defaults["freq2ch1"] / 1000000.0, "CH1, FrequencyWord3": defaults["freq3ch1"] / 1000000.0,
                            "CH1, PhaseWord1" :defaults["phase1ch1"], "CH1, PhaseWord2" :defaults["phase2ch1"], "CH1, PhaseWord3" :defaults["phase3ch1"]}



            time.sleep(0.1) 
            print "Set properties of:", SerNumber
            for p in self.default.iterkeys():
                self.setProperty(p, self.default[p] )
        except ValueError:
            print "CQT DDS Device not found"
        except KeyError:
            print "DDS device " + SerNumber + " not found..."
            self.name       = "Dummy"
            self.description= "Dummy generator instead of missing " +  SerNumber
            self.properties = ["Frequency", "Amplitude", "Phase"]
            self.min     = {"Frequency": 1,   "Amplitude" : 0,    "Phase" :0}
            self.max     = {"Frequency": 200, "Amplitude" : 1023, "Phase" :360}
            self.value   = {"Frequency": 100, "Amplitude" : 512,  "Phase" :0}
            self.default = {"Frequency": 120, "Amplitude" : 600,  "Phase" :180}
            self.minscan  = {"Frequency": 1,   "Amplitude" : 0,    "Phase" :0}
            self.maxscan  = {"Frequency": 200, "Amplitude" : 1023, "Phase" :360}
            self.stepscan = {"Frequency": 1, "Amplitude" : 1,  "Phase" : 1}
            print "...Dummy loaded instead"
    
    def setDefault(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        self.default[property] = value
        return True

    
    def setProperty(self, property, value):
        if property not in self.properties:
            print "This is not a property"
            return False
        
        if (value > self.max[property]):
            print "Value of the property exceeds maximum allowed"
            return False        
        if (value < self.min[property]):
            print "Value of", property ,"is under minimum allowed:", value ,"<", self.min[property]
            return False
        
        print "Set property:", property     #Eventually update with the new frequency words
        if   (property == "CH0, Frequency"):
            self.dds.SetFrequency(0, value * 1000000.0)
        elif (property == "CH0, FrequencyWord1"):
            self.dds.SetFrequencyWord(0, value * 1000000.0, 0x00)
        elif (property == "CH0, FrequencyWord2"):
            self.dds.SetFrequencyWord(0, value * 1000000.0, 0x01)
        elif (property == "CH0, FrequencyWord3"):
            self.dds.SetFrequencyWord(0, value * 1000000.0, 0x02)
        elif (property == "CH0, Amplitude"):
            self.dds.SetAmplitude(0, int(value))
        elif (property == "CH0, Phase"):
            self.dds.SetPhase(0, value)
        elif (property == "CH0, PhaseWord1"):
            self.dds.SetPhaseWord(0, value, 0x00)
        elif (property == "CH0, PhaseWord2"):
            self.dds.SetPhaseWord(0, value, 0x01)
        elif (property == "CH0, PhaseWord3"):
            self.dds.SetPhaseWord(0, value, 0x02)
        elif (property == "CH1, Frequency"):
            self.dds.SetFrequency(1, value * 1000000.0)
        elif (property == "CH1, FrequencyWord1"):
            self.dds.SetFrequencyWord(1, value * 1000000.0, 0x00)
        elif (property == "CH1, FrequencyWord2"):
            self.dds.SetFrequencyWord(1, value * 1000000.0, 0x01)
        elif (property == "CH1, FrequencyWord3"):
            self.dds.SetFrequencyWord(1, value * 1000000.0, 0x02)
        elif (property == "CH1, Amplitude"):
            self.dds.SetAmplitude(1, int(value))
        elif (property == "CH1, Phase"):
            self.dds.SetPhase(1, value)
        elif (property == "CH1, PhaseWord1"):
            self.dds.SetPhaseWord(1, value, 0x00)
        elif (property == "CH1, PhaseWord2"):
            self.dds.SetPhaseWord(1, value, 0x01)
        elif (property == "CH1, PhaseWord3"):
            self.dds.SetPhaseWord(1, value, 0x02)
        else:
            print "Property is not listed, maybe you are not using a DDS board (like Dummy)"
            
        self.value[property] = value
        return True


class Modulation(QtGui.QDialog):
    def __init__(self, parent=None):
        print "__init__ is called"
        QtGui.QWidget.__init__(self, None)
        self.uiM = ddsgui.Ui_DDSDialog()
        self.uiM.setupUi(self)
        self.current_board = ""
        self.copyDDSList = DDSList

# You can enable them later and make them crosstalk with MainWindow
        self.uiM.ampl0.setDisabled(1)
        self.uiM.freq0.setDisabled(1)
        self.uiM.phase0.setDisabled(1)
        self.uiM.ampl1.setDisabled(1)
        self.uiM.freq1.setDisabled(1)
        self.uiM.phase1.setDisabled(1)
        self.uiM.resetButton.setDisabled(1)
        self.uiM.ampl0ch0.setDisabled(1)
        self.uiM.ampl0ch1.setDisabled(1)
        self.uiM.freq0ch0.setDisabled(1)
        self.uiM.freq0ch1.setDisabled(1)
        self.uiM.phase0ch0.setDisabled(1)
        self.uiM.phase0ch1.setDisabled(1)

# Must be
        self.uiM.ListplayMode.setDisabled(1)

        
# Fills the boards list in the GUI
        self.uiM.sernumBox.addItems(DDSList.board_list())
        
# Connect signals and slots
        QtCore.QObject.connect(self.uiM.freq0, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq0_changed)
        QtCore.QObject.connect(self.uiM.freq1, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq1_changed)
        QtCore.QObject.connect(self.uiM.phase0, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase0_changed)
        QtCore.QObject.connect(self.uiM.phase1, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase1_changed)
        QtCore.QObject.connect(self.uiM.ampl0, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl0_changed)
        QtCore.QObject.connect(self.uiM.ampl1, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl1_changed)
        QtCore.QObject.connect(self.uiM.resetButton, QtCore.SIGNAL('clicked()'), self.slot_reset_clicked)
        QtCore.QObject.connect(self.uiM.sernumBox, QtCore.SIGNAL('activated(QString)'), self.slot_board_selected)
        QtCore.QObject.connect(self.uiM.SingleTone, QtCore.SIGNAL('clicked(bool)'), self.single_tone_selected)
        QtCore.QObject.connect(self.uiM.PhaseModulation, QtCore.SIGNAL('clicked(bool)'), self.phase_modulation_selected)
        QtCore.QObject.connect(self.uiM.FrequencyModulation, QtCore.SIGNAL('clicked(bool)'), self.freq_modulation_selected)
        QtCore.QObject.connect(self.uiM.AmplitudeModulation, QtCore.SIGNAL('clicked(bool)'), self.ampl_modulation_selected)
        QtCore.QObject.connect(self.uiM.FrequencyModulation_8lvl, QtCore.SIGNAL('clicked(bool)'), self.eightlvl_ch0_freq_modulation_selected)
        QtCore.QObject.connect(self.uiM.autoPhaseReset, QtCore.SIGNAL('clicked(bool)'), self.slot_auto_phase_reset_clicked)

# Set current values of the interface
        try:
            self.slot_board_selected(self.uiM.sernumBox.currentText())
        except:
            print "No DDS board selected"
# Connect signals and slots for profiles
        QtCore.QObject.connect(self.uiM.phase1ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase1ch0_changed)
        QtCore.QObject.connect(self.uiM.phase2ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase2ch0_changed)
        QtCore.QObject.connect(self.uiM.phase3ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase3ch0_changed)
        QtCore.QObject.connect(self.uiM.phase1ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase1ch1_changed)
        QtCore.QObject.connect(self.uiM.phase2ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase2ch1_changed)
        QtCore.QObject.connect(self.uiM.phase3ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_phase3ch1_changed)

        QtCore.QObject.connect(self.uiM.freq1ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq1ch0_changed)
        QtCore.QObject.connect(self.uiM.freq2ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq2ch0_changed)
        QtCore.QObject.connect(self.uiM.freq3ch0, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq3ch0_changed)
        QtCore.QObject.connect(self.uiM.freq1ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq1ch1_changed)
        QtCore.QObject.connect(self.uiM.freq2ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq2ch1_changed)
        QtCore.QObject.connect(self.uiM.freq3ch1, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq3ch1_changed)

        QtCore.QObject.connect(self.uiM.ampl1ch0, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl1ch0_changed)
        QtCore.QObject.connect(self.uiM.ampl2ch0, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl2ch0_changed)
        QtCore.QObject.connect(self.uiM.ampl3ch0, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl3ch0_changed)
        QtCore.QObject.connect(self.uiM.ampl1ch1, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl1ch1_changed)
        QtCore.QObject.connect(self.uiM.ampl2ch1, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl2ch1_changed)
        QtCore.QObject.connect(self.uiM.ampl3ch1, QtCore.SIGNAL('valueChanged(int)'), self.slot_ampl3ch1_changed)

        QtCore.QObject.connect(self.uiM.freq4ch0lvl8, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq4ch0lvl8_changed)
        QtCore.QObject.connect(self.uiM.freq5ch0lvl8, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq5ch0lvl8_changed)
        QtCore.QObject.connect(self.uiM.freq6ch0lvl8, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq6ch0lvl8_changed)
        QtCore.QObject.connect(self.uiM.freq7ch0lvl8, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq7ch0lvl8_changed)



    def slot_freq4ch0lvl8_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x03)

    def slot_freq5ch0lvl8_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x04)

    def slot_freq6ch0lvl8_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x05)

    def slot_freq7ch0lvl8_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x06)

    def slot_phase1ch0_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 0, phase, 0x00)

    def slot_phase2ch0_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 0, phase, 0x01)

    def slot_phase3ch0_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 0, phase, 0x02)
        
    def slot_phase1ch1_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 1, phase, 0x00)

    def slot_phase2ch1_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 1, phase, 0x01)
        
    def slot_phase3ch1_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseWord(board, 1, phase, 0x02)
        
    def slot_freq1ch0_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x00)

    def slot_freq2ch0_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x01)

    def slot_freq3ch0_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 0, freq, 0x02)
        
    def slot_freq1ch1_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 1, freq, 0x00)

    def slot_freq2ch1_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 1, freq, 0x01)
        
    def slot_freq3ch1_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequencyWord(board, 1, freq, 0x02)

    def slot_ampl1ch0_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 0, ampl, 0x00)

    def slot_ampl2ch0_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 0, ampl, 0x01)

    def slot_ampl3ch0_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 0, ampl, 0x02)

    def slot_ampl1ch1_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 1, ampl, 0x00)

    def slot_ampl2ch1_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 1, ampl, 0x01)

    def slot_ampl3ch1_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitudeWord(board, 1, ampl, 0x02)


# Single tone operation
    def single_tone_selected(self):
        board = self.uiM.sernumBox.currentText()
        print "Single tone operation"
        DDSList.SetLevel(board, "default")
        DDSList.SetMode(board, "singletone", 2)

# Phase modulation operation
    def phase_modulation_selected(self):
        board = self.uiM.sernumBox.currentText()
        print "Phase modulation operation"
        DDSList.SetLevel(board, "simple_4lvl")
        DDSList.SetMode(board, "pm", 2)
        DDSList.SetMode(board, "pm", 2)
        settings = DDSList.GetSettings(board)
        self.slot_phase1ch0_changed(settings["phase1ch0"])
        self.slot_phase2ch0_changed(settings["phase2ch0"])
        self.slot_phase3ch0_changed(settings["phase3ch0"])
        self.slot_phase1ch1_changed(settings["phase1ch1"])
        self.slot_phase2ch1_changed(settings["phase2ch1"])
        self.slot_phase3ch1_changed(settings["phase3ch1"])

# Frequency modulation operation
    def freq_modulation_selected(self):
        board = self.uiM.sernumBox.currentText()
        print "Frequency modulation operation"
        DDSList.SetLevel(board, "simple_4lvl")
        DDSList.SetMode(board, "fm", 2)
        settings = DDSList.GetSettings(board)
        self.slot_freq1ch0_changed(settings["freq1ch0"])
        self.slot_freq2ch0_changed(settings["freq2ch0"])
        self.slot_freq3ch0_changed(settings["freq3ch0"])
        self.slot_freq1ch1_changed(settings["freq1ch1"])
        self.slot_freq2ch1_changed(settings["freq2ch1"])
        self.slot_freq3ch1_changed(settings["freq3ch1"])

# Amplitude modulation operation
    def ampl_modulation_selected(self):
        board = self.uiM.sernumBox.currentText()
        print "Amplitude modulation operation"
        DDSList.SetLevel(board, "simple_4lvl")
        DDSList.SetMode(board, "am", 2)
        settings = DDSList.GetSettings(board)
        self.slot_ampl1ch0_changed(settings["ampl1ch0"])
        self.slot_ampl2ch0_changed(settings["ampl2ch0"])
        self.slot_ampl3ch0_changed(settings["ampl3ch0"])
        self.slot_ampl1ch1_changed(settings["ampl1ch1"])
        self.slot_ampl2ch1_changed(settings["ampl2ch1"])
        self.slot_ampl3ch1_changed(settings["ampl3ch1"])

    def eightlvl_ch0_freq_modulation_selected(self):
        board = self.uiM.sernumBox.currentText()
        print "8 level frequency modulation operation: CH0"
        DDSList.SetLevel(board, "simple_8lvlCH0")
        DDSList.SetMode(board, "singletone", 1)
        DDSList.SetMode(board, "fm", 0)
        settings = DDSList.GetSettings(board)
        self.slot_freq4ch0lvl8_changed(settings["freq4ch0"])
        self.slot_freq5ch0lvl8_changed(settings["freq5ch0"])
        self.slot_freq6ch0lvl8_changed(settings["freq6ch0"])
        self.slot_freq7ch0lvl8_changed(settings["freq7ch0"])

# Updates values when user changes the board
    def slot_board_selected(self, sernum):
        self.current_board = sernum
        print sernum + " Selected"
        settings = DDSList.GetSettings(sernum)
        self.uiM.freq0.setValue(settings["freq0"])
        self.uiM.ampl0.setValue(settings["ampl0"])
        self.uiM.phase0.setValue(settings["phase0"])
        self.uiM.freq1.setValue(settings["freq1"])
        self.uiM.ampl1.setValue(settings["ampl1"])
        self.uiM.phase1.setValue(settings["phase1"])
        self.uiM.phase1ch0.setValue(settings["phase1ch0"])
        self.uiM.phase2ch0.setValue(settings["phase2ch0"])
        self.uiM.phase3ch0.setValue(settings["phase3ch0"])
        self.uiM.phase1ch1.setValue(settings["phase1ch1"])
        self.uiM.phase2ch1.setValue(settings["phase2ch1"])
        self.uiM.phase3ch1.setValue(settings["phase3ch1"])
        self.uiM.freq1ch0.setValue(settings["freq1ch0"])
        self.uiM.freq2ch0.setValue(settings["freq2ch0"])
        self.uiM.freq3ch0.setValue(settings["freq3ch0"])
        self.uiM.freq1ch1.setValue(settings["freq1ch1"])
        self.uiM.freq2ch1.setValue(settings["freq2ch1"])
        self.uiM.freq3ch1.setValue(settings["freq3ch1"])
        self.uiM.freq4ch0lvl8.setValue(settings["freq4ch0"])
        self.uiM.freq5ch0lvl8.setValue(settings["freq5ch0"])
        self.uiM.freq6ch0lvl8.setValue(settings["freq6ch0"])
        self.uiM.freq7ch0lvl8.setValue(settings["freq7ch0"])
        self.uiM.ampl1ch0.setValue(settings["ampl1ch0"])
        self.uiM.ampl2ch0.setValue(settings["ampl2ch0"])
        self.uiM.ampl3ch0.setValue(settings["ampl3ch0"])
        self.uiM.ampl1ch1.setValue(settings["ampl1ch1"])
        self.uiM.ampl2ch1.setValue(settings["ampl2ch1"])
        self.uiM.ampl3ch1.setValue(settings["ampl3ch1"])
        self.uiM.description.setText(DDSList.GetDescription(sernum))
        self.RecallMode(settings["mode"], settings["level"])
        self.uiM.autoPhaseReset.setChecked(settings["autoreset"])
        self.slot_auto_phase_reset_clicked(settings["autoreset"]) # Sends command to DDS to choose the reset mode

    def RecallMode(self, mode, level):
        if mode == "singletone" and level == "default":
            self.uiM.SingleTone.click()
        elif mode == "pm" and level == "simple_4lvl":
            self.uiM.PhaseModulation.click()
        elif mode == "fm" and level == "simple_4lvl":
            self.uiM.FrequencyModulation.click()
        elif mode == "fm" and level == "simple_8lvlCH0":
            self.uiM.FrequencyModulation_8lvl.click()
        elif mode == "am" and level == "simple_4lvl":
            self.uiM.AmplitudeModulation.click()

# changed RF0 frequency
    def slot_freq0_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequency(board, 0, freq)

# changed RF0 frequency
    def slot_freq1_changed(self, freq):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetFrequency(board, 1, freq)

# changed RF0 amplitude
    def slot_ampl0_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitude(board, 0, ampl)

# changed RF1 amplitude
    def slot_ampl1_changed(self, ampl):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetAmplitude(board, 1, ampl)

# changed RF0 phase
    def slot_phase0_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhase(board, 0, phase)

# changed RF1 phase
    def slot_phase1_changed(self, phase):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhase(board, 1, phase)

# Changed phase reset checkbox
    def slot_auto_phase_reset_clicked(self, phase_reset):
        board = self.uiM.sernumBox.currentText()
        DDSList.SetPhaseAutoreset(board, phase_reset)

    def slot_reset_clicked(self):
        DDSList.MasterReset()

    def load_settings(self,data):
        all_dds = data['ddslist']      # Keys are serial numbers, which are text strings
        for serial in all_dds.keys():
            this_dds = all_dds[serial]      # Keys are literals, see self.dds_settings
            get_index = self.uiM.sernumBox.findText(serial)
            if get_index >= 0:
                try:
                    self.uiM.sernumBox.setCurrentIndex(get_index)
                    self.uiM.freq0.setValue(this_dds["freq0"])
                    self.uiM.phase0.setValue(this_dds["phase0"])
                    self.uiM.ampl0.setValue(this_dds["ampl0"])
                    self.uiM.freq1.setValue(this_dds["freq1"])
                    self.uiM.phase1.setValue(this_dds["phase1"])
                    self.uiM.ampl1.setValue(this_dds["ampl1"])
                    self.uiM.phase1ch0.setValue(this_dds["phase1ch0"])
                    self.uiM.phase2ch0.setValue(this_dds["phase2ch0"])
                    self.uiM.phase3ch0.setValue(this_dds["phase3ch0"])
                    self.uiM.phase1ch1.setValue(this_dds["phase1ch1"])
                    self.uiM.phase2ch1.setValue(this_dds["phase2ch1"])
                    self.uiM.phase3ch1.setValue(this_dds["phase3ch1"])
                    self.uiM.freq1ch0.setValue(this_dds["freq1ch0"])
                    self.uiM.freq2ch0.setValue(this_dds["freq2ch0"])
                    self.uiM.freq3ch0.setValue(this_dds["freq3ch0"])
                    self.uiM.freq1ch1.setValue(this_dds["freq1ch1"])
                    self.uiM.freq2ch1.setValue(this_dds["freq2ch1"])
                    self.uiM.freq3ch1.setValue(this_dds["freq3ch1"])
                    self.uiM.ampl1ch0.setValue(this_dds["ampl1ch0"])
                    self.uiM.ampl2ch0.setValue(this_dds["ampl2ch0"])
                    self.uiM.ampl3ch0.setValue(this_dds["ampl3ch0"])
                    self.uiM.ampl1ch1.setValue(this_dds["ampl1ch1"])
                    self.uiM.ampl2ch1.setValue(this_dds["ampl2ch1"])
                    self.uiM.ampl3ch1.setValue(this_dds["ampl3ch1"])
                    self.uiM.freq4ch0lvl8.setValue(this_dds["freq4ch0"])
                    self.uiM.freq5ch0lvl8.setValue(this_dds["freq5ch0"])
                    self.uiM.freq6ch0lvl8.setValue(this_dds["freq6ch0"])
                    self.uiM.freq7ch0lvl8.setValue(this_dds["freq7ch0"])
                    self.RecallMode(this_dds["mode"], this_dds["level"])
                    self.uiM.autoPhaseReset.setChecked(this_dds["autoreset"]) # Sets the label properly
                    self.slot_auto_phase_reset_clicked(this_dds["autoreset"]) # Sends command to DDS to choose the reset mode
                except KeyError as e:
                    print "Key error in the settings data: ", e
            else:
                print serial, "is not in the list"
