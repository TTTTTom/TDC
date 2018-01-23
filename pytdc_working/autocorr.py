'''
Created on Oct 29, 2012

@author: cqt
'''

# Calculates autocorrelation function for the photon arrival times

import sys, time
import struct
from numpy import *
import matplotlib.pyplot as plt
# from PyQt4 import QtGui
import tkFileDialog

#from psychopy import  gui, core
#import pylab

#Open a dialog box to select files from


class autocorr():
    def __init__(self, max = 3000000.0, bin = 1000.0):
        self.max     = max
        self.bin     = bin
        self.current = []
        self.hsize   = int(max / bin)
        self.histro  = array([0] * self.hsize)
        self.counter = 0
    
    def add(self, delay):
        # remove outdated elements from the list
        self.current[:] = [x for x in self.current if ((delay - x) < self.max)]
        
        # add list elements to the 
        for x in self.current:
            try:
                index = int( (delay - x) / self.bin )
                self.histro[index] += 1 
            except:
                pass
    
        self.counter += 1
        if (self.counter % 10000 == 0):
            print self.counter, " Points processed ... "
    
        self.current.append(delay)
        
        
    def save(self, fname):
        pass
        
def main():
    ac    = autocorr()
#    app   = QtGui.QApplication(sys.argv)
#    fname = QtGui.QFileDialog.getSaveFileName(None, 'Open timestamp file', '*.dat')
#    fname = "C:\\Users\\cqt\\Desktop\\timestamps2.dat"
#    fname = gui.fileOpenDlg('.')
#    if not fname:
#        core.quit()
        
    fname = tkFileDialog.askopenfilename()
    print "Processing ... ", fname 

    with open(fname, 'rb') as f:
        while(True):
            try:
                [delay] = struct.unpack('d', f.read(8) )
                ac.add(delay)
            except:
                print "Run out of data, exiting ..." 
                plt.plot(arange(0.0, ac.max, ac.bin), ac.histro)
                plt.show()
                return


if __name__ == "__main__":
    main()