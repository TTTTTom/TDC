'''
Created on Sep 19, 2012

@author: cqt
'''
import pylab
import numpy
from scipy import optimize, misc

import sys
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5

from fit_ui import  Ui_Dialog
from sine_fit_ui import Ui_SineDialog
from ramsey_fit_ui import Ui_RamseyDialog
from coherent_thermal_fit_ui import Ui_Coh_Th_Dialog
from antiX_fit_ui import Ui_AntiX_Dialog


# Sin fit function
def sinfunc(x, a, b, Tpi):
    if (a <0 or b < 0):
        return 1e15
    else:
        return a + b * numpy.sin(x * numpy.pi / (2.0 * Tpi) ) ** 2

# Ramsey fit function
def ramseyfunc(x, a, b, f, decay):
    if (a <0 or b < 0):
        return 1e15
    else:
        return a + b * numpy.cos(x * 2 * numpy.pi * f) * numpy.exp(-x/decay)

# Coherent fit function
def coherentfunc(x, a, nbar, n_total, Tpi, gamma):
        if (a < 0 or nbar < 0):
            return 1e15
        else:
            coh_array = numpy.array([numpy.exp(-nbar)*(nbar**n)/int(misc.factorial(n)) * numpy.cos(numpy.sqrt(n+1) * x * numpy.pi/Tpi) * numpy.exp(- numpy.sqrt(n+1) * gamma * x) for n in range(0,n_total)])
            return (a/2) * (1 - numpy.sum(coh_array, axis = 0))

# Thermal fit function
def thermalfunc(x, a, nbar, n_total, Tpi, gamma):
    if (a < 0 or nbar < 0):
        return 1e15
    else:
        th_array = numpy.array([(nbar**n)/((nbar+1)**(n+1)) * numpy.cos(
            numpy.sqrt(n + 1) * x * numpy.pi / Tpi) * numpy.exp(- numpy.sqrt(n + 1) * gamma * x) for n in
                                 range(0, n_total)])
        return (a / 2) * (1 - numpy.sum(th_array, axis = 0))

# Whatever we can use to fit frequency scan ... function
def freqfunc (x, a, b, f0, Tpi, T):
    if (a < 0 or b < 0 or b > 99999 or Tpi <= 0 or T < 0):
        return 1e15
    else:
        # omega =  numpy.pi / Tpi
        omega1 = numpy.sqrt((numpy.pi / Tpi)**2  + ( 2.0 * numpy.pi * (x - f0) )**2 )
        #if a + b * ( numpy.sin(omega * T / 2.0) )**2 > 1:   # Disabled since we can use 3 bright ions without threshold
        #    return 1e15
        #else:
        #    return a + b * ( omega * numpy.sin(omega1 * T / 2.0) / omega1 )**2
        return a + b * ( (numpy.pi / Tpi) * numpy.sin(omega1 * T / 2.0) / omega1 )**2

def antiX_func(x, a, b1, b2, f1, f2, Tpi1, Tpi2, T):
    if (a < 0 or b1 < 0 or b2 < 0 or b1 > 99999 or b2 > 99999 or Tpi1 <= 0 or Tpi2 <= 0 or T < 0):
        return 1e15
    else:
        # omega =  numpy.pi / Tpi
        omega1 = numpy.sqrt((numpy.pi / Tpi1) ** 2 + (2.0 * numpy.pi * (x - f1)) ** 2)
        omega2 = numpy.sqrt((numpy.pi / Tpi2) ** 2 + (2.0 * numpy.pi * (x - f2)) ** 2)
        # if a + b * ( numpy.sin(omega * T / 2.0) )**2 > 1:   # Disabled since we can use 3 bright ions without threshold
        #    return 1e15
        # else:
        #    return a + b * ( omega * numpy.sin(omega1 * T / 2.0) / omega1 )**2
        return a + b1*((numpy.pi / Tpi1) * numpy.sin(omega1 * T / 2.0) / omega1) ** 2 + b2*((numpy.pi / Tpi2) * numpy.sin(omega2 * T / 2.0) / omega2) ** 2


# Differecne between fit and experimental data
def sinfit(params, y, x):
    a, b, Tpi  = params
    return y - sinfunc(x, a, b, Tpi)

# Differecne between fit and experimental data  
def freqfit(params, y, x):
    a, b, f0, Tpi, T = params
    return y - freqfunc(x, a, b, f0, Tpi, T)

def antiX_fit(params, y, x):
    a, b1, b2, f1, f2, Tpi1, Tpi2, T = params
    return y - antiX_func(x, a, b1, b2, f1, f2, Tpi1, Tpi2, T)

# Differecne between fit and experimental data
def freqfitWoPT(params, y, x, T):
    a, b, f0, Tpi = params
    return y - freqfunc(x, a, b, f0, Tpi, T)

# Difference between fit and experimental data
def ramseyfit(params, y, x):
    a, b, f, decay = params
    return y - ramseyfunc(x, a, b, f, decay)

def coherentfit(params, y, x, n, Tpi, gamma):
    a, nbar = params
    return y - coherentfunc(x, a, nbar, n, Tpi, gamma)

def thermalfit(params, y, x, n, Tpi, gamma):
    a, nbar = params
    return y - thermalfunc(x, a, nbar, n, Tpi, gamma)
    
# GUI for setting fit parameters for the plot
class sine_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_SineDialog()
        self.ui.setupUi(self)

        self.fit      = sine_fit()
        self.plot     = plot
        self.plotline = plotline
        self.scandata = scandata
        
        QtCore.QObject.connect(self.ui.aSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.bSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TpiSpinBox , QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton,   QtCore.SIGNAL('clicked()'),              self.slot_fit_clicked) 
        QtCore.QObject.connect(self.ui.doneButton,  QtCore.SIGNAL('clicked()'),              self.slot_done_clicked) 
        
        self.update_display()

    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a = data['a']
            self.fit.b = data['b']
            self.fit.Tpi = data['Tpi']
        except KeyError as e:
            print "Key error in input data: ", e
        self.update_display()


    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.bSpinBox.value(), \
                            self.ui.TpiSpinBox.value() )
        self.update_plot()
        
    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv( Qwt5.QwtPlot.xBottom ).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()

        # get experimental data
        x    = self.scandata.getx()     
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if(val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice) )
        # fit them
        self.fit_data()
        
        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()


    def update_display(self):
        [a, b, Tpi] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.bSpinBox.setValue(b)
        self.ui.TpiSpinBox.setValue(Tpi)

    # run a fit program, 
    def fit_data(self):
        self.fit.fit()
        self.fit.print_all()

    # redraws fit line        
    def update_plot(self):
        x = self.scandata.getx()
        try:
            #xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            print "Fit out of bounds"
        except ValueError:
            print "Nothing to fit"
            
 
# GUI for setting fit parameters for the plot
class coherent_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Coh_Th_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Coherent Fit")

        self.fit      = CoherentFit()
        self.plot     = plot
        self.plotline = plotline
        self.scandata = scandata

        QtCore.QObject.connect(self.ui.aSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.nbarSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.nSpinBox , QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TpiSpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.gammaSpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton,   QtCore.SIGNAL('clicked()'),              self.slot_fit_clicked)
        QtCore.QObject.connect(self.ui.doneButton,  QtCore.SIGNAL('clicked()'),              self.slot_done_clicked)

        self.update_display()

    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a = data['a']
            self.fit.nbar = data['nbar']
            self.fit.n = data['n']
            self.fit.Tpi = data['Tpi']
            self.fit.gamma = data['gamma']
        except KeyError as e:
            print "Key error in input data: ", e
        self.update_display()


    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.nbarSpinBox.value(), \
                            self.ui.nSpinBox.value(), \
                            self.ui.TpiSpinBox.value(), \
                            self.ui.gammaSpinBox.value() )
        try:
            self.update_plot()
        except ValueError:
            print "Nothing to update"

    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv( Qwt5.QwtPlot.xBottom ).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()

        # get experimental data
        x    = self.scandata.getx()
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if(val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice) )
        # fit them
        self.fit_data()

        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()


    def update_display(self):
        [a, nbar, n, Tpi, gamma] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.nbarSpinBox.setValue(nbar)
        self.ui.nSpinBox.setValue(n)
        self.ui.TpiSpinBox.setValue(Tpi)
        self.ui.gammaSpinBox.setValue(gamma)

    # run a fit program,
    def fit_data(self):
        self.fit.fit()
        self.fit.print_all()

    # redraws fit line
    def update_plot(self):
        x = self.scandata.getx()
        try:
            #xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            pass

class thermal_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Coh_Th_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Thermal Fit")

        self.fit      = ThermalFit()
        self.plot     = plot
        self.plotline = plotline
        self.scandata = scandata

        QtCore.QObject.connect(self.ui.aSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.nbarSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.nSpinBox , QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TpiSpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.gammaSpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton,   QtCore.SIGNAL('clicked()'),              self.slot_fit_clicked)
        QtCore.QObject.connect(self.ui.doneButton,  QtCore.SIGNAL('clicked()'),              self.slot_done_clicked)

        self.update_display()

    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a = data['a']
            self.fit.nbar = data['nbar']
            self.fit.n = data['n']
            self.fit.Tpi = data['Tpi']
            self.fit.gamma = data['gamma']
        except KeyError as e:
            print "Key error in input data: ", e
        self.update_display()


    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.nbarSpinBox.value(), \
                            self.ui.nSpinBox.value(), \
                            self.ui.TpiSpinBox.value(), \
                            self.ui.gammaSpinBox.value() )
        self.update_plot()

    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv( Qwt5.QwtPlot.xBottom ).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()

        # get experimental data
        x    = self.scandata.getx()
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if(val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice) )
        # fit them
        self.fit_data()

        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()


    def update_display(self):
        [a, nbar, n, Tpi, gamma] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.nbarSpinBox.setValue(nbar)
        self.ui.nSpinBox.setValue(n)
        self.ui.TpiSpinBox.setValue(Tpi)
        self.ui.gammaSpinBox.setValue(gamma)

    # run a fit program,
    def fit_data(self):
        self.fit.fit()
        self.fit.print_all()

    # redraws fit line
    def update_plot(self):
        x = self.scandata.getx()
        try:
            # xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            print "Fit out of bounds"
        except ValueError:
            print "Nothing to fit"

class ramsey_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_RamseyDialog()
        self.ui.setupUi(self)

        self.fit = RamseyFit()
        self.plot = plot
        self.plotline = plotline
        self.scandata = scandata

        QtCore.QObject.connect(self.ui.aSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.bSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.dSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton, QtCore.SIGNAL('clicked()'), self.slot_fit_clicked)
        QtCore.QObject.connect(self.ui.doneButton, QtCore.SIGNAL('clicked()'), self.slot_done_clicked)

        self.update_display()

    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a = data['a']
            self.fit.b = data['b']
            self.fit.f = data['Frequency']
            self.fit.d = data['Decoherence time']
        except KeyError as e:
            print "Key error in input data: ", e
        self.update_display()

    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.bSpinBox.value(), \
                            self.ui.fSpinBox.value(), \
                            self.ui.dSpinBox.value())
        self.update_plot()

    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv(Qwt5.QwtPlot.xBottom).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()

        # get experimental data
        x = self.scandata.getx()
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if (val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice))
        # fit them
        self.fit_data()

        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()

    def update_display(self):
        [a, b, f, d] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.bSpinBox.setValue(b)
        self.ui.fSpinBox.setValue(f)
        self.ui.dSpinBox.setValue(d)

    # run a fit program,
    def fit_data(self):
        self.fit.fit()
        self.fit.print_all()

    # redraws fit line
    def update_plot(self):
        x = self.scandata.getx()
        try:
            #xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            print "Fit out of bounds"
        except ValueError:
            print "Nothing to fit"


# GUI for setting fit parameters for the plot
class freq_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.fit = freq_fit()
        self.plot     = plot
        self.plotline = plotline
        self.scandata = scandata

        QtCore.QObject.connect(self.ui.aSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.bSpinBox,    QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TpiSpinBox , QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TSpinBox ,   QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.freqSpinBox, QtCore.SIGNAL('valueChanged(double)'),   self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton,   QtCore.SIGNAL('clicked()'),              self.slot_fit_clicked)
        QtCore.QObject.connect(self.ui.doneButton,  QtCore.SIGNAL('clicked()'),              self.slot_done_clicked)

        self.update_display()


    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a    = data['a']
            self.fit.b    = data['b']
            self.fit.Tpi  = data['Tpi']
            self.fit.T    = data['T']
            self.fit.freq = data['freq']
        except KeyError as e:
            print "Eye error in input data: ", e
        self.update_display()


    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.bSpinBox.value(), \
                            self.ui.freqSpinBox.value(), \
                            self.ui.TpiSpinBox.value(), \
                            self.ui.TSpinBox.value() )
        self.update_plot()

    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv( Qwt5.QwtPlot.xBottom ).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()
        print "Axis range: ", xmin, xmax

        # get experimental data
        x    = self.scandata.getx()
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if(val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        if self.ui.AutoFindMax.isChecked():
            try:
                self.ui.freqSpinBox.setValue(xslice[yslice.index(max(yslice))])
            except ValueError:
                print "Nothing to fit"

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice) )
        # fit them
        self.fit_data()

        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()


    def update_display(self):
        [a, b, f0, Tpi, T] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.bSpinBox.setValue(b)
        self.ui.freqSpinBox.setValue(f0)
        self.ui.TpiSpinBox.setValue(Tpi)
        self.ui.TSpinBox.setValue(T)

        # run a fit program,
    def fit_data(self):
        if self.ui.includePulseTBox.isChecked():
            self.fit.fit()
        else:
            self.fit.fitWoPT()
        self.fit.print_all()

    # redraws fit line        
    def update_plot(self):
        x = self.scandata.getx()
        try:
            #xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            print "Fit out of bounds"
        except ValueError:
            print "Nothing to fit"


class anticrossing_fit_gui(QtGui.QDialog):
    def __init__(self, plot, plotline, scandata, parent=None):
        print "__init__ is called"
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_AntiX_Dialog()
        self.ui.setupUi(self)

        self.fit = anticrossing_freq_fit()
        self.plot = plot
        self.plotline = plotline
        self.scandata = scandata

        QtCore.QObject.connect(self.ui.aSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.b1SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.b2SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.Tpi1SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.Tpi2SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.TSpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.freq1SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.freq2SpinBox, QtCore.SIGNAL('valueChanged(double)'),
                               self.slot_parameter_changed)
        QtCore.QObject.connect(self.ui.fitButton, QtCore.SIGNAL('clicked()'), self.slot_fit_clicked)
        QtCore.QObject.connect(self.ui.doneButton, QtCore.SIGNAL('clicked()'), self.slot_done_clicked)
        QtCore.QObject.connect(self.ui.freq1SpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq_changed)
        QtCore.QObject.connect(self.ui.freq2SpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_freq_changed)

        self.update_display()

    def slot_freq_changed(self):
        self.ui.Df_label.setText(str(self.ui.freq1SpinBox.value() - self.ui.freq2SpinBox.value()))

    # Loads program settings
    def load_settings(self, data):
        try:
            self.fit.a = data['a']
            self.fit.b = data['b']
            self.fit.Tpi = data['Tpi']
            self.fit.T = data['T']
            self.fit.freq = data['freq']
        except KeyError as e:
            print "Eye error in input data: ", e
        self.update_display()

    def slot_parameter_changed(self, value):
        self.fit.set_params(self.ui.aSpinBox.value(), \
                            self.ui.b1SpinBox.value(), \
                            self.ui.b2SpinBox.value(), \
                            self.ui.freq1SpinBox.value(), \
                            self.ui.freq2SpinBox.value(), \
                            self.ui.Tpi1SpinBox.value(), \
                            self.ui.Tpi2SpinBox.value(), \
                            self.ui.TSpinBox.value())
        self.update_plot()

    def slot_fit_clicked(self):
        # Get the data interval
        interval = self.plot.axisScaleDiv(Qwt5.QwtPlot.xBottom).interval()
        xmin = interval.minValue()
        xmax = interval.maxValue()
        print "Axis range: ", xmin, xmax

        # get experimental data
        x = self.scandata.getx()
        yavg = self.scandata.get_avg()

        xslice = []
        yslice = []
        for idx, val in enumerate(x):
            if (val >= xmin and val <= xmax):
                xslice.append(val)
                yslice.append(yavg[idx])

        #if self.ui.AutoFindMax.isChecked():
        #    self.ui.freqSpinBox.setValue(xslice[yslice.index(max(yslice))])

        self.fit.set_data(numpy.array(xslice), numpy.array(yslice))
        # fit them
        self.fit_data()

        # Display result
        self.update_display()
        self.update_plot()

    def slot_done_clicked(self):
        self.plotline.setData([], [])
        self.plot.replot()

    def update_display(self):
        [a, b1, b2, f1, f2, Tpi1, Tpi2, T] = self.fit.get_params()
        self.ui.aSpinBox.setValue(a)
        self.ui.b1SpinBox.setValue(b1)
        self.ui.b2SpinBox.setValue(b2)
        self.ui.freq1SpinBox.setValue(f1)
        self.ui.freq2SpinBox.setValue(f2)
        self.ui.Tpi1SpinBox.setValue(Tpi1)
        self.ui.Tpi2SpinBox.setValue(Tpi2)
        self.ui.TSpinBox.setValue(T)

        # run a fit program,

    def fit_data(self):
        self.fit.fit()

    # redraws fit line
    def update_plot(self):
        x = self.scandata.getx()
        try:
            #xlarge = numpy.linspace(x[0], x[-1], 400)
            xlarge = numpy.linspace(min(x), max(x), 400)
            y = self.fit.function_data(xlarge)
            self.plotline.setData(xlarge, y)
            self.plot.replot()
        except IndexError:
            print "Fit out of bounds"
        except ValueError:
            print "Nothing to fit"


# Fit typical frequency scan data
class freq_fit():
    def __init__(self):
        self.a      = 0.1    # Background level (counts)
        self.b      = 8       # Peak height (counts)
        self.freq   = 84.5    # Resonance frequency (MHz)
        self.Tpi    = 15      # pi time (microseconds)
        self.T      = 15      # microwave time (microseconds)

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program 
    def fit(self):
        [a, b, freq, Tpi, T], flag  = \
            optimize.leastsq(freqfit, [self.a, self.b, self.freq, self.Tpi, self.T], \
                             args=(self.y, self.x))
            
        self.a    = a
        self.b    = b
        self.freq = freq
        self.Tpi  = Tpi
        self.T    = T

    def fitWoPT(self):
        [a, b, freq, Tpi], flag  = \
            optimize.leastsq(freqfitWoPT, [self.a, self.b, self.freq, self.Tpi], \
                             args=(self.y, self.x, self.T))

        self.a    = a
        self.b    = b
        self.freq = freq
        self.Tpi  = Tpi
    
    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, b, f0, Tpi, T):
        self.a      = a    # Background level (counts)
        self.b      = b    # Peak height (counts)
        self.freq   = f0   # Resonance frequency (MHz)
        self.Tpi    = Tpi  # pi time (microseconds)
        self.T      = T    # microwave time (microseconds)
    
    def get_params(self):
        return [self.a, self.b, self.freq, self.Tpi, self.T]

    def func(self, x):
        return freqfunc(x, self.a, self.b, self.freq, self.Tpi, self.T)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]
    
    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "b          = ", self.b
        print "f0         = ", self.freq
        print "Pi time    = ", self.Tpi
        print "Pulse time = ", self.T

class anticrossing_freq_fit():
    def __init__(self):
        self.a = 0.1  # Background level (counts)
        self.b1 = 0.8  # Peak height (counts)
        self.b2 = 0.8  # Peak height (counts)
        self.freq1 = 105.127  # Resonance frequency (MHz)
        self.freq2 = 105.130  # Resonance frequency (MHz)
        self.Tpi1 = 900  # pi time (microseconds)
        self.Tpi2 = 900  # pi time (microseconds)
        self.T = 900  # microwave time (microseconds)

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program
    def fit(self):
        [a, b1, b2, freq1, freq2, Tpi1, Tpi2, T], flag = \
            optimize.leastsq(antiX_fit, [self.a, self.b1, self.b2, self.freq1, self.freq2, self.Tpi1, self.Tpi2, self.T], \
                             args=(self.y, self.x))

        self.a = a
        self.b1 = b1
        self.b2 = b2
        self.freq1 = freq1
        self.freq2 = freq2
        self.Tpi1 = Tpi1
        self.Tpi2 = Tpi2
        self.T = T

    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, b1, b2, f1, f2, Tpi1, Tpi2, T):
        self.a = a  # Background level (counts)
        self.b1 = b1  # Peak height (counts)
        self.b2 = b2  # Peak height (counts)
        self.freq1 = f1  # Resonance frequency (MHz)
        self.freq2 = f2  # Resonance frequency (MHz)
        self.Tpi1 = Tpi1  # pi time (microseconds)
        self.Tpi2 = Tpi2  # pi time (microseconds)
        self.T = T  # microwave time (microseconds)

    def get_params(self):
        return [self.a, self.b1, self.b2, self.freq1, self.freq2, self.Tpi1, self.Tpi2, self.T]

    def func(self, x):
        return antiX_func(x, self.a, self.b1, self.b2, self.freq1, self.freq2, self.Tpi1, self.Tpi2, self.T)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]

    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "b1          = ", self.b1
        print "b2          = ", self.b2
        print "f1         = ", self.freq1
        print "f2         = ", self.freq2
        print "Pi time 1  = ", self.Tpi1
        print "Pi time 2  = ", self.Tpi2
        print "Pulse time = ", self.T


# Fit typical frequency scan data
class sine_fit():
    def __init__(self):
        self.a      = 0.1    # Background level (counts)
        self.b      = 8       # Peak height (counts)
        self.Tpi    = 15      # pi time (microseconds)

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program 
    def fit(self):
        [a, b, Tpi], flag  = \
            optimize.leastsq(sinfit, [self.a, self.b, self.Tpi], \
                             args=(self.y, self.x))
            
        self.a    = a
        self.b    = b
        self.Tpi  = Tpi
    
    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, b, Tpi):
        self.a      = a    # Background level (counts)
        self.b      = b    # Amplitude (counts)
        self.Tpi    = Tpi  # pi time (microseconds)
    
    def get_params(self):
        return [self.a, self.b, self.Tpi]

    def func(self, x):
        return sinfunc(x, self.a, self.b, self.Tpi)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]
    
    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "b          = ", self.b
        print "Pi time    = ", self.Tpi


# Fit typical Ramsey scan data
class RamseyFit():
    def __init__(self):
        self.a      = 0.5    # Background level (counts)
        self.b      = 0.5       # Peak height (counts)
        self.f    = 0.001      # frequency (Mega Hertz)
        self.decay  = 300     # Decoherence (microseconds)

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program
    def fit(self):
        [a, b, f, decay], flag  = \
            optimize.leastsq(ramseyfit, [self.a, self.b, self.f, self.decay], \
                             args=(self.y, self.x))

        self.a    = a
        self.b    = b
        self.f  = f
        self.decay  = decay

    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, b, f, decay):
        self.a      = a    # Background level (counts)
        self.b      = b    # Amplitude (counts)
        self.f    = f  # frequency (Mega Hertz)
        self.decay  = decay     # Decoherence (microseconds)

    def get_params(self):
        return [self.a, self.b, self.f, self.decay]

    def func(self, x):
        return ramseyfunc(x, self.a, self.b, self.f, self.decay)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]

    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "b          = ", self.b
        print "Frequency  = ", self.f
        print "Decoherence time    = ", self.decay

class CoherentFit():
    def __init__(self):
        self.a      = 0.5    # Amplitude
        self.nbar      = 0.5       # Mean
        self.n    = 0.001      # Size of space
        self.Tpi  = 300     # Rabi oscillation pi time
        self.gamma = 0          # Decay

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program
    def fit(self):
        [a, nbar], flag  = \
            optimize.leastsq(coherentfit, [self.a, self.nbar], \
                             args=(self.y, self.x, self.n, self.Tpi, self.gamma))

        self.a    = a
        self.nbar    = nbar

    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, nbar, n, Tpi, gamma):
        self.a      = a
        self.nbar      = nbar
        self.n    = n
        self.Tpi  = Tpi
        self.gamma = gamma

    def get_params(self):
        return [self.a, self.nbar, self.n, self.Tpi, self.gamma]

    def func(self, x):
        return coherentfunc(x, self.a, self.nbar, self.n, self.Tpi, self.gamma)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]

    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "nbar          = ", self.nbar
        print "n  = ", self.n
        print "Tpi = ", self.Tpi
        print "gamma   = ", self.gamma

class ThermalFit():
    def __init__(self):
        self.a      = 0.5    # Amplitude
        self.nbar      = 0.5       # Mean
        self.n    = 0.001      # Size of space
        self.Tpi  = 300     # Rabi oscillation pi time
        self.gamma = 0          # Decay

        self.x = []
        self.y = []

    # Pass experimental data fo the fit
    def set_data(self, x, y):
        self.x = x
        self.y = y

    # run the fitting program
    def fit(self):
        [a, nbar], flag  = \
            optimize.leastsq(thermalfit, [self.a, self.nbar], \
                             args=(self.y, self.x, self.n, self.Tpi, self.gamma))

        self.a    = a
        self.nbar    = nbar

    # set parameters for the fit, recalculate the function for display
    def set_params(self, a, nbar, n, Tpi, gamma):
        self.a      = a
        self.nbar      = nbar
        self.n    = n
        self.Tpi  = Tpi
        self.gamma = gamma

    def get_params(self):
        return [self.a, self.nbar, self.n, self.Tpi, self.gamma]

    def func(self, x):
        return thermalfunc(x, self.a, self.nbar, self.n, self.Tpi, self.gamma)

    def function_data(self, xlist):
        return [self.func(x) for x in xlist]

    def print_all(self):
        print "Parameters: "
        print "a          = ", self.a
        print "nbar          = ", self.nbar
        print "n  = ", self.n
        print "Tpi = ", self.Tpi
        print "gamma   = ", self.gamma

if __name__ == '__main__':
    # load the data
#    t, x1, x2 = numpy.loadtxt("C:\\Users\\cqt\\Desktop\\testfit.dat", unpack=True, delimiter=",")
    t, x1, x2 = numpy.loadtxt("test.dat", unpack=True, delimiter=",")

    print t, x1
    
    f = ThermalFit()
    f.set_data(t, x1)
    f.set_params(1.0, 7.0, 8, 10.0, 10.0)
    f.fit()
    f.print_all()

    # show is necessary to display the plot when
    # not in interactive mode
    #pylab.show()
    
    #app = QtGui.QApplication(sys.argv)
    #myapp = anticrossing_fit_gui()
    #myapp.show()

    #sys.exit(app.exec_())