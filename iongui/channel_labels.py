'''
Created on Aug 1, 2013

@author: lab
'''

import sys
from PyQt4 import QtCore, QtGui
from channel_labels_gui import Ui_ChannelLabelsEditor


class ChannelLabel(object):
    '''
    Stores the labels for channel tool tips
    '''

    def __init__(self):
        '''
        Initialize labels to default values
        '''
        self.label = [
             # Out 1
             "Cooling beam AOM QO0012 RF1(inverse)", 
             "Cooling beam EOM 7.37GHz(inverse)",
             "Far detuned beam (inverse)",
             "384nm optical pumping laser on/off AOM, inverted",
             "Detection beam AOM QO0024 RF1 strong(control logic)",
             "Detection beam AOM QO0012 RF0 weak(control logic)", 
             "Detection beam EOM 2.105GHz(inverse)",
             "110 MHz semi far detuned AOM, inverted",
             # Out 2
             "Channel 1",
             "Sisyphus beams (inverse)",
             "Connected to counter gate",
             "Adiabatic rods Voltage change",
             "935 EOM sideband on/off (inverse)",
             "399 Raman beams power modulation(QO0024 P0)",
             "399 Raman beams power modulation(QO0024 P1)",
             "12.6 Ghz microwave on/off switch, inverted",
             # Out 3
             "Keithley fn gen #1",
             "Keithley fn gen #2",
             "399t Raman beam QO49 P0", 
             "399t Raman beam QO49 P1",
             "399 bar Raman beam AOM on/off (inverse)",
             "TDC trigger",
             "399 Raman beam AOM home made RF switch",
             "399 Raman beam Valadimir's control logic",
             # Out 4
             "399 Raman beam Valadimir's control logic", 
             "399 Raman beam Valadimir's control logic",
             "399t Raman beam QO44, CH0",    
             "399t Raman beam QO44, CH1,combined with former to give QO48 CH0",
             "4-5",
             "399t Raman beam combined with former to give QO48 CH1", 
             "399t Raman beam QO49, P2",
             "399t Raman beam QO49, P3",
             # Counter gate
             "Channel 1",
             "Channel 2",
             "Channel 0", 
             "Channel 1",
             "Channel 2",
             "Channel 7",
             "Channel 8",
             "Channel 9",
             # To be expanded when needed:
             # Out 5
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             # Out 6
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             # Out 7
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             # Out 8
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             "Unused",
             ]
        
    def print_all(self):
        for l in self.label:
            print l
  
  
class ChannelLabelGui(QtGui.QDialog):
    def __init__(self, labels, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_ChannelLabelsEditor()
        self.ui.setupUi(self)
        
        self.labels = labels.label
        self.table  = self.ui.tableWidget
        
        self.bitGroups = ["Out 1", "Out 2", "Out 3", "Out 4", "Counter gate"]
        self.bitGroupsColors =[QtGui.QColor(127,230,230), 
                               QtGui.QColor(230,127,230),
                               QtGui.QColor(230,230,127),
                               QtGui.QColor(240,127,127),
                               QtGui.QColor(127,240,127)]

        
        self.table.setRowCount(len(self.labels))
        
        for i in range(len(self.labels)):
            item1 = QtGui.QTableWidgetItem()
            item1.setBackgroundColor(self.bitGroupsColors[i/8])
            item1.setText(self.labels[i])
            self.ui.tableWidget.setItem(i, 1, item1)
            
            item2 = QtGui.QTableWidgetItem()
            ch_name = self.bitGroups[i/8]
            item2.setBackgroundColor(self.bitGroupsColors[i/8])
            item2.setText(ch_name + ": Ch " +  str( i - 8* (i/8) ))            
            self.ui.tableWidget.setItem(i, 0, item2)
 

  
# Test the GUI
def main():
    app = QtGui.QApplication(sys.argv)
    
    labels = ChannelLabel()
    myapp  = ChannelLabelGui(labels)
    myapp.show()

    sys.exit(app.exec_())

    labels.print_all()


if __name__ == "__main__":
    main()
