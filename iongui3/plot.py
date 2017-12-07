__author__ = 'Dima'

from scandata import ScanData
from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
import sys, math, time
from fit import freq_fit_gui, sine_fit_gui
from display_counters_ui import Ui_DisplayCounterDialog
#from errorbar import ErrorBarPlotCurve
import numpy

# Plots the data in the scandata class, used to display the data in
# the frequency scan, delay scan and simple scan modes
class ScanDataPlot(QtCore.QObject):
    # initialise
    def __init__(self, qwt_plot, scandata):

        self.plot     = qwt_plot
        self.scandata = scandata

        # average value plot
        self.plotavg  = Qwt5.QwtPlotCurve("Average")
        self.plotavg.setStyle(Qwt5.QwtPlotCurve.NoCurve)
        self.plotavg.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Ellipse,
                                      Qt.QBrush(Qt.Qt.red),
                                      Qt.QPen(Qt.Qt.red),
                                      Qt.QSize(7, 7)))
        self.plotavg.attach(self.plot)

        # Current value plot
        self.plotline = Qwt5.QwtPlotCurve("Counts")
        self.plotline.setStyle(Qwt5.QwtPlotCurve.NoCurve)
        self.plotline.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Ellipse,
                                      Qt.QBrush(Qt.Qt.blue),
                                      Qt.QPen(Qt.Qt.black),
                                      Qt.QSize(7, 7)))

#        self.plotline = ErrorBarPlotCurve("Counts")
        self.plotline.attach(self.plot)

        # extra plots for the counters, etc
        self.extra_plots = {}

        # Fit plot
        self.plotfit  = Qwt5.QwtPlotCurve("Fit")
        self.plotfit.setStyle(Qwt5.QwtPlotCurve.Lines)
        self.plotfit.attach(self.plot)

        self.config_gui = display_counters_gui(self.change_plot)
#        self.fit = freq_fit_gui(self.plot, self.plotfit, self.scandata)

        self.picker = Qwt5.QwtPlotPicker(Qwt5.QwtPlot.xBottom, Qwt5.QwtPlot.yLeft,
                                         Qwt5.QwtPicker.PointSelection | Qwt5.QwtPicker.DragSelection,
                                         Qwt5.QwtPlotPicker.VLineRubberBand,
                                         Qwt5.QwtPicker.AlwaysOn,
                                         self.plot.canvas())
        self.picker.setTrackerMode(Qwt5.QwtPicker.AlwaysOn)
        self.picker.setTrackerPen(Qt.QPen(Qt.Qt.red))

        self.zoomer = Qwt5.QwtPlotZoomer(Qwt5.QwtPlot.xBottom,
                                         Qwt5.QwtPlot.yLeft,
                                         Qwt5.QwtPicker.DragSelection,
                                         Qwt5.QwtPicker.AlwaysOff,
                                         self.plot.canvas())
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

        self.marker = Qwt5.QwtPlotMarker()
        self.marker.setLineStyle(Qwt5.QwtPlotMarker.VLine | Qwt5.QwtPlotMarker.HLine)
        self.marker.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        self.marker.setLinePen(QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.DashLine))
        self.marker.setValue(0.0, 0.0)
        self.marker.attach(self.plot)

        self.grid = Qwt5.QwtPlotGrid()
        self.grid.attach(self.plot)
        self.grid.setPen(Qt.QPen(Qt.Qt.black, 0, Qt.Qt.DotLine))

        self.plot.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)

        self.connect(self.plot, QtCore.SIGNAL("mouseMoveEvent()"), self.mouse_moved_slot)

    def enable_top_axis(self, enable):
        self.plot.enableAxis(3, enable)

    def rescale_top_axis(self, start, start2, step, step2):
        lowerBound = self.plot.axisScaleDiv(Qwt5.QwtPlot.xBottom).lowerBound()
        upperBound = self.plot.axisScaleDiv(Qwt5.QwtPlot.xBottom).upperBound()

        if (step == 0.0):
            low = start2
            high = start2
        else:
            low  = start2 + (lowerBound - start) * step2 / step
            high = start2 + (upperBound - start) * step2 / step

        self.plot.setAxisScale(Qwt5.QwtPlot.xTop, low, high)

    # Mouse event to pick the value
    def mouse_moved_slot(self, e):
        canvasPos = self.plot.canvas().mapFrom(self, e.pos())
        xFloat = self.invTransform(Qwt5.QwtPlot.xBottom, canvasPos.x())
        yFloat = self.invTransform(Qwt5.QwtPlot.yLeft, canvasPos.y())
        self.marker.setValue(xFloat, yFloat)
        self.replot()

    # replot the experimental data
    def replot(self):
        # replot the graph
        y = self.scandata.get()
        x = self.scandata.getx()
        self.plotline.setData(x, y)
        # and the averaged line
        yavg = self.scandata.get_avg()
        self.plotavg.setData(x, yavg)

        # And whatever extra plots the user have requested
        for (counter, threshold) in self.extra_plots.keys():
            ycnt = self.scandata.get_counter_data(counter, threshold)
#            print x, ycnt
            self.extra_plots[(counter, threshold)].setData(x, ycnt)

        self.plot.setAxisAutoScale(Qwt5.QwtPlot.xBottom)
        self.plot.setAxisAutoScale(Qwt5.QwtPlot.yLeft)
        self.zoomer.setZoomBase()

        self.plot.replot()

    def config(self):
        self.config_gui.show()
        print "plot config is called"

    # attach fit to the plot
    # fit is a class that does the fit
    def add_fit(self, fit):
        return fit(self.plot, self.plotfit, self.scandata)

    def add_plot(self, counter, threshold):
        # If plot already exist, do nothing
        if (counter, threshold) in self.extra_plots.keys():
            return

        # add plot if we can not find it in the list
        color = self.plot_color(counter, threshold)
        line = Qwt5.QwtPlotCurve("Counts")
        line.setStyle(Qwt5.QwtPlotCurve.NoCurve)
        line.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Ellipse,
                                      Qt.QBrush(color),
                                      Qt.QPen(color),
                                      Qt.QSize(7, 7)))

        line.attach(self.plot)
        self.extra_plots[(counter, threshold)] = line
        self.replot()

    # remove line from the plot
    def del_plot(self, counter, threshold):
        # If plot already exist, do nothing
        if (counter, threshold) in self.extra_plots.keys():
            plot = self.extra_plots.pop( (counter, threshold) )
            plot.detach()
#            del plot
            self.replot()

    # Function tha gui calls to change what counters we want to display
    def change_plot(self, counter, threshold, checked):
        print "Counter=", counter, " Threshold=", threshold, " Checked=", checked

        if checked:
            self.add_plot(counter, threshold)
        else:
            self.del_plot(counter, threshold)

    # Table of colors for different plots
    def plot_color(self, counter, threshold):
        color_table = \
            {(0,True): Qt.Qt.darkYellow,  (0,False): Qt.Qt.darkYellow,
             (1,True): Qt.Qt.darkGreen,   (1,False): Qt.Qt.darkGreen,
             (2,True): Qt.Qt.darkCyan,    (2,False): Qt.Qt.darkCyan,
             (3,True): Qt.Qt.darkMagenta, (3,False): Qt.Qt.darkMagenta,
             (4,True): Qt.Qt.darkRed,     (4,False): Qt.Qt.darkRed,
             (5,True): Qt.Qt.darkBlue,    (5,False): Qt.Qt.darkBlue,
             (6,True): Qt.Qt.darkGray,    (6,False): Qt.Qt.darkGray,
             (7,True): Qt.Qt.black,       (7,False): Qt.Qt.black }
        return color_table.get((counter, threshold), Qt.Qt.black)


class display_counters_gui(QtGui.QDialog):
    def __init__(self, callback_func, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DisplayCounterDialog()
        self.ui.setupUi(self)

        # List of checkboxes
        self.av_boxes = [ self.ui.cntav1, self.ui.cntav2, self.ui.cntav3, self.ui.cntav4,
                          self.ui.cntav5, self.ui.cntav6, self.ui.cntav7, self.ui.cntav8]
        self.th_boxes = [ self.ui.cntth1, self.ui.cntth2, self.ui.cntth3, self.ui.cntth4,
                          self.ui.cntth5, self.ui.cntth6, self.ui.cntth7, self.ui.cntth8]

        # list of slot functions to process clicks
        self.av_slots = [self.slot_cntav1, self.slot_cntav2, self.slot_cntav3, self.slot_cntav4,
                         self.slot_cntav5, self.slot_cntav6, self.slot_cntav7, self.slot_cntav8]
        self.th_slots = [self.slot_cntth1, self.slot_cntth2, self.slot_cntth3, self.slot_cntth4,
                         self.slot_cntth5, self.slot_cntth6, self.slot_cntth7, self.slot_cntth8]

        self.update_plots = callback_func

        for box, slot in zip(self.av_boxes, self.av_slots):
            QtCore.QObject.connect(box, QtCore.SIGNAL('clicked()'), slot)
        for box, slot in zip(self.th_boxes ,self.th_slots):
            QtCore.QObject.connect(box, QtCore.SIGNAL('clicked()'), slot)

    def checkbox_clicked(self, counter, threshold):
        if threshold:
            checked = self.th_boxes[counter].isChecked()
        else:
            checked = self.av_boxes[counter].isChecked()
        self.update_plots(counter, threshold, checked)


    # Each checkbox has its own slot function to process clicks
    def slot_cntav1(self):
        self.checkbox_clicked(0, False)
    def slot_cntav2(self):
        self.checkbox_clicked(1, False)
    def slot_cntav3(self):
        self.checkbox_clicked(2, False)
    def slot_cntav4(self):
        self.checkbox_clicked(3, False)
    def slot_cntav5(self):
        self.checkbox_clicked(4, False)
    def slot_cntav6(self):
        self.checkbox_clicked(5, False)
    def slot_cntav7(self):
        self.checkbox_clicked(6, False)
    def slot_cntav8(self):
        self.checkbox_clicked(7, False)
    def slot_cntth1(self):
        self.checkbox_clicked(0, True)
    def slot_cntth2(self):
        self.checkbox_clicked(1, True)
    def slot_cntth3(self):
        self.checkbox_clicked(2, True)
    def slot_cntth4(self):
        self.checkbox_clicked(3, True)
    def slot_cntth5(self):
        self.checkbox_clicked(4, True)
    def slot_cntth6(self):
        self.checkbox_clicked(5, True)
    def slot_cntth7(self):
        self.checkbox_clicked(6, True)
    def slot_cntth8(self):
        self.checkbox_clicked(7, True)




# class for testing
class PlotWindow(Qt.QMainWindow):
    def __init__(self, parent=None):
        Qt.QMainWindow.__init__(self, parent)

        self.data   = ScanData()
        for x in xrange(100):
            counters = [1.0*math.sin(x/10.0)**2, 0., 0.7*math.sin(x/10.0)**2, 0., 0., 0., 0., 0.,  \
                        0.8*math.sin(x/10.0)**2, 0., 0.4*math.sin(x/10.0)**2, 0., 0., 0., 0., 0.]
            fpga_data = [('a', 12), ('a', 2), ('a', 11), ('a', 10), ('a', 2), ('a', 13)]
            self.data.add_pair(x/10.0, math.sin(x/10.0)**2, [10,9], counters, fpga_data)

        # Initialize a QwPlot central widget
        self.qwt_plot = Qwt5.QwtPlot(self)
        self.qwt_plot.resize(700,400)
        self.sd       = ScanDataPlot(self.qwt_plot, self.data)
        self.fit = self.sd.add_fit(sine_fit_gui)
        self.sd.replot()
#        self.fit.show()

        time.sleep(1.0)
        self.sd.add_plot(0, True)
        self.sd.add_plot(2, True)
        self.sd.replot()

        self.sd.config()

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    wnd  = PlotWindow(None)
    wnd.resize(800, 500)
    wnd.show()

    sys.exit(app.exec_())
