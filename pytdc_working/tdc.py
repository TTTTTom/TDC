# -*- coding:utf-8 -*-
"""
Created on Jul 10, 2011

@author: Dima
"""

import sys
sys.path.append('../')

from PyQt4 import Qt
from PyQt4 import QtCore, QtGui
from PyQt4 import Qwt5
from pytdc_gui import Ui_TDCWindow
from tdcreader import tdc_parser, TDCAction
from fit import sine_fit_gui
from micromotion import DACWindow

# Some defines, consistent with tdcreader
IDLE, CALIBRATE, ACQUIRE, PAUSE = range(4)


class TDCWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        print "TDC called"
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_TDCWindow()
        self.ui.setupUi(self)

        self.tdc = tdc_parser()
        self.tdc.read()
        QtCore.QObject.connect(self.ui.refreshRateBox, QtCore.SIGNAL('valueChanged(int)'), self.refresh_slot)
        
        self.hstartline = Qwt5.QwtPlotCurve("A")
        self.hpstartline = Qwt5.QwtPlotCurve("C")
        self.hpstartline.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Ellipse,
                                   Qt.QBrush(Qt.Qt.blue),
                                   Qt.QPen(Qt.Qt.red),
                                   Qt.QSize(3, 3)))
        self.hpstartline.setPen(Qt.QPen(Qt.Qt.red))

        self.hstartline.attach(self.ui.fine_start_plot)
        self.hpstartline.attach(self.ui.fine_start_plot)
      
        self.hstopline = Qwt5.QwtPlotCurve("B")
        self.hpstopline = Qwt5.QwtPlotCurve("D")
        self.hpstopline.setSymbol(Qwt5.QwtSymbol(Qwt5.QwtSymbol.Ellipse,
                                  Qt.QBrush(Qt.Qt.blue),
                                  Qt.QPen(Qt.Qt.red),
                                  Qt.QSize(3, 3)))
        self.hpstopline.setPen(Qt.QPen(Qt.Qt.red))
        self.hstopline.attach(self.ui.fine_stop_plot)          
        self.hpstopline.attach(self.ui.fine_stop_plot)          

        self.histline = Qwt5.QwtPlotCurve("Histogram")
        self.histline.attach(self.ui.hist_plot)

        # Fit plot
        self.plotfit = Qwt5.QwtPlotCurve("Fit")
        self.plotfit.setStyle(Qwt5.QwtPlotCurve.Lines)
        self.plotfit.setPen(Qt.QPen(Qt.Qt.red))
        self.plotfit.attach(self.ui.hist_plot)
        self.fit_curve = sine_fit_gui(self.ui.hist_plot, self.plotfit, self.tdc)

        # DAC
        self.micromotion = DACWindow()

#        self.picker = Qwt5.QwtPlotPicker(Qwt5.QwtPlot.xBottom, Qwt5.QwtPlot.yLeft,
#                                         Qwt5.QwtPicker.PointSelection | Qwt5.QwtPicker.DragSelection,
#                                         Qwt5.QwtPlotPicker.VLineRubberBand,
#                                         Qwt5.QwtPicker.AlwaysOn,
#                                         self.ui.hist_plot.canvas())
#        self.picker.setTrackerMode(Qwt5.QwtPicker.AlwaysOn)
#        self.picker.setTrackerPen(Qt.QPen(Qt.Qt.red))

#        self.zoomer = Qwt5.QwtPlotZoomer(Qwt5.QwtPlot.xBottom,
#                                         Qwt5.QwtPlot.yLeft,
#                                         Qwt5.QwtPicker.DragSelection,
#                                         Qwt5.QwtPicker.AlwaysOff,
#                                         self.ui.hist_plot.canvas())
#        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

#        self.marker = Qwt5.QwtPlotMarker()
#        self.marker.setLineStyle(Qwt5.QwtPlotMarker.VLine | Qwt5.QwtPlotMarker.HLine)
#        self.marker.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
#        self.marker.setLinePen(QtGui.QPen(QtCore.Qt.darkGray, 1, QtCore.Qt.DashLine))
#        self.marker.setValue(0.0, 0.0)
#        self.marker.attach(self.ui.hist_plot)

        self.grid = Qwt5.QwtPlotGrid()
        self.grid.attach(self.ui.hist_plot)
        self.grid.setPen(Qt.QPen(Qt.Qt.black, 0, Qt.Qt.DotLine))

#        self.ui.hist_plot.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
    # signal / slot connection
        QtCore.QObject.connect(self.ui.calibrateButton, QtCore.SIGNAL('clicked()'), self.calibrate_slot) 
        QtCore.QObject.connect(self.ui.startButton, QtCore.SIGNAL('clicked()'), self.run_slot) 
        QtCore.QObject.connect(self.ui.saveButton,  QtCore.SIGNAL('clicked()'), self.save_slot) 
        QtCore.QObject.connect(self.ui.csetButton,  QtCore.SIGNAL('clicked()'), self.cset_slot) 
        QtCore.QObject.connect(self.ui.pauseButton,  QtCore.SIGNAL('clicked()'), self.pause_slot)
        QtCore.QObject.connect(self.ui.filenameButton,  QtCore.SIGNAL('clicked()'), self.filename_slot) 
        QtCore.QObject.connect(self.ui.save_stampsBox,  QtCore.SIGNAL('stateChanged (int)'), self.save_stamps_slot) 
        QtCore.QObject.connect(self.ui.actionFit,  QtCore.SIGNAL('triggered()'), self.fit_slot)
        QtCore.QObject.connect(self.ui.actionDAC,  QtCore.SIGNAL('triggered()'), self.dac_slot)

        
        QtCore.QObject.connect(self.tdc,  QtCore.SIGNAL('calibration_data_ready()'), self.plot_calibration)
        QtCore.QObject.connect(self.tdc,  QtCore.SIGNAL('tdc_data_ready()'), self.plot_histogram)
        QtCore.QObject.connect(self.tdc,  QtCore.SIGNAL('NewEvent()'), self.new_event)

        
        # update status text
        self.plot_status()

    def new_event(self):
        if self.micromotion.to_optimize:        # skip whole loop if there is nothing to do, so the program runs faster
            # If enough points, jump to set rod voltages
            if self.micromotion.points < self.micromotion.ui.numberPoints.value():
                if self.micromotion.new_point:      # Reset histogram
                    self.tdc.ascuire(True, self.ui.startSpinBox.value(), self.ui.stopSpinBox.value(),
                                     self.ui.stepSpinBox.value())
                    self.micromotion.new_point = False
                if self.tdc.histevents == self.micromotion.ui.countSpinBox.value():     # enough events to fit
                    self.fit_curve.slot_fit_clicked()     # Sine Fit and data building
                    fit_params = self.fit_curve.fit.get_params()
                    if self.micromotion.ui.FixVDiffMMMM.isChecked():
                        self.micromotion.volt_axis.add(self.micromotion.volt_sum)
                        self.micromotion.ui.ch0SpinBox.setValue(self.micromotion.dac.v[0]+self.micromotion.step)
                        self.micromotion.ui.ch1SpinBox.setValue(self.micromotion.dac.v[1]+self.micromotion.step)
                    elif self.micromotion.ui.FixVSumMMMM.isChecked():
                        self.micromotion.volt_axis.add(self.micromotion.volt_diff)
                        self.micromotion.ui.ch0SpinBox.setValue(self.micromotion.dac.v[0]+self.micromotion.step)
                        self.micromotion.ui.ch1SpinBox.setValue(self.micromotion.dac.v[1]-self.micromotion.step)
                    self.micromotion.amplitude_data.add(fit_params[1])
                    try:
                        phases = [fit_params[2] - 360, fit_params[2], fit_params[2] + 360]
                        last_phase = self.micromotion.phase_data.get(-1)
                        awayness = [abs(x - last_phase) for x in phases]
                        min_awayness = awayness.index(min(awayness))
                        self.micromotion.phase_data.add(phases[min_awayness])
                    except IndexError:
                        self.micromotion.phase_data.add(fit_params[2])
                    self.micromotion.make_plots(self.micromotion.volt_axis.getall(),
                                                self.micromotion.amplitude_data.getall(),
                                                self.micromotion.phase_data.getall(),
                                                "V_diff (V)", "Amplitude (Counts)", "Phase (Degrees)")
                    self.micromotion.points += 1
                    self.micromotion.new_point = True       # First event of a new point is next
            else:
                self.micromotion.to_optimize = False
                ideal_value = self.micromotion.volt_axis.getall()[self.micromotion.amplitude_data.getall().index(min(self.micromotion.amplitude_data.getall()))]        # Index of minimum value in amplitude is used to address the ideal voltage value
                if self.micromotion.ui.FixVDiffMMMM.isChecked():
                    fix_value = self.micromotion.volt_diff
                    self.micromotion.ui.ch0SpinBox.setValue((ideal_value + fix_value)/2)
                    self.micromotion.ui.ch1SpinBox.setValue((ideal_value - fix_value)/2)
                elif self.micromotion.ui.FixVSumMMMM.isChecked():
                    fix_value = self.micromotion.volt_sum
                    self.micromotion.ui.ch0SpinBox.setValue((fix_value + ideal_value)/2)
                    self.micromotion.ui.ch1SpinBox.setValue((fix_value - ideal_value)/2)
                self.micromotion.ui.NoMMMM.click()

    # slot for calibrate button
    def calibrate_slot(self):
        n_event = self.ui.neventsBox.value()
        if n_event > 0:
            self.tdc.calibrate(n_event)
            
        self.plot_calibration()

    # Shows the fit dialog to fit the data with the sine wave
    def fit_slot(self):
        self.fit_curve.show()

    def refresh_slot(self, value):
        self.tdc.refresh = value


    # Shows the dialog to fix the rod voltages to minimize micromotion
    def dac_slot(self):
        self.micromotion.show()

    # save delay histogram to a file
    def save_slot(self):
        # Open file and save the data
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        if ( filename == '' ) :
            return
        self.tdc.savehist(filename)
        self.plot_status()

    # Choose file name for time stamp file
    def filename_slot(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Open file', '~')
        if ( filename == '' ):
            return
        self.ui.filenameEdit.setText(filename)

    # save timestamps box was checked or unchecked
    def save_stamps_slot(self, state):
        if self.ui.save_stampsBox.isChecked():
            pass
        else:
            pass
        
    # plot calibration   
    def run_slot(self):
        if (self.tdc.state == IDLE):
            self.tdc.switch_mode(TDCAction.START,
                                 self.ui.startSpinBox.value(),
                                 self.ui.stopSpinBox.value(),
                                 self.ui.stepSpinBox.value())
            if (self.ui.save_stampsBox.isChecked()): # Save events to file
                self.tdc.event_saver.open(self.ui.filenameEdit.text())
        else:
            self.tdc.switch_mode(TDCAction.STOP,
                                 self.ui.startSpinBox.value(),
                                 self.ui.stopSpinBox.value(),
                                 self.ui.stepSpinBox.value())  
        self.plot_status()

    # 
    def cset_slot(self):
        self.tdc.set_csetup(self.ui.cstartBox.value(), self.ui.cstopBox.value())

    # pause the data collection        
    def pause_slot(self):
        if self.tdc.state == ACQUIRE:  # We should resume for now
            self.tdc.pause()
        elif self.tdc.state == PAUSE:  # stop data collection for now
            self.tdc.resume()
            
        self.plot_status()
 
    # plot calibration            
    def plot_calibration(self):
        x = range(0, len(self.tdc.hstart))       
        self.hstartline.setData(x,  self.tdc.hstart)
        self.hpstartline.setData(x, self.tdc.hpstart)
        
        self.hstopline.setData(x,  self.tdc.hstop)
        self.hpstopline.setData(x, self.tdc.hpstop)
        
        self.ui.fine_start_plot.replot()        
        self.ui.fine_stop_plot.replot() 
        self.plot_status()         

    # plot histogram
    def plot_histogram(self):
        self.histline.setData(self.tdc.xhist, self.tdc.yhist)
        # x_slice = self.fit_curve.get_xslice()
        # y_slice = self.fit_curve.get_yslice()
        # self.histline.setData(x_slice, y_slice)
        self.ui.hist_plot.replot()
        self.plot_status()        
       
    # updates the status text
    def plot_status(self):
        if self.tdc.state == IDLE:
            self.txtlabel = "TDC is idle"
            self.ui.startButton.setText("Start")
            self.ui.pauseButton.setText("Pause")
            self.ui.pauseButton.setChecked(False)    
            self.ui.calibrateButton.setText("Calibrate")            
        elif self.tdc.state == CALIBRATE:
            self.txtlabel = "TDC is calibrating, "
            self.txtlabel += str(self.tdc.nevents)
            self.txtlabel += " events processed, "
            self.ui.startButton.setText("Start")
            self.ui.pauseButton.setText("Pause")
            self.ui.pauseButton.setChecked(False)
            self.ui.calibrateButton.setText("Calibrating ... ")            
        elif self.tdc.state == ACQUIRE:
            self.txtlabel = "TDC is collecting data"
            self.ui.startButton.setText("Stop")
            self.ui.pauseButton.setText("Pause")
            self.ui.pauseButton.setChecked(False)    
            self.ui.calibrateButton.setText("Calibrate")
        elif self.tdc.state == PAUSE:
            self.txtlabel = "Data collection is paused ... "
            self.ui.startButton.setText("Stop")
            self.ui.pauseButton.setText("Resume")
            self.ui.pauseButton.setChecked(True)


        if self.tdc.calibrated == False:
            self.txtlabel += ", Device is not calibrated"
            
        # if self.tdc.tdcdev.handle == None:
        #     self.txtlabel += ", Can not connect to TDC via USB, device not found"
            
        self.ui.status_label.setText(self.txtlabel)
  

# main function to test GUI
def main():
    app = QtGui.QApplication(sys.argv)
    
    tdc_win = TDCWindow()
    tdc_win.show()
    
    # Traditional signals, things are messy here
#    QtCore.QObject.connect(ionmain.simple_scan, QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
#    QtCore.QObject.connect(ionmain.freq_scan,   QtCore.SIGNAL("scanSimpleRequest"), ionseq.run_slot)
#    QtCore.QObject.connect(ionmain.delay_scan,  QtCore.SIGNAL("scanDelayRequest"),  ionseq.scan_delay_slot)
#    QtCore.QObject.connect(ionseq           ,   QtCore.SIGNAL("scanLineChanged"),   ionmain.delay_scan.scan_line_slot)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

