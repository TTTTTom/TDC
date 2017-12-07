# program controls EOM frequency for locking to iodine cell
import urllib2
import re
from PyQt4 import QtCore, QtGui
from iodineeomgui import Ui_IodineCellEOM
import sys
import time

# Main widget
class IodineEOM(QtGui.QDialog):
    def __init__(self, parent=None):
        print "GUI is called"
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_IodineCellEOM()
        self.ui.setupUi(self)

        # initialization steps to get LCD number to read
        #self.increase_1MHz()
        #self.decrease_1MHz()
        try:
            urllib2.urlopen('http://192.168.222.2/cgi-bin/pllcom?freqinc=0', timeout = 1)
        except:
            print "Can't connect to the EOM generator"

        #QtCore.QObject.connect(self.ui.lcdNumber, QtCore.SIGNAL('data_ready(QByteArray)'), self.read_freq)
        QtCore.QObject.connect(self.ui.pushButton_4, QtCore.SIGNAL('clicked()'), self.increase_1MHz)
        QtCore.QObject.connect(self.ui.pushButton_3, QtCore.SIGNAL('clicked()'), self.decrease_1MHz)
        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL('clicked()'), self.goto_freq10272MHz)
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL('clicked()'), self.goto_freq10262MHz)
        QtCore.QObject.connect(self.ui.pushButton_5, QtCore.SIGNAL('clicked()'), self.manual_entry)
        #QtCore.QObject.connect(self.ui.manual_entry, QtCore.SIGNAL('valueChanged()'), self.manual_entry_slot)
        #self.manual_entry = self.ui.manual_entry
        #self.manual_entry.valueChanged.connect(self.manual_entry_slot)

    def initialize(self):
        read_data = urllib2.urlopen('http://192.168.222.2/cgi-bin/pllcom?freqinc=0', timeout = 1)
        start_data = read_data.read(50)
        self.display_freq(start_data)

    # increase frequency by 1 MHz
    def increase_1MHz(self):
        print "increase_1MHz button clicked"
        try:
            data = urllib2.urlopen('http://192.168.222.2/cgi-bin/pllcom?freqinc=1', timeout = 1)
        except:
            print "Can't connect to the EOM generator"
            return

        time.sleep(0.5)
        dataread = data.read(50)
        self.display_freq(dataread)
        self.check_pll(dataread)

    # decrease frequency by 1 MHz
    def decrease_1MHz(self):
        print "decrease_1MHz button clicked"
        try:
            data = urllib2.urlopen('http://192.168.222.2/cgi-bin/pllcom?freqinc=-1', timeout = 1)
        except:
            print "Can't connect to the EOM generator"
            return

        time.sleep(0.5)
        dataread = data.read(50)
        self.display_freq(dataread)
        self.check_pll(dataread)

    # display frequency on LCD screen
    def display_freq(self,data):
        datarec = re.search('(?<=YIG_frq=)\w+',data)
        datastr = int(datarec.group(0))/1000
        print datastr
        self.ui.lcdNumber.display(datastr)
        #self.ui.lcdNumber.value()

    # check if PLL is locked
    def check_pll(self,data):
        pllboo = re.search('(?<=PLL_lock=)\w+',data)
        self.ui.checkBox.setEnabled(0)
        if int(pllboo.group(0)) == 1:
            self.ui.checkBox.setChecked(1)
        else:
            self.ui.checkBox.setChecked(0)


    # go to 10242 MHz
    def goto_freq10272MHz(self):
        print "go to freq 10272 MHz"
        diff1 = 10272-self.ui.lcdNumber.intValue()
        if abs(diff1) < 100:
            if diff1 > 0:
                for i in range(diff1) :
                    self.increase_1MHz()
            if diff1 < 0:
                for i in range(abs(diff1)) :
                    self.decrease_1MHz()
        else:
            print "Frequency is too far off. Please make sure it is within 100 MHz of 10272 MHz."

    def goto_freq10262MHz(self):
        print "go to freq 10262 MHz"
        diff1 = 10262-self.ui.lcdNumber.intValue()
        if abs(diff1) < 100:
            if diff1 > 0:
                for i in range(diff1) :
                    self.increase_1MHz()
            if diff1 < 0:
                for i in range(abs(diff1)) :
                    self.decrease_1MHz()
        else:
            print "Frequency is too far off. Please make sure it is within 100 MHz of 10262 MHz."

    def manual_entry(self):
        print "manual entry"
        diff1 = int(self.ui.manual_entry.value())-self.ui.lcdNumber.intValue()
        if abs(diff1) < 100:
            if diff1 > 0:
                for i in range(diff1) :
                    self.increase_1MHz()
            if diff1 < 0:
                for i in range(abs(diff1)) :
                    self.decrease_1MHz()


# execute this if we started this file
if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    myapp = IodineEOM()
    myapp.show()
    sys.exit(app.exec_())