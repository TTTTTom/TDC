# -*- coding:utf-8 -*-
"""
Created on Apr 17, 2011

@author: Dima
"""
import sys, math
import traceback

sys.path.insert(0, '..')
sys.path.insert(0, '..\\DDS')

from PyQt4 import QtCore, QtGui
#from guibyte import Ui_Dialog
from guibyte import Ui_TimeSeqWindow
from fpgaseq import FPGA_Seq, SeqLine
from sideband_seq import sideband_ui_dialog
from channel_labels import ChannelLabel
from counters import CounterConfig
from timeseq_tabbar import TabBar, TabBarTest
import pickle
import json



# BITWIDTH  = 28 # Width of a bit button in pixels
BITHEIGHT = 28 # Height of a bit button in pixels
# NBITS     = 40 # Number of bits
NBITS     = 64
BITWIDTH  = 22 # Width of a bit button in pixels
# PIXWIDTH = 200 + BITWIDTH * NBITS # Width of the screen in pixels
PIXWIDTH = 450 + BITWIDTH * NBITS 

# Button group for the scan radio buttons
scangroup = QtGui.QButtonGroup()
scangroup.setExclusive(False)

#class MyButton(QtGui.QToolButton):
class MyButton(QtGui.QPushButton):

    def mouseReleaseEvent(self, e):
        if (e.button() == QtCore.Qt.RightButton):
            self.emit(QtCore.SIGNAL("rightClicked()"))
        if (e.button() == QtCore.Qt.LeftButton):
            self.emit(QtCore.SIGNAL("leftClicked()"))

# Bit for the GUI
class MyBit():
    def __init__(self, widget, layout, x, y):

        self.layout = layout
        self.widget = widget
#        self.button = QtGui.QToolButton(widget)
        self.button = MyButton(widget)
        self.button.setMinimumSize(QtCore.QSize(20, 20))
        self.button.setObjectName("bit")
        layout.addWidget(self.button, y, x, 1, 1)
        
        self.color     = {}
        self.color[-1] = "* { background-color: rgb(255,125,100) }"
        self.color[1]  = "* { background-color: rgb(125,255,100) }"
        self.color[0]  = "* { background-color: rgb(125,110,100) }"
        self.bit       = 0

        self.button.setStyleSheet(self.color[self.bit])                
        QtCore.QObject.connect(self.button, QtCore.SIGNAL('leftClicked()'), self.bit_clicked)

        QtCore.QObject.connect(self.button, QtCore.SIGNAL('rightClicked()'), self.bit_right_clicked)


    def bit_right_clicked(self):
        self.bit = self.bit - 1
        if (self.bit == -2):
            self.bit = 1
        self.display()

    # Slot to click the button 
    def bit_clicked(self):
        self.bit = self.bit + 1
        if (self.bit == 2):
            self.bit = -1
        self.display()
    
    # Set the button value
    def set(self, bit):
        self.bit = bit
        self.display()
        
    # Changes color of the button according to the bit
    def display(self):
        self.button.setStyleSheet(self.color[self.bit])
        
        
    # Enable or disable button 
    def setActive(self, active):
        self.button.setEnabled(active)
    
    # Delete bit button
    def delete(self):
        self.layout.removeWidget(self.button)
        self.button.setParent(None)

    def setToolTip(self, tip):
        self.button.setToolTip(tip)
       
       
# one line of output bit pattern for the GUI 
class Pattern():
    def __init__(self, widget, layout, y, lenght = NBITS):
        self.bits = {}
        self.layout = layout
        self.widget = widget
        self.row    = y
        self.lenght = lenght
        self.labels = ChannelLabel()
        for i in range(lenght):
            self.bits[i] = MyBit(self.widget, self.layout, i + 40, self.row)
            self.bits[i].setToolTip(self.labels.label[i])

    # Activate or reactivate bits buttons
    def setActive(self, active):
        for i in self.bits:
            self.bits[i].setActive(active)
        
    # Deletes row of bits for the user interface and memory
    def delete(self):
        for i in self.bits:
            self.bits[i].delete()
    
    # get the pattn array
    def getPattern(self):
        bitarray = {}
        for i in self.bits:
            bitarray[i] = self.bits[i].bit
        return bitarray

    # set the bit array according to the seqline 
    def setPattern(self, bitarray):
        if ( len(bitarray) != len(self.bits)):
            return
        for i in bitarray:
            self.bits[i].set(bitarray[i])

# Data from chapter
class ChapterData():
    def __init__(self, nrow = 2, active = True, lines = [], name = "Default chapter"):
        self.name   = str(name)
        self.type   = "__chapter__"
        self.nrow   = nrow
        self.active = active
        self.lines  = lines[:]

# Class that draws labels on top of the time sequence pattern
class Labels():    
    def __init__(self, widget, rows = 1):
        self.widget = widget
        self.nrow  = rows

#        self.widget.setGeometry(QtCore.QRect(50, 20, PIXWIDTH, self.nrow * BITWIDTH))
        self.widget.setMinimumSize(QtCore.QSize(PIXWIDTH, self.nrow * BITWIDTH))
        
        self.layout = QtGui.QGridLayout(widget)
        self.layout.setObjectName("gridLayout")
        
        self.buttonLabel = QtGui.QLabel(self.widget)
        self.buttonLabel.setText("Chapter\nname\n")
#        self.buttonLabel.setStyleSheet("* { background-color: rgb(200,127,127) }")
        # self.buttonLabel.setGeometry(QtCore.QRect(0, 0, 44, 20))
        # self.buttonLabel.setMinimumSize(QtCore.QSize(44, 20))   
        self.buttonLabel.setGeometry(QtCore.QRect(0, 0, 74, 50))
        self.buttonLabel.setMinimumSize(QtCore.QSize(74, 50))        
#        self.buttonLabel.setMaximumSize(QtCore.QSize(44, 20))        
        self.layout.addWidget(self.buttonLabel, 1, 0, 1, 1)

        self.plusLabel   = QtGui.QLabel(self.widget)
        self.plusLabel.setText("+/- ")
#        self.plusLabel.setStyleSheet("* { background-color: rgb(127,200,127) }")
        self.plusLabel.setGeometry(QtCore.QRect(0, 0, 20, 18))
        self.plusLabel.setMinimumSize(QtCore.QSize(20, 18))
        self.plusLabel.setMaximumSize(QtCore.QSize(20, 18))
        self.layout.addWidget(self.plusLabel, 1, 1, 1, 1)
        
        self.delayLabel   = QtGui.QLabel(self.widget)     
        self.delayLabel.setText("Delay\n(us)\n")
#        self.delayLabel.setStyleSheet("* { background-color: rgb(127,127,200) }")
        self.delayLabel.setGeometry(QtCore.QRect(0, 0, 60, 50))
        self.delayLabel.setMinimumSize(QtCore.QSize(60, 50))
        self.delayLabel.setMaximumSize(QtCore.QSize(80, 50))
        self.layout.addWidget(self.delayLabel, 1, 2, 1, 2)
        
        self.scanLabel   = QtGui.QLabel(self.widget)     
        self.scanLabel.setText("    Scan")
#        self.scanLabel.setStyleSheet("* { background-color: rgb(230,127,230) }")
        self.scanLabel.setGeometry(QtCore.QRect(0, 0, 42, 22))
        self.scanLabel.setMinimumSize(QtCore.QSize(42, 22))
        self.scanLabel.setMaximumSize(QtCore.QSize(42, 22))
        self.layout.addWidget(self.scanLabel, 1, 3, 1, 1)
 
        self.bitGroups = ["Out 1", "Out 2", "Out 3", "Out 4", "Out 5", "Out 6", "Out 7", "Counter gate"]
        self.bitGroupsColors =["* { background-color: rgb(127,230,230) }", 
                               "* { background-color: rgb(230,127,230) }",
                               "* { background-color: rgb(230,230,127) }",
                               "* { background-color: rgb(240,127,127) }",
                               "* { background-color: rgb(127,230,230) }", 
                               "* { background-color: rgb(230,127,230) }",
                               "* { background-color: rgb(230,230,127) }",
                               "* { background-color: rgb(127,240,127) }"]
 
        self.bitLabel = {}
        self.bitGroupLabel = {}
        self.bitChannelLabel = ChannelLabel()
        for i in range(8):
            self.bitGroupLabel[i]   = QtGui.QLabel(self.widget)             
            self.bitGroupLabel[i].setText(self.bitGroups[i])
            self.bitGroupLabel[i].setStyleSheet(self.bitGroupsColors[i])
            self.bitGroupLabel[i].setGeometry(QtCore.QRect(0, 0, 16, 16))
            self.bitGroupLabel[i].setMinimumSize(QtCore.QSize(16, 16))
#            self.bitGroupLabel[i].setMaximumSize(QtCore.QSize(20, 20))
            self.layout.addWidget(self.bitGroupLabel[i], 0, 4+8*i, 1, 8)                       
            for j in range(8):
                self.bitLabel[8*i+j]   = QtGui.QLabel(self.widget)             
                self.bitLabel[8*i+j].setText(str(j+1))
                self.bitLabel[8*i+j].setStyleSheet(self.bitGroupsColors[i])
                self.bitLabel[8*i+j].setGeometry(QtCore.QRect(0, 0, 20, 20))
                self.bitLabel[8*i+j].setMinimumSize(QtCore.QSize(20, 20))
                self.bitLabel[8*i+j].setMaximumSize(QtCore.QSize(20, 20))
                self.bitLabel[8*i+j].setToolTip(self.bitChannelLabel.label[8*i+j])
                self.layout.addWidget(self.bitLabel[8*i+j], 1, 4+8*i+j, 1, 1)            

        
# Chapter for the time sequence; draws it on the screen and keeps the data
class Chapter():
    def __init__(self, widget, rows, active = True):
        self.green = "* { background-color: rgb(125,255,100) }"
        self.gray  = "* { background-color: rgb(125,110,100) }"
        self.widget = widget

        self.active = active
        if (rows < 2):
            self.nrow = 2
        else:
            self.nrow   = rows

        self.delay = {}
        self.scan  = {}
        self.pattn = {}

        self.widget.setGeometry(QtCore.QRect(50, 20, PIXWIDTH, self.nrow * BITWIDTH))
        self.widget.setMinimumSize(QtCore.QSize(PIXWIDTH, self.nrow * BITWIDTH))
        
        self.layout = QtGui.QGridLayout(widget)
        self.layout.setObjectName("gridLayout")

        self.activeButton = QtGui.QPushButton(self.widget)
        self.activeButton.setMinimumSize(QtCore.QSize(44, 20))
        self.activeButton.setGeometry(QtCore.QRect(0, 0, 44, 20))        
        self.layout.addWidget(self.activeButton, 0, 0, 1, 1)

        self.create_context_menu()

        self.name = QtGui.QLineEdit(self.widget)
        self.name.setMinimumSize(QtCore.QSize(44, 20))
        self.name.setObjectName("Chapter name")
        self.layout.addWidget(self.name, 1, 0, 1, 1)

        self.plusButton = QtGui.QToolButton(self.widget)
        self.plusButton.setText("+")
        self.plusButton.setMinimumSize(QtCore.QSize(18, 18))
        self.layout.addWidget(self.plusButton, 0, 1, 1, 1)

        self.minusButton = QtGui.QToolButton(self.widget)
        self.minusButton.setText("-")
        self.minusButton.setMinimumSize(QtCore.QSize(18, 18))
        self.layout.addWidget(self.minusButton, 1, 1, 1, 1)
       
       
        # add row       
        for i in range(self.nrow):
            self.delay[i] = QtGui.QDoubleSpinBox(self.widget)
            self.delay[i].setMaximum(10000000)
            self.delay[i].setMinimum(0.06)
            self.delay[i].setSingleStep(1.0)
            self.delay[i].setObjectName("delay")
            self.delay[i].setMinimumSize(QtCore.QSize(50, 22))
            self.layout.addWidget(self.delay[i], i, 3, 1, 2)
            
#            self.scan[i] = QtGui.QRadioButton(self.widget)
            self.scan[i] = QtGui.QCheckBox(self.widget)
            self.scan[i].setMinimumSize(QtCore.QSize(22, 22))
            self.layout.addWidget(self.scan[i], i, 5, 1, 1)
            scangroup.addButton(self.scan[i])
            
            self.pattn[i] = Pattern(self.widget, self.layout, i)
            
            

        self.setActive(self.active)       
        self.layout.update()
        
        # Signal / slot connection for buttons
        QtCore.QObject.connect(self.activeButton, QtCore.SIGNAL('clicked()'), self.active_clicked)
        QtCore.QObject.connect(self.plusButton,  QtCore.SIGNAL('clicked()'), self.plus_clicked)
        QtCore.QObject.connect(self.minusButton, QtCore.SIGNAL('clicked()'), self.minus_clicked)
        
    # Gets all the data to save chapter to disk 
    def getData(self):
        chapdata = ChapterData(nrow = self.nrow, active = self.active, name = self.name.text())
        for i in range(self.nrow):
            chapdata.lines.append(SeqLine(self.delay[i].value(), self.scan[i].isChecked(), self.pattn[i].getPattern()))
        return chapdata
    
    # Sets the data 
    def setData(self, chapdata):
    # Add or remove rows in the chapter
        if (chapdata.nrow > self.nrow):
            for i in range(chapdata.nrow - self.nrow):
                self.add_line()
        elif (chapdata.nrow < self.nrow):
            for i in range(self.nrow - chapdata.nrow):
                self.del_line()        
        self.nrow = chapdata.nrow
    # set rows 
        for i in range(self.nrow):
            self.pattn[i].setPattern(chapdata.lines[i].bitarray)
            self.delay[i].setValue(chapdata.lines[i].delay)
            self.scan[i].setChecked(chapdata.lines[i].scanned)
    # Set active data
        self.name.setText(chapdata.name)
        self.setActive(chapdata.active)    
#        print "setData for ", chapdata.name

    # sets the data from json structure that
    def setJSONData(self, chapdata):
        # Add or remove rows in the chapter
        nrow   = chapdata['nrow']
        if (nrow > self.nrow):
            for i in range(nrow - self.nrow):
                self.add_line()
        elif (nrow < self.nrow):
            for i in range(self.nrow - nrow):
                self.del_line()
        self.nrow = nrow

        # set rows
        for i in range(self.nrow):
            line = chapdata['lines'][i]
            self.delay[i].setValue(line['delay'])
            self.scan[i].setChecked(line['scanned'])
            bitarray = line['bitarray']
            bit = {}
            for bitkey, bitval in bitarray.items():
                index = int(bitkey)
                bit[index] = bitval
            self.pattn[i].setPattern(bit)

        # Set active data
        self.name.setText(chapdata['name'])
        self.setActive(chapdata['active'])

    # return chapter name and line number if scan check box is clicked. 
    # return "" and -1 otherwise
    def getScanLine(self):
        for i in range(self.nrow):
            if (self.scan[i].isChecked()):
                return self.name.text(), i
        return "", -1
        
            
    # returns the array of seqline objects that correspond to the chapter
    def appendData(self, seq):
        if (self.active == False):
            return seq 

        for i in range(self.nrow):
            seq.append(SeqLine(self.delay[i].value(), self.scan[i].isChecked(), self.pattn[i].getPattern()))
        return seq
    
    # Adds one line to the chapter
    def add_line(self):        
        self.widget.setGeometry(QtCore.QRect(50, 20, PIXWIDTH, (self.nrow + 1)* BITWIDTH))
        self.widget.setMinimumSize(QtCore.QSize(PIXWIDTH, (self.nrow + 1) * BITWIDTH))
        self.delay[self.nrow] = QtGui.QDoubleSpinBox(self.widget)
        self.delay[self.nrow].setMaximum(10000000)
        self.delay[self.nrow].setMinimum(0.06)
        self.delay[self.nrow].setSingleStep(1.0)
        self.delay[self.nrow].setObjectName("delay")
        self.delay[self.nrow].setMinimumSize(QtCore.QSize(50, 22))
        self.layout.addWidget(self.delay[self.nrow], self.nrow, 3, 1, 2)
        
#        self.scan[self.nrow] = QtGui.QRadioButton(self.widget)
        self.scan[self.nrow] = QtGui.QCheckBox(self.widget)
        self.scan[self.nrow].setMinimumSize(QtCore.QSize(22, 22))
        self.layout.addWidget(self.scan[self.nrow], self.nrow, 5, 1, 1)
        scangroup.addButton(self.scan[self.nrow])

        self.pattn[self.nrow] = Pattern(self.widget, self.layout, self.nrow)
        self.nrow += 1
        # emit a signal if chapter size changed
        self.widget.emit(QtCore.SIGNAL('resizeChapter()'))

    # removes one line from the chapter
    def del_line(self):
        if (self.nrow <= 2):
            return
        self.del_line_anyway()

    # removes one line without checking how many lines left
    def del_line_anyway(self):
        self.nrow -= 1
        # remove delay indicator
        self.layout.removeWidget(self.delay[self.nrow])
        self.delay[self.nrow].setParent(None)
        self.layout.removeWidget(self.scan[self.nrow])
        scangroup.removeButton(self.scan[self.nrow])
        self.scan[self.nrow].setParent(None)
        # remove line of buttons
        self.pattn[self.nrow].delete()
        self.widget.setGeometry(QtCore.QRect(50, 20, PIXWIDTH, (self.nrow)* BITWIDTH))
        self.widget.setMinimumSize(QtCore.QSize(PIXWIDTH, (self.nrow) * BITWIDTH))
        # emit a signal if chapter size changed
        self.widget.emit(QtCore.SIGNAL('resizeChapter()'))
    
    # slot for active clicked signal    
    def active_clicked(self):
        if self.active :
            self.setActive(False)
        else:
            self.setActive(True)

    # slot for plus button signal. Adds another line     
    def plus_clicked(self):
        self.add_line()
    
    # slot for minus button signal. Removes last line         
    def minus_clicked(self):
        self.del_line()
                          
    # set the active state for the chapter
    def setActive(self, active):
        self.active = active
        # change color of the button
        if(self.active):
            self.activeButton.setStyleSheet(self.green)
        else:
            self.activeButton.setStyleSheet(self.gray)
        # make everything else disabled
        for i in self.pattn:
            self.pattn[i].setActive(self.active)
        for i in self.delay:
            self.delay[i].setEnabled(self.active)
        for i in self.scan:
            self.scan[i].setEnabled(self.active)
                    
        self.plusButton.setEnabled(self.active)
        self.minusButton.setEnabled(self.active)
        self.name.setEnabled(self.active)

    # create context menu
    def create_context_menu(self):
        self.popMenu = QtGui.QMenu(self.widget)
        self.add_normal_item = QtGui.QAction('Add normal chapter', self.widget)
        self.popMenu.addAction(self.add_normal_item)
        self.add_sideband_item = QtGui.QAction('Add sideband chapter', self.widget)
        self.popMenu.addAction(self.add_sideband_item)
        self.popMenu.addSeparator()
        self.remove_item    = QtGui.QAction('Remove chapter', self.widget)
        self.popMenu.addAction(self.remove_item)

        self.activeButton.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.activeButton, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
        QtCore.QObject.connect(self.add_normal_item, QtCore.SIGNAL('triggered()'), self.add_normal_chapter_slot)
        QtCore.QObject.connect(self.add_sideband_item, QtCore.SIGNAL('triggered()'), self.add_sideband_chapter_slot)
        QtCore.QObject.connect(self.remove_item,    QtCore.SIGNAL('triggered()'), self.remove_chapter_slot)

    # execute actions based on the menu choice
    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.activeButton.mapToGlobal(point))

    # runs when context menu item is triggered
    def add_normal_chapter_slot(self):
        self.widget.emit(QtCore.SIGNAL('addChapter'), self, CHAP.NORMAL)

    # runs when context menu item is triggered
    def add_sideband_chapter_slot(self):
        self.widget.emit(QtCore.SIGNAL('addChapter'), self, CHAP.SIDEBAND)

    # runs when context menu item is triggered
    def remove_chapter_slot(self):
        self.widget.emit(QtCore.SIGNAL('removeChapter'), self)

    def who(self):
        print "I am a NORMAL chapter"
        
# Enum for different types of sequence
class CHAP:
    NORMAL, SIDEBAND = range(2)
    
# pumping_time and raman_pi_time are here for the compartability reasons
class SidebandChapterData(ChapterData):
    def __init__(self, nrow = 2, active = True, lines = [], name = "Sideband cooling"):
        self.name   = "Sideband cooling"
        self.type   = "__sideband_chapter__"
        self.nrow   = nrow
        self.active = active
        self.lines  = lines[:]

#        self.pumping_time  = 1  # default optical puming time (microseconds)
#        self.raman_pi_time = 1  # raman pi time for the sideband transition (\eta \Omega)
        self.n_phonons     = 10 # initial number of phonons
        self.n_cycles      = 40 # initial number of the optical pumping cycles
        self.n_lines       = 2  # Number of lines per sideband cooling step
                   
    # Saves the sideband cooling configuration     
    def setConfig(self, n_phonons, n_cycles, n_lines):
#        self.pumping_time  = pumping_time  # default optical puming time (microseconds)
#        self.raman_pi_time = raman_pi_time  # raman pi time for the sideband transition (\eta \Omega)
        self.n_phonons     = n_phonons # initial number of phonons
        self.n_cycles      = n_cycles # initial number of the optical pumping cycles
        self.n_lines       = n_lines

    # Returns the sadeband cooling parameters
    def getConfig(self):
        return  self.n_phonons, self.n_cycles, self.n_lines
        


# Class inherited from the main chapter class 
class SidebandChapter(Chapter):
    def __init__(self, widget):
        Chapter.__init__(self, widget, 2)

        self.nlines = 2
        
        self.name.setText("Sideband cooling")
        self.name.setStyleSheet('color: red; background-color: yellow')
        self.name.setToolTip("This is a special chapter for the sideband cooling sequence")
        
        self.setup_line(0)
        self.setup_line(1)
       
        self.plusButton.setEnabled(True)
        self.minusButton.setEnabled(True)
        self.plusButton.setToolTip("Configure the sideband cooling")
        self.minusButton.setToolTip("Configure the sideband cooling")
        self.plusButton.setStyleSheet('background-color: yellow')        
        self.minusButton.setStyleSheet('background-color: yellow')
        self.plusButton.setText("Cfg")
        self.minusButton.setText("Cfg")
        
        self.cfg = sideband_ui_dialog()

                
        QtCore.QObject.disconnect(self.plusButton,  QtCore.SIGNAL('clicked()'), self.plus_clicked)
        QtCore.QObject.disconnect(self.minusButton, QtCore.SIGNAL('clicked()'), self.minus_clicked)
        QtCore.QObject.connect(self.plusButton,  QtCore.SIGNAL('clicked()'), self.config_clicked)
        QtCore.QObject.connect(self.minusButton, QtCore.SIGNAL('clicked()'), self.config_clicked)

        QtCore.QObject.connect(self.cfg.ui.plusButton  , QtCore.SIGNAL('clicked()'), self.add_step) 
        QtCore.QObject.connect(self.cfg.ui.minusButton , QtCore.SIGNAL('clicked()'), self.del_step) 
        QtCore.QObject.connect(self.cfg.ui.nlines ,      QtCore.SIGNAL('valueChanged(int)'), self.change_nlines) 
        
    # returns the array of seqline objects that correspond to the chapter
    # HAS TO CHANGE IT for the sideband cooling !!! 
    def appendData(self, seq):
        if (self.active == False):
            return seq 

        for i in range(self.cfg.n_cycles):
            for l in range(self.nrow / self.nlines):
#            raman_time = self.cfg.raman_pi_time / math.sqrt(1.0 + self.cfg.n_phonons * (1.0 - float(i+1.0) / float(self.cfg.n_cycles) ))
                raman_time = self.delay[self.nlines * (l + 1) - 1].value() / math.sqrt(1.0 + self.cfg.n_phonons * (1.0 - float(i+1.0) / float(self.cfg.n_cycles) ))
                for n in range (self.nlines - 1):
                    seq.append(SeqLine(self.delay[self.nlines * l + n].value(), self.scan[self.nlines * l + n].isChecked(), self.pattn[self.nlines * l + n].getPattern()))
#                    print self.delay[self.nlines * l + n].value()
                seq.append(SeqLine(raman_time, self.scan[self.nlines * (l + 1) - 1].isChecked(), self.pattn[self.nlines * (l + 1) - 1].getPattern()))
#                print "Raman time is ", raman_time
        return seq


    # Gets all the data to save chapter to disk 
    def getData(self):
        chapdata = SidebandChapterData(nrow = self.nrow, active = self.active, name = self.name.text())
        chapdata.setConfig(self.cfg.n_phonons, self.cfg.n_cycles, self.cfg.n_lines)
        
        for i in range(self.nrow):
            chapdata.lines.append(SeqLine(self.delay[i].value(), self.scan[i].isChecked(), self.pattn[i].getPattern()))
        return chapdata
#        print "getData SidebandSequence"
    
    # Sets the data 
    def setData(self, chapdata):
    # Add or remove rows in the chapter 
    # number of rows in the sideband chapter should be divisible by nlines    
 
     # Set sideband cooling specific data
        [ self.cfg.n_phonons, self.cfg.n_cycles, self.cfg.n_lines ] =  chapdata.getConfig()
        
        self.nlines = self.cfg.n_lines
        nrow = ( chapdata.nrow / self.nlines ) * self.nlines 
        
        if (nrow > self.nrow):
            for i in range(nrow - self.nrow):
                self.add_line()
        elif (nrow < self.nrow):
            for i in range(self.nrow - nrow):
                self.del_line()        
        self.nrow   = nrow

    # set rows 
        for i in range(self.nrow):
            self.pattn[i].setPattern(chapdata.lines[i].bitarray)
            self.delay[i].setValue(chapdata.lines[i].delay)
            self.scan[i].setChecked(False)
            self.setup_line(i)
    # Set active data
        self.name.setText("Sideband cooling")
        self.setActive(chapdata.active)

#        print "setData SidebandSequence"

        # sets the data from json structure that
    def setJSONData(self, chapdata):
        # Add or remove rows in the chapter
        self.cfg.n_phonons = chapdata['n_phonons']
        self.cfg.n_cycles  = chapdata['n_cycles']
        self.cfg.n_lines   = chapdata['n_lines']

        self.nlines = self.cfg.n_lines
        nrow = ( chapdata['nrow'] / self.nlines ) * self.nlines

        if (nrow > self.nrow):
            for i in range(nrow - self.nrow):
                self.add_line()
        elif (nrow < self.nrow):
            for i in range(self.nrow - nrow):
                self.del_line()
        self.nrow = nrow

        # set rows
        for i in range(self.nrow):
            line = chapdata['lines'][i]
            self.delay[i].setValue(line['delay'])
            self.scan[i].setChecked(False)
            bitarray = line['bitarray']
            bit = {}
            for bitkey, bitval in bitarray.items():
                index = int(bitkey)
                bit[index] = bitval
            self.pattn[i].setPattern(bit)
            self.setup_line(i)

        # Set active data
        self.name.setText("Sideband cooling")
        self.setActive(chapdata['active'])


 
    # Override set active method of the parent class to disable +/- button
    def setActive(self, active):
        Chapter.setActive(self, active)
        self.plusButton.setEnabled(True)
        self.minusButton.setEnabled(True)
        for i in self.delay:
            self.delay[i].setEnabled(True)
            self.scan[i].setEnabled(False)

    # Click the config button
    def config_clicked(self):
        self.cfg.show()
        
    # print who i am on the console, for debugging
    def who(self):
        print "I am a SIDEBAND chapter"
    
    # Proper colors for the sideband chapter lines
    def add_line(self):
#        super(SidebandChapter(), self).add_line()
        Chapter.add_line(self)
        self.setup_line(self.nrow - 1)
        
    # Adjust colors, tooltips and control elements
    def setup_line(self, index):
        self.scan[index].setEnabled(False)
        if ( (index % self.nlines) == self.nlines - 1):
            self.delay[index].setToolTip("Raman pi time, the longest Raman pulse duration, actual delay is calculated for every cycle")
            self.delay[index].setEnabled(True)
            self.delay[index].setStyleSheet('background-color: pink')
        else:
            self.delay[index].setToolTip("Optical pumping")
            self.delay[index].setEnabled(True)
            self.delay[index].setStyleSheet('background-color: lightskyblue') 

    
    # Sideband chapter lines should appear in pairs, we add 2 line for each step
    def add_step(self):
        for i in range(self.nlines):
            self.add_line()        
        
    # Sideband chapter lines should appear in pairs, we remove 2 line for each step
    def del_step(self):
        for i in range(self.nlines):
            self.del_line()

    def change_nlines(self, nlines):
        if (nlines < self.nlines):
            self.del_lines_per_step(self.nlines - nlines)
        elif(nlines > self.nlines):
            self.add_lines_per_step(nlines - self.nlines)
        

    def add_lines_per_step(self, delta):
        print "add " + str(delta * self.nrow / self.nlines) + " lines"
        for i in range(delta * self.nrow / self.nlines):
            self.add_line()
            
        self.nlines += delta
        for i in range(self.nrow):
            self.setup_line(i)
        
        
    def del_lines_per_step(self, delta):
        print "delete " + str(delta) + " lines"
        for i in range(delta * self.nrow / self.nlines):
            self.del_line()
            
        self.nlines -= delta

        for i in range(self.nrow):
            self.setup_line(i)


# generate sequence that consist of several chapters     
class Sequence():
    def __init__(self, widget, chapter_list, tab="Default"):
        self.tab     = tab
        self.widget  = widget
        self.vlayout = QtGui.QVBoxLayout(self.widget)
        self.vlayout.setObjectName("verticalLayout")

        self.chapter = [] # was {}
        self.wchap   = [] # was {}

        # Draw labels on the top
        self.wlabels  = QtGui.QWidget(self.widget)
        self.vlayout.addWidget(self.wlabels)
        self.labels   = Labels(self.wlabels)
        
        nChapters = len(chapter_list)
                
        # Draw chapters
        for i in range(nChapters):
            self.add_chapter(i, chapter_list[i])

        # for i in range(nChapters):
        #     self.chapter[i].who()


    def set_tab_name(self, tab):
        self.tab=tab

    # resize time sequence widget
    def resize(self):
        nrow = 0
        for chap in self.chapter:
            nrow += chap.nrow
        nrow += 2 # space for labels
        self.widget.setMinimumSize(QtCore.QSize(PIXWIDTH, nrow * 32))
        self.widget.setMaximumSize(QtCore.QSize(PIXWIDTH, nrow * 32))

    # get a chapter data
    def get(self):
        data = []
        for chap in self.chapter:
            data = chap.appendData(data)
        return data
    
    # Returns name of the selected chapter and line number for scanning
    def getScanLine(self):
        for chap in self.chapter:
            name, line = chap.getScanLine()
            if (line >= 0):
                return name, line
        return "", -1
    

    # retieves all the data to save it in the file
    def getData(self):
        data = []
        for chap in self.chapter:
            data.append(chap.getData())
        return data
    
    # save sequence data to a file
    def save(self, file):
        pickle.dump(self.getData(), file)


    # save sequence data in JSON format. More readable for humans than pickle
    def json_dump_slot(self, filename):
        with open(filename, mode='w') as f:
            data = self.getData()
            json.dump(data, f, sort_keys = False, indent = 4, skipkeys=True, default=jdefault)

    # remove all current chapters
    def remove_all_chapters(self):
        while self.chapter:
            self.remove_chapter(self.chapter[0])

    # loads sequence data from a file and updates GUI
    def load(self, file):
        data = pickle.load(file)
        self.load_data(data)

    # load the data from the data structure
    def load_data(self, data):
        self.remove_all_chapters()

        # add chapters
        for idx, d in enumerate(data):
            if d.name == "Sideband cooling":
                self.add_chapter(idx, CHAP.SIDEBAND)
            else:
                self.add_chapter(idx, CHAP.NORMAL)
            self.chapter[idx].setData(d)

        self.resize()


    # Load JSON data structure
    def load_json_data(self, json_data):
        self.remove_all_chapters()
        for idx, d in enumerate(json_data):
            if d['name'] == "Sideband cooling":
                self.add_chapter(idx, CHAP.SIDEBAND)
            else:
                self.add_chapter(idx, CHAP.NORMAL)
            self.chapter[idx].setJSONData(d)

        self.resize()


    # load time sequence data from a json file
    def load_json(self, file):
        json_data = json.load(file)
        self.load_json_data()


    # adds chapter to the sequence
    def add_chapter(self, index, chapter_type):
        self.wchap.insert(index, QtGui.QWidget(self.widget))
        self.vlayout.insertWidget(index + 1, self.wchap[index])
#        self.vlayout.addWidget(self.wchap[index])

        if (chapter_type   == CHAP.NORMAL):
            self.chapter.insert(index, Chapter(self.wchap[index], 2))
        elif (chapter_type == CHAP.SIDEBAND):
            self.chapter.insert(index, SidebandChapter(self.wchap[index]))

        QtCore.QObject.connect(self.wchap[index], QtCore.SIGNAL('resizeChapter()'), \
                               self.resize)

        QtCore.QObject.connect(self.wchap[index], QtCore.SIGNAL('removeChapter'), \
                               self.remove_chapter)

        QtCore.QObject.connect(self.wchap[index], QtCore.SIGNAL('addChapter'), \
                               self.add_chapter_slot)

    # process chapter slot and
    def add_chapter_slot(self, chapter, chapter_type):
        index = self.chapter.index(chapter)
        self.add_chapter(index, chapter_type)
        self.resize()
#        print "add chapter slot"
#        print index, chapter, self.chapter

    # removes chapter from the sequence
    def remove_chapter(self, chapter):
        index = self.chapter.index(chapter)
        self.chapter.pop(index)
        self.wchap.pop(index)
        b = self.vlayout.takeAt(index+1)
        b.widget().deleteLater()
        self.resize()
#        print "remove chapter"
#        print index, chapter, self.chapter

# Function to enable JSON dump
def jdefault(obj):
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, QtCore.QString):
        return str(obj)
    return vars(obj)


class SequenceTab():
    def __init__(self, tabWidget, active = False, tab = None, name = "Default", \
                 chapters =  [CHAP.NORMAL, CHAP.NORMAL] ):
        self.name      = name
        self.tabWidget = tabWidget

        print self.name

        if (tab == None):
            self.tab = QtGui.QWidget()
            self.tabWidget.addTab(self.tab, name)
            idx =  self.tabWidget.indexOf(self.tab)
            self.tabWidget.setTabText(idx, name)
            self.tab.setObjectName("tab"+name)
        else:
            self.tab = tab
            idx = self.tabWidget.indexOf(self.tab)
            self.tabWidget.setTabText(idx, name)

        self.scrollArea = QtGui.QScrollArea(self.tab)
        self.scrollArea.setGeometry(QtCore.QRect(0, 0, 1341, 751))
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setMaximumSize(QtCore.QSize(1380, 751))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.widget = QtGui.QWidget(self.scrollArea)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1322, 749))
        self.widget.setObjectName("widget")
        self.scrollArea.setWidget(self.widget)

        self.sequence = Sequence(self.widget, chapters)
        self.sequence.resize()
        self.sequence.set_tab_name(self.name)

        self.activate(active)

    def sequence(self):
        return self.sequence

    def relabel(self, name):
        idx = self.tabWidget.indexOf(self.tab)
        self.tabWidget.tabBar().setLabel(name, idx)

    def activate(self, active):
        self.active = active
        idx = self.tabWidget.indexOf(self.tab)
        self.tabWidget.tabBar().setActive(active, idx)

    def isactive(self):
        return self.active

# Data from chapter
class TabData():
    def __init__(self, sequence, name="Default", active=True ):
        self.type     = "__tabdata__"
        self.name     = str(name)
        self.active   = active
        self.sequence = sequence

# Main widget
#class MyTest(QtGui.QDialog):
class TimeSeqWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TimeSeqWindow()
        self.ui.setupUi(self)

        self.ui.tabWidget.removeTab(0)
        self.ui.tabWidget.setTabBar(TabBar( self.ui.tabWidget))
        # Set custom tab bar
        # Add a default tab
        self.sequence_tab = []

        # Load default time sequence
        self.load_file()

        # If nothing is loaded, add a default tab
        if len(self.sequence_tab) == 0:
            self.sequence_tab.append( SequenceTab(self.ui.tabWidget, # tab=self.ui.tab,
                                                  name="Default", chapters = [CHAP.NORMAL, CHAP.SIDEBAND]) )

        self.fpga     = FPGA_Seq()

        self.setUSBStatus(self.fpga.usbstatus)
        
        QtCore.QObject.connect(self.ui.runButton, QtCore.SIGNAL('clicked()'), 
                               self.run_slot)
        QtCore.QObject.connect(self.ui.saveButton, QtCore.SIGNAL('clicked()'), 
                               self.save_slot)
        QtCore.QObject.connect(self.ui.savetabButton, QtCore.SIGNAL('clicked()'),
                               self.save_tab_slot)
        QtCore.QObject.connect(self.ui.loadButton, QtCore.SIGNAL('clicked()'), 
                               self.load_slot)
        QtCore.QObject.connect(self.ui.configButton, QtCore.SIGNAL('clicked()'), 
                               self.config_slot)
        QtCore.QObject.connect(self.ui.add_tab_button, QtCore.SIGNAL('clicked()'),
                               self.add_tab_slot)
        QtCore.QObject.connect(self.ui.remove_tab_button, QtCore.SIGNAL('clicked()'),
                               self.remove_tab_slot)
#        QtCore.QObject.connect(self.fpga.usb.read_thread, QtCore.SIGNAL('data_ready(QByteArray)'), self.data_ready_slot)
        QtCore.QObject.connect(self, QtCore.SIGNAL("lastWindowClosed()"), self.stop_slot)
        
        QtCore.QObject.connect(scangroup, QtCore.SIGNAL("buttonClicked(int)"), self.scan_clicked_slot)

        QtCore.QObject.connect(self.ui.tabWidget.tabBar(), QtCore.SIGNAL('enableTab'), self.enable_tab_slot)

        QtCore.QObject.connect(self.ui.tabWidget.tabBar(), QtCore.SIGNAL('renameTab'), self.rename_tab_slot)

        QtCore.QObject.connect(self.fpga, QtCore.SIGNAL("usbstatus(int)"), self.setUSBStatus)

#        print "Time sequence after init is", self.sequence_get()

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


    # returns the time sequence for the fpga
    def sequence_get(self):
        s= []
        for tab in self.sequence_tab:
            if tab.isactive():
#                s.append(tab.sequence.get())
                s.extend(tab.sequence.get())
        return s

    # returns all the data that describe all the time sequences
    def sequence_getData(self):
        d = []
        for tab in self.sequence_tab:
            d.append(TabData(tab.sequence.getData(), name=tab.name, active=tab.isactive() ))
        return d

    # Finds a scan line in the sequences
    def sequence_getScanLine(self):
        for tab in self.sequence_tab:
            name, line = tab.sequence.getScanLine()
            if line != -1:
                return name, line
        return name, line

    # saves all the tabs in the JSON file
    def sequence_json_dump_slot(self, filename):
        with open(filename, mode='w') as f:
            data = self.sequence_getData()
            json.dump(data, f, sort_keys = False, indent = 4, skipkeys=True, default=jdefault)

    # load pickle file
    def sequence_load(self, file):
        data = pickle.load(file)
        for idx, d in enumerate(data):
            if hasattr(d, type) == False: # Old format, no type data present
                idx = self.ui.tabWidget.currentIndex()
                self.sequence_tab[idx].sequence.load_data(data)
                return
            if d.type == "__chapter__": # Only one tab is saved
                idx = self.ui.tabWidget.currentIndex()
                self.sequence_tab[idx].sequence.load_data(data)
                return
            if d.type == "__tabdata__": # The whole sequence including all the tabs is saved
                st = SequenceTab(self.ui.tabWidget, name=d.name)
                self.sequence_tab.append(st)
                st.activate(d.active)
                st.sequence.load_data(d.sequence)

    # load json file
    def sequence_load_json(self, file):
        json_data = json.load(file)
        for idx, d in enumerate(json_data):
            if 'type' not in d: # Old format, no type data present
                idx = self.ui.tabWidget.currentIndex()
                self.sequence_tab[idx].sequence.load_json_data(json_data)
                return
            if d['type'] == "__chapter__": # Only one tab is saved
                idx = self.ui.tabWidget.currentIndex()
                self.sequence_tab[idx].sequence.load_json_data(json_data)
                return
            if d['type'] == "__tabdata__": # The whole sequence including all the tabs is saved
                st = SequenceTab(self.ui.tabWidget, name=d['name'])
                self.sequence_tab.append(st)
                st.activate(d['active'])
                st.sequence.load_json_data(d['sequence'])

    # Slot to process tab enable events
    def enable_tab_slot(self, idx, enable):
        print idx, enable
        self.sequence_tab[idx].activate(enable)

    # print the time sequence 
    def write(self):
        s = self.sequence_get()
        for i in s:
            i.write()

    # uploads new time sequence to an fpga
    def config_slot(self):
#        self.write()
        self.fpga.setSeq(self.sequence_get())
#        print "configured", self.sequence_get()
        self.save_tofile() # Saves to the default time sequence

  
    #  runs a loaded time sequence 
    def run_slot(self, reload = True):
        if (reload):
            self.fpga.setSeq(self.sequence_get())
            self.save_tofile() # Saves to the default time sequence
        self.fpga.run()
        
    def scan_clicked_slot(self, button):
        name, line = self.sequence_getScanLine()
        self.emit(QtCore.SIGNAL("scanLineChanged"), name, line) 
        # print "Button ", name, " Line ", line ," clicked"
    
    # Save time sequence to file
    def save_slot(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        if ( filename == "" ):
            return
        self.save_tofile(filename)       
#        file = open(filename, "wb")
#        pickle.dump(self.sequence.getData(), file)
#        file.close()

    def save_tab_slot(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        if ( filename == "" ):
            return
        try:
            idx = self.ui.tabWidget.currentIndex()
            self.sequence_tab[idx].sequence.json_dump_slot(filename)
        except:
            print "Can't save timesequence tab to " + filename
            traceback.print_exc()

    # saves data to the default file, will read this file upon the startup
    # Now pickle format is the default
    def save_tofile(self, filename = "default_timeseq.dat"):
        try:
            self.sequence_json_dump_slot(filename)
        except:
            print "Can't save time sequence to the default file " + filename
            traceback.print_exc()                        
               
    # loads timesequence from file
    def load_slot(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '~')
        self.load_file(filename)

        
    # loads timesequence data from file
    def load_file(self, filename = "default_timeseq.dat"):
        # json format
        try:
            file = open(filename, "rb")
            self.sequence_load_json(file)
            file.close()
            loaded = True
        except:
            print "Can't load the timesequence file in json format, trying pickle next" + filename
            traceback.print_exc()
            loaded = False

        if loaded:
            return

        # Pickle format
        try:
            file = open(filename, "rb")
            self.sequence_load(file)
            file.close()
            loaded = True
        except:
            print "Can't load the timesequence file in pickle format  " + filename
            traceback.print_exc()
            loaded = False


    # closes USB connection
    def stop_slot(self):
        self.fpga.usb.close()
        
    def nrep_changed_slot(self, value):
        self.fpga.setNrep(value)

    def mask_changed_slot(self, mask):
        print "Mask changed slot got ", mask
        self.fpga.setCntrMask(mask)

    # change delay, reconfigure fpga and run a time sequence 
    def scan_delay_slot(self, delay):

        # Change delay and reload time sequence
        seq = self.sequence_get()
        for i in seq:
            if i.scanned:
                i.delay = delay
        self.fpga.setSeq(seq, changes_only=True)
        
        # run the time sequence
        self.fpga.run()

        
# Appends data to display buffer when they are ready
#    def data_ready_slot(self, data):
        # print data
#        self.ui.rcvText.append(str(data))
                
    # updates USB status string
    def setUSBStatus(self, status):
        if (status == 0):
            self.ui.labelUSB.setText("FPGA is connected")
        if (status == -1) :
            self.ui.labelUSB.setText("Can't connect to FPGA")
            self.ui.labelUSB.setStyleSheet("QLabel { background-color : red; color : blue; }")

    # Adds tab in the time sequence window
    def add_tab_slot(self):
        # add the tab
        nm = "Extra" + str(len(self.sequence_tab))
        st = SequenceTab(self.ui.tabWidget, name=nm)
        self.sequence_tab.append(st)
        # Copy the data from the existing one
        idx = self.ui.tabWidget.currentIndex()
        dat = self.sequence_tab[idx].sequence.getData()
        st.sequence.load_data(dat)

    # Removes tab
    def remove_tab_slot(self):
        if len(self.sequence_tab) < 2:
            return
        idx = self.ui.tabWidget.currentIndex()
        self.ui.tabWidget.removeTab(idx)
        self.sequence_tab.pop(idx)

#2.7    def rename_tab_slot(self, idx, name):
    def rename_tab_slot(self, name, idx):
        self.sequence_tab[idx].name = name
        self.sequence_tab[idx].sequence.set_tab_name(name)
        print idx, self.sequence_tab[idx].name
        self.sequence_tab[idx].relabel(name)


# main function to test GUI
def main():
    app = QtGui.QApplication(sys.argv)
#   myapp = MyByte()
#   myapp.show()
    myapp = TimeSeqWindow()
    myapp.show()
    myapp.fpga.setNrep(10) # We do only one pulse if the program is run directly
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
