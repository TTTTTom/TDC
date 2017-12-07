'''
Created on 13-May-2011

@author: cqt
'''

from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
from histogram import HistogramItem
from counters  import CounterConfig

# Class takes care of histrogram, threshold, etc
class IonData():
    def __init__(self, ui):
#        self.plot       = ui.histrogram_plot
        self.plot       = ui.histrogram_qwt_plot
        self.threshold  = ui.thresholdBox
        self.applyth    = ui.apply_threshold
        self.number     = ui.lcdNumber
        self.nrep       = ui.repetitionBox
        self.hist       = None
    
#        self.plotline = Qwt5.QwtPlotCurve("Histogram")
        self.plotline = HistogramItem()
        self.plotline.setColor(Qt.Qt.blue)
        self.plotline.attach(self.plot)

        self.counter_config = CounterConfig()

        # Setup histogram plot
        #self.plot.axes.clear()
        #self.plot.axes.set_title("Histrogram")
        #self.plot.axes.set_ylabel("Counts")
        #self.plot.axes.set_xlim(0, 20)
        #self.plot.axes.grid(True)
        #self.plot.draw()

    # Parses the settings from the JSON file
    def load_settings(self, data):
        try:
            self.threshold.setValue(data["threshold"])
            self.nrep.setValue(data["nrep"])
            self.applyth.setChecked(data["applyth"])
        except KeyError as e:
            print "Key error in the settings data: ", e.value

    def show_counter_config(self):
        self.counter_config.show()

    def set_histogram(self, hist):    
        self.hist = hist
    
    def new_histogram(self, intensity=0):
        self.data, fpga_data  = self.hist.pop(0)
        histogram = self.data['a']
        x = range(0, len(histogram))

        numValues = 20
        intervals = []
        values    = Qwt5.QwtArrayDouble(numValues)

        for i in range(numValues):
            intervals.append(Qwt5.QwtDoubleInterval(x[i], x[i]+1));
            values[i] = histogram[i]

        self.plotline.setData(Qwt5.QwtIntervalData(intervals, values))

        # self.plotline.setData(histrogram[:20])
        self.plot.replot()
        
        total   = sum(histogram)
        
        # calculates thresholded, or not thresholded value for a experimental run 
        if (self.applyth.isChecked()):
            belowth = sum(histogram[0:self.threshold.value()])
            value = 1.0 - float(belowth) / float(total)
        else:
            average = 0 
            for i in range(0, len(histogram)):
                average += i * histogram[i] 
                
            if (total != 0):
                value = float(average) / float(total)
            else:
                value = 0.00
        
        # Show the computed value
        self.number.display(value)

        self.counter_config.process(self.data, intensity)

        v1 = self.counter_config.counter_data.get_above_thr()
        v2 = self.counter_config.counter_data.get_average()
        all_values = v1 + v2

        return value, histogram, all_values, fpga_data
