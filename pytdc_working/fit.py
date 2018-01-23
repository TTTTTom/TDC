'''
Created on Sep 19, 2012

@author: cqt
'''
import pylab
import numpy
from scipy import optimize
import pickle
import sys
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5

from sine_fit_ui import Ui_SineDialog


# Sin fit function
def sin_func(x, a, b, phi, freq):
    return a + b * numpy.sin(x * 2 * numpy.pi * freq / 1000.0 + 2 * numpy.pi * phi / 360)

# Difference between fit and experimental data
def sin_fit_error(params, y, x, freq):
    a, b, phi = params
    return y - sin_func(x, a, b, phi, freq)

    
# GUI for setting fit parameters for the plot
class sine_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_SineDialog()
        self.ui.setupUi(self)

        self.fit      = SineFit()
        self.plot     = plot
        self.plotline = plotline
        self.scandata = scandata
        
        QtCore.QObject.connect(self.ui.aSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.bSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.PhiSpinBox,  QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.xminSpinBox, QtCore.SIGNAL('valueChanged(double)'),   self.slot_boundary_changed)
        QtCore.QObject.connect(self.ui.xmaxSpinBox, QtCore.SIGNAL('valueChanged(double)'),   self.slot_boundary_changed)
        QtCore.QObject.connect(self.ui.fitButton,   QtCore.SIGNAL('clicked()'),              self.slot_fit_clicked) 
        QtCore.QObject.connect(self.ui.doneButton,  QtCore.SIGNAL('clicked()'),              self.slot_done_clicked)

        self.update_display()

        self.xmin = self.ui.xminSpinBox.value()
        self.xmax = self.ui.xmaxSpinBox.value()

        try:
            self.load_freq()
        except:
            self.ui.fSpinBox.setValue(30.178)


    def save_freq(self):
        with open('f_fit.dat', 'w') as f:
            pickle.dump(self.ui.fSpinBox.value(), f)
        f.closed

    def load_freq(self):
        with open('f_fit.dat', 'r') as f:
            self.ui.fSpinBox.setValue(pickle.load(f))
        f.closed

    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(),
                            self.ui.bSpinBox.value(),
                            self.ui.PhiSpinBox.value(),
                            self.ui.fSpinBox.value())
        self.update_plot()
        self.save_freq()

    def slot_boundary_changed(self, value):
        self.xmin = self.ui.xminSpinBox.value()
        self.xmax = self.ui.xmaxSpinBox.value()
        self.update_plot()
        
    def slot_fit_clicked(self):
        # Get the data interval
#        interval = self.plot.axisScaleDiv( Qwt5.QwtPlot.xBottom ).interval()
#        self.xmin = interval.minValue()
#        self.xmax = interval.maxValue()

        # get experimental data
        x    = self.scandata.getx()     
        yavg = self.scandata.get_avg()
        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if(val >= self.xmin and val <= self.xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice))
        # fit them
        self.fit_data()
        
        # Display result
        self.update_display()
        self.update_plot()

    def get_xslice(self):
        x    = self.scandata.getx()
        xslice = []
        for idx, val in enumerate(x):
            if(val >= self.xmin and val <= self.xmax):
                xslice.append(val)
        return xslice

    def get_yslice(self):
        x    = self.scandata.getx()
        yavg = self.scandata.get_avg()
        yslice = []
        for idx, val in enumerate(x):
            if(val >= self.xmin and val <= self.xmax):
                yslice.append(yavg[idx])
        return yslice

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()


    def update_display(self):
        [a, b, phi, freq] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.bSpinBox.setValue(b)
        self.ui.PhiSpinBox.setValue(phi)
        self.ui.fSpinBox.setValue(freq)

    # run a fit program, 
    def fit_data(self):
        self.fit.fit()
        self.fit.print_all()

    # redraws fit line        
    def update_plot(self):
#        x = self.scandata.getx()
#        try:
#            xlarge = numpy.linspace(x[0], x[-1], 400)
#            y = self.fit.function_data(xlarge)
#            self.plotline.setData(xlarge, y)
#            self.plot.replot()
#        except IndexError:
#            pass
        try:
            xsmall = numpy.linspace(self.xmin, self.xmax, 400)
            y = self.fit.function_data(xsmall)
            self.plotline.setData(xsmall, y)
            self.plot.replot()
        except IndexError:
            pass


# Fit typical frequency scan data
class SineFit(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.a = 100    # Background level (counts)
        self.b = 10     # Peak height (counts)
        self.phi = 180    # Phase (degrees)
        self.freq = 30     # Frequency of modulation (MHz)

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program 
    def fit(self):
        self.a = sum(self.y)/float(len(self.y))
        self.b = max(self.y) - min(self.y)
        [a, b, phi], flag = \
            optimize.leastsq(sin_fit_error, [self.a, self.b, self.phi],
                             args=(self.y, self.x, self.freq))
        if b < 0:   # There are two local minima with the same physical meaning. This makes the output unambiguous.
            b = -b
            phi += 180
        self.a = a
        self.b = b
        self.phi = phi % 360
    
    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, b, phi, freq):
        self.a = a    # Background level (counts)
        self.b = b    # Amplitude (counts)
        self.phi = phi  # Phase (degrees)
        self.freq = freq # Modulation frequency (MHz)
    
    def get_params(self):
        return [self.a, self.b, self.phi, self.freq]

    def func(self, x):
        return sin_func(x, self.a, self.b, self.phi, self.freq)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]
    
    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "b          = ", self.b
        print "Phase      = ", self.phi


if __name__ == '__main__':
    # load the data
#    t, x1, x2 = numpy.loadtxt("C:\\Users\\cqt\\Desktop\\testfit.dat", unpack=True, delimiter=",")
    t, x1, x2 = numpy.loadtxt("test.dat", unpack=True, delimiter=",")

    print t, x1
    
    fitted = SineFit()
    fitted.set_data(t, x1)
    fitted.set_params(1.0, 7.0, 10.0, 10.0)
    fitted.fit()
    fitted.print_all()

    # show is necessary to display the plot when
    # not in interactive mode
    # pylab.show()
    
    #app = QtGui.QApplication(sys.argv)
    #myapp = freq_fit_gui()
    #myapp.show()

    #sys.exit(app.exec_())