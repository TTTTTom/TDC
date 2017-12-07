import sys
import os
# import random
import numpy as np
from CamGUI_mpl_mainwin import Ui_Cam_mainwin
from PyQt4 import QtGui, QtCore
import pickle
# from numpy import arange, sin, pi
# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.gridspec as gridspec
# import matplotlib

import MMCorePy
# import matplotlib.pyplot as plt

import time

# from Gauss_fit_ui import Ui_Gauss_Fit_Dialog

# from scipy import optimize

from functools import wraps

from TroubleshootingCAM import Ui_Help

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

DEVICE = ['Camera-1', 'PrincetonInstruments', 'Camera-1']


# class GaussFit(QtCore.QObject):
#     def __init__(self):
#         QtCore.QObject.__init__(self)
#
#         self.a = 100
#         self.x0 = 10
#         self.y0 = 10
#         self.sigmax = 2
#         self.sigmay = 2
#
#         self.inten = []
#
#     # Pass experimental data fo the fit
#     def set_data(self, inten):
#         self.inten = inten
#
#     # run the fitting program
#     def fit(self, inten):
#         # self.a = sum(self.y) / float(len(self.y))
#         # self.b = max(self.y) - min(self.y)
#         self.set_data(inten)
#         inten_x = np.sum(self.inten, axis=0)
#         [a, x0, sigmax], flag = \
#             optimize.leastsq(gauss_fit_error, [self.a, self.x0, self.sigmax],
#                              args=(inten_x))
#
#         inten_y = np.sum(self.inten, axis=0)
#         [y0, sigmay], flag = \
#             optimize.leastsq(gauss_fit_error_no_a, [self.y0, self.sigmay],
#                              args=(inten_y, a))
#
#         self.set_params(a, x0, sigmax, y0, sigmay)
#
#     # set parameters for the fit, recalculate the function for display
#     def set_params(self, a, x0, y0, sigmax, sigmay):
#         self.a = a
#         self.x0 = x0
#         self.y0 = y0
#         self.sigmax = sigmax
#         self.sigmay = sigmay
#
#     def get_params(self):
#         return [self.a, self.x0, self.y0, self.sigmax, self.sigmay]
#
#     # def func(self, x):
#     #     return sin_func(x, self.a, self.x0, self.y0, self.sigmax, self.sigmay)
#
#     # def function_data(self, xlist):
#     #     return [self.func(x) for x in xlist]
#
#     def print_all(self):
#         print "Parameters: "
#         print "a          = ", self.a
#         print "x0         = ", self.x0
#         print "y0         = ", self.y0
#         print "sigmax     = ", self.sigmax
#         print "sigmay     = ", self.sigmay
#
# # Sin fit function
# def gauss_func(x, a, x0, sigmax, y0, sigmay):
#     return a*np.exp(-(x-x0)**2/(2*sigmax**2))*np.exp(-(y-y0)**2/(2*sigmay**2))
#
# # Difference between fit and experimental data
# def gauss_fit_error(params, x):
#     a, x0, sigmax = params
#     return y - gauss_func(x, a, x0, sigmax)
#
# def gauss_fit_error_no_a(params, y, x, freq):
#     a, x0, sigmax, y0, sigmay = params
#     return y - gauss_func(x, a, x0, sigmax, y0, sigmay)
#
# class gauss_fit_gui(QtGui.QDialog):
#     def __init__(self, parent=None):
#         print "__init__ is called"
#         QtGui.QDialog.__init__(self, parent)
#         self.ui = Ui_Gauss_Fit_Dialog()
#         self.ui.setupUi(self)
#
#         self.GaussFit = GaussFit()
#         self.datax = []
#         self.datay = []
#
#         QtCore.QObject.connect(self.ui.aSpinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_parameter_changed)
#         QtCore.QObject.connect(self.ui.x0SpinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_parameter_changed)
#         QtCore.QObject.connect(self.ui.y0SpinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_parameter_changed)
#         QtCore.QObject.connect(self.ui.sigmaxSpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
#         QtCore.QObject.connect(self.ui.sigmaySpinBox, QtCore.SIGNAL('valueChanged(double)'), self.slot_parameter_changed)
#         QtCore.QObject.connect(self.ui.fitButton, QtCore.SIGNAL('clicked()'), self.slot_fit_clicked)
#         # QtCore.QObject.connect(self.ui.doneButton, QtCore.SIGNAL('clicked()'), self.slot_done_clicked)
#
#         # self.update_display()
#
#     #     try:
#     #         self.load_freq()
#     #     except:
#     #         self.ui.fSpinBox.setValue(30.178)
#     #
#     # def save_freq(self):
#     #     with open('gauss_fit.dat', 'w') as f:
#     #         pickle.dump(self.ui.fSpinBox.value(), f)
#     #     f.closed
#     #
#     # def load_freq(self):
#     #     with open('gauss_fit.dat', 'r') as f:
#     #         self.ui.fSpinBox.setValue(pickle.load(f))
#     #     f.closed
#
#     def set_data(self, datax, datay):
#         self.datax = datax
#         self.datay = datay
#
#     def slot_parameter_changed(self, value):
#         self.GaussFit.set_params(self.ui.aSpinBox.value(),
#                             self.ui.x0SpinBox.value(),
#                             self.ui.y0SpinBox.value(),
#                             self.ui.sigmaxSpinBox.value(),
#                             self.ui.sigmaySpinBox.value())
#         self.GaussFit.print_all()
#         # self.update_plot()
#         # self.save_freq()
#
#     def slot_fit_clicked(self, datax, datay):
#         # x = self.scandata.getx()
#         # yavg = self.scandata.get_avg()
#         # xslice = []
#         # yslice = []
#         # for idx, val in enumerate(x):
#         #     if (val >= self.xmin and val <= self.xmax):
#         #         xslice.append(val)
#         #         yslice.append(yavg[idx])
#         self.set_data(datax, datay)
#         self.GaussFit.set_data(np.array(self.datax), np.array(self.datay))
#         self.fit_data()
#
#         # Display result
#         # self.update_display()
#         # self.update_plot()
#
#     # def get_xslice(self):
#     #     x = self.scandata.getx()
#     #     xslice = []
#     #     for idx, val in enumerate(x):
#     #         if (val >= self.xmin and val <= self.xmax):
#     #             xslice.append(val)
#     #     return xslice
#
#     # def get_yslice(self):
#     #     x = self.scandata.getx()
#     #     yavg = self.scandata.get_avg()
#     #     yslice = []
#     #     for idx, val in enumerate(x):
#     #         if (val >= self.xmin and val <= self.xmax):
#     #             yslice.append(yavg[idx])
#     #     return yslice
#
#     # def slot_done_clicked(self):
#     #     self.plotline.setData([], [])
#     #     self.plot.replot()
#     #
#     # def update_display(self):
#     #     [a, b, phi, freq] = self.fit.get_params()
#     #     self.ui.aSpinBox.setValue(a)
#     #     self.ui.bSpinBox.setValue(b)
#     #     self.ui.PhiSpinBox.setValue(phi)
#     #     self.ui.fSpinBox.setValue(freq)
#     #
#     # run a fit program,
#     def fit_data(self):
#         self.GaussFit.fit()
#         self.GaussFit.print_all()
#     #
#     # # redraws fit line
#     # def update_plot(self):
#     #     try:
#     #         xsmall = np.linspace(self.xmin, self.xmax, 400)
#     #         y = self.fit.function_data(xsmall)
#     #         self.plotline.setData(xsmall, y)
#     #         self.plot.replot()
#     #     except IndexError:
#     #         pass

class help_gui(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui_help = Ui_Help()
        self.ui_help.setupUi(self)

def timing_function(some_function):
    """Outputs the time a function takes to execute."""
    @wraps(some_function)
    def wrapper(*args, **kwargs):
        # print "args", args, "kwargs", kwargs
        t1 = time.time()
        some_function(*args, **kwargs)
        # output = some_function(*args, **kwargs)
        # print "output", str(output) + "\n"
        # time.sleep(1)
        t2 = time.time()
        print "It took " + str((t2-t1)) + " s to run the function " + some_function.__name__ + "\n"
        return "Return Time it took to run the function " + some_function.__name__ + " is " + str((t2-t1)) + "\n"
    return wrapper

class MyCam(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Cam_mainwin()
        self.ui.setupUi(self)

        self.help_ui = help_gui()

        self.mmc = MMCorePy.CMMCore()
        # self.mmc.enableDebugLog(True)
        # self.mmc.enableStderrLog(False)
        # print self.mmc.getVersionInfo()
        # print self.mmc.getAPIVersionInfo()
        # self.mmc.loadDevice(*DEVICE)
        # self.mmc.initializeAllDevices()
        # self.mmc.setCameraDevice(DEVICE[0])
        # # self.mmc.setProperty(DEVICE[0], 'Port', 'EM')
        # self.mmc.setProperty(DEVICE[0], 'Port', 'LowNoise')
        # self.mmc.setProperty(DEVICE[0], 'ReadoutRate', '0MHz 16bit')
        #
        # self.cam_props = self.getProperties(DEVICE[0])
        # self.ui.propertycomboBox.addItems(self.cam_props.keys())

        self.slot_resetCAM_clicked()

        QtCore.QObject.connect(self.ui.startButton, QtCore.SIGNAL('clicked()'), self.slot_start_clicked)
        self.connect(self.ui.exposurespinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_update_exposure)
        QtCore.QObject.connect(self.ui.propertycomboBox, QtCore.SIGNAL('currentIndexChanged(int)'),
                               self.slot_prop_changed)
        QtCore.QObject.connect(self.ui.applyROIButton, QtCore.SIGNAL('clicked()'), self.slot_update_ROI)
        QtCore.QObject.connect(self.ui.fullROIButton,    QtCore.SIGNAL('clicked()'), self.slot_resetROI_clicked)
        QtCore.QObject.connect(self.ui.cameraButton, QtCore.SIGNAL('clicked()'), self.slot_camera_clicked)
        QtCore.QObject.connect(self.ui.PMTButton, QtCore.SIGNAL('clicked()'), self.slot_PMT_clicked)
        QtCore.QObject.connect(self.ui.snapButton, QtCore.SIGNAL('clicked()'), self.slot_snap_clicked)
        QtCore.QObject.connect(self.ui.actionGaussian, QtCore.SIGNAL("triggered()"), self.gauss_fit_slot)
        QtCore.QObject.connect(self.ui.ROR_Large_radioButton, QtCore.SIGNAL('clicked()'), self.slot_ROR_clicked)
        QtCore.QObject.connect(self.ui.ROR_Low_radioButton, QtCore.SIGNAL('clicked()'), self.slot_ROR_clicked)
        QtCore.QObject.connect(self.ui.ROR_Med_radioButton, QtCore.SIGNAL('clicked()'), self.slot_ROR_clicked)
        QtCore.QObject.connect(self.ui.showPOIButton, QtCore.SIGNAL('stateChanged(int)'), self.slot_update_POI)
        QtCore.QObject.connect(self.ui.POIxspinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_update_POI)
        QtCore.QObject.connect(self.ui.POIyspinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_update_POI)
        QtCore.QObject.connect(self.ui.resetCamButton, QtCore.SIGNAL('clicked()'), self.slot_resetCAM_clicked)
        QtCore.QObject.connect(self.ui.actionPrint_Help, QtCore.SIGNAL("triggered()"), self.print_help)


        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_for_figure)

        # self.delaytimer = QtCore.QTimer(self)
        # self.delaytimer.setSingleShot(True)
        # self.delaytimer.timeout.connect(self.start_timer)

        # self.gauss_fit_ui = gauss_fit_gui()

        self.exposure = self.ui.exposurespinBox.value()
        self.mmc.setExposure(self.exposure)

        self.ROI_state = 'Full'

        self.intensity = 0

        try:
            self.load_state()
        except:
            print "Could not load previous state"
            self.params = {'PMT': {'ROI': [201, 257, 40, 40], 'POI': [216, 271]},
                           'Camera': {'ROI': [210, 283, 40, 40], 'POI': [224, 297]}}

        self.frame = np.zeros((512, 512))

    def print_help(self):
        self.help_ui.show()
        # if self.ui.startButton.text() == "Stop":
        #     self.ui.startButton.setText("Start")
        #     self.timer.stop()
        #     self.mmc.stopSequenceAcquisition()  # The only reason to stop is to keep fix the text in the console window. Otherwise a recurring error that could show up will disturb the reading of the help.
        # print "For 'Waiting for new frame' at 0.1 MHz Readout Rate in Continuous Acquisition, reduce ROI"
        # print "For no new frame after you changed the ROI, set xsize AND ysize to be multiples of 4 and apply. In some regions of the camera the minimum xsize and ysize might be bigger than 20"
        # print "For Unknown or Memory Errors: Reset camera"
        # print "If problem persists, restart involved programs and devices systematically"
        # print "If issue persists, work with the old version mainwin_2 and use WinXTest. WinXTest does not seem to acquire data right after having run this program (WTF?!), try again after a restart of the computer"
        # print "If nothing works, bang your head against the Stop and Think sign, then call Roland or someone that knows the MM Library"

    def slot_update_POI(self, *args):
        if self.ui.startButton.text() == "Start":
            # print "frame", self.frame
            self.draw_frame(self.frame)

    def get_intensity(self):
        return self.intensity

    def slot_camera_clicked(self):
        self.ROI_state = 'Camera'
        values = self.params['Camera']
        self.ui.xspinBox.setValue(values['ROI'][0])
        self.ui.yspinBox.setValue(values['ROI'][1])
        self.ui.xSizespinBox.setValue(values['ROI'][2])
        self.ui.ySizespinBox.setValue(values['ROI'][3])
        self.ui.POIxspinBox.setValue(values['POI'][0])
        self.ui.POIyspinBox.setValue(values['POI'][1])
        self.slot_update_ROI()

    def slot_PMT_clicked(self):
        self.ROI_state = 'PMT'
        values = self.params['PMT']
        self.ui.xspinBox.setValue(values['ROI'][0])
        self.ui.yspinBox.setValue(values['ROI'][1])
        self.ui.xSizespinBox.setValue(values['ROI'][2])
        self.ui.ySizespinBox.setValue(values['ROI'][3])
        self.ui.POIxspinBox.setValue(values['POI'][0])
        self.ui.POIyspinBox.setValue(values['POI'][1])
        self.slot_update_ROI()

    def save_state(self):
        with open('cam_params_2.dat', 'w') as f:
            pickle.dump(self.params, f)

    def load_state(self):
        with open('cam_params_2.dat', 'r') as f:
            self.params = pickle.load(f)

    def pause_cam(my_func):
        @wraps(my_func)
        def wrapper(self, *args):
            if self.ui.startButton.text() == "Stop":
                self.ui.startButton.setText("Start")    # Just in case the decorated function calls another function that was also decorated by this pause_cam, like resetCAM
                self.timer.stop()
                self.mmc.stopSequenceAcquisition()
                my_func(self, *args)
                self.mmc.startContinuousSequenceAcquisition(self.exposure)
                self.ui.startButton.setText("Stop")
                # self.delaytimer.start(5*self.exposure)
                self.timer.start(self.exposure)
            else:
                my_func(self, *args)
        return wrapper

    # def start_timer(self):
    #     self.timer.start(self.exposure)

    @pause_cam
    def slot_resetCAM_clicked(self):
        if 'Camera-1' in self.mmc.getLoadedDevices():
            print 'Camera-1 reset'
            self.mmc.reset()
        self.mmc.loadDevice(*DEVICE)
        self.mmc.initializeAllDevices()
        self.mmc.setCameraDevice(DEVICE[0])
        self.mmc.setProperty(DEVICE[0], 'Port', 'LowNoise')
        self.update_ROR()
        self.reset_ROI()        # The reset command already resets the ROI. This line is to reflect the new (full) range in the GUI.
        print "ROI was reset"
        print "Devices", self.mmc.getLoadedDevices()
        self.cam_props = self.getProperties(DEVICE[0])
        self.ui.propertycomboBox.addItems(self.cam_props.keys())

    def update_ROR(self):   # ReadOut Rate
        if self.ui.ROR_Med_radioButton.isChecked():
            self.mmc.setProperty(DEVICE[0], 'ReadoutRate', '1MHz 16bit')
        elif self.ui.ROR_Low_radioButton.isChecked():
            self.mmc.setProperty(DEVICE[0], 'ReadoutRate', '0MHz 16bit')
        else:
            self.mmc.setProperty(DEVICE[0], 'ReadoutRate', '5MHz 16bit')

    @pause_cam
    def slot_ROR_clicked(self):
        self.update_ROR()

    # @timing_function
    @pause_cam
    def slot_snap_clicked(self):
        if not(self.exposure == self.ui.exposurespinBox.value()):
            self.mmc.setExposure(self.exposure)
        self.mmc.snapImage()
        self.frame = self.mmc.getImage()
        # print "frame", frame.shape
        # if self.ui.showPOIButton.isChecked():
        #     POI_frame = np.zeros((frame.shape[0], frame.shape[1]))
        #     POI_frame[[self.ui.POIxspinBox.value()], [
        #         self.ui.POIyspinBox.value()]] = 127  # Position relative to the frame, not the camera array
        #     self.ui.mplwidget.axes.imshow(POI_frame + frame, interpolation='nearest')
        # else:
        #     self.ui.mplwidget.axes.imshow(frame, interpolation='nearest')
        # self.ui.mplwidget.draw()
        # self.intensity = frame[[self.ui.POIxspinBox.value()], [self.ui.POIyspinBox.value()]]
        # self.ui.intensityLabel.setText('Intensity: ' + str(self.intensity))
        self.draw_frame(self.frame)

    def slot_start_clicked(self):
        if self.ui.startButton.text() == "Start":
            self.ui.startButton.setText("Stop")
            self.mmc.startContinuousSequenceAcquisition(self.exposure)
            self.timer.start(self.ui.exposurespinBox.value())
        else:
            self.ui.startButton.setText("Start")
            self.timer.stop()
            self.mmc.stopSequenceAcquisition()

    def gauss_fit_slot(self):
        QtGui.QMessageBox.about(self, "Go Fit Yo Mama!", "Fitting code is not ready yet...")
    #     self.gauss_fit_ui.show()

    def reset_ROI(self):
        self.ROI_state = 'Full'
        self.mmc.clearROI()
        self.ui.xspinBox.setValue(0)
        self.ui.yspinBox.setValue(0)
        self.ui.xSizespinBox.setValue(512)
        self.ui.ySizespinBox.setValue(512)
        self.ui.POIxspinBox.setMaximum(self.ui.xSizespinBox.value() - 1)
        self.ui.POIyspinBox.setMaximum(self.ui.ySizespinBox.value() - 1)

    @pause_cam
    def slot_resetROI_clicked(self):
        self.reset_ROI()

    @pause_cam
    def slot_update_exposure(self, exp_time):
        self.exposure = exp_time
        self.mmc.setExposure(self.exposure)

    @pause_cam
    def slot_update_ROI(self, *args):
        if not(self.ui.xSizespinBox.value() % 4 == 0 and self.ui.ySizespinBox.value() % 4 == 0):
            print "Camera might not like your image size. Please make it multiple of 4."
        self.mmc.setROI(self.ui.xspinBox.value(), self.ui.yspinBox.value(), self.ui.xSizespinBox.value(), self.ui.ySizespinBox.value())
        if self.ROI_state == 'Camera':
            self.params['Camera']['ROI'] = [self.ui.xspinBox.value(), self.ui.yspinBox.value(),
                                             self.ui.xSizespinBox.value(), self.ui.ySizespinBox.value()]
            self.params['Camera']['POI'] = [self.ui.POIxspinBox.value(), self.ui.POIyspinBox.value()]
        elif self.ROI_state == 'PMT':
            self.params['PMT']['ROI'] = [self.ui.xspinBox.value(), self.ui.yspinBox.value(),
                                             self.ui.xSizespinBox.value(), self.ui.ySizespinBox.value()]
            self.params['PMT']['POI'] = [self.ui.POIxspinBox.value(), self.ui.POIyspinBox.value()]
        self.save_state()
        self.ui.POIxspinBox.setMaximum(self.ui.xSizespinBox.value() - 1)
        self.ui.POIyspinBox.setMaximum(self.ui.ySizespinBox.value() - 1)

    # @timing_function
    def check_for_figure(self):
        try:
            self.mmc.waitForDevice(DEVICE[0])
            if self.mmc.getRemainingImageCount() > 0:
                self.frame = self.mmc.getLastImage()
                # print "frame", frame.shape
                self.draw_frame(self.frame)
                # if self.ui.showPOIButton.isChecked():
                #     POI_frame = np.zeros((frame.shape[0], frame.shape[1]))
                #     POI_frame[[self.ui.POIxspinBox.value()], [self.ui.POIyspinBox.value()]] = 127  # Position relative to the frame, not the camera array
                #     self.ui.mplwidget.axes.imshow(POI_frame+frame, interpolation='nearest')
                # else:
                #     self.ui.mplwidget.axes.imshow(frame, interpolation='nearest')
                # self.ui.mplwidget.draw()
                # self.intensity = frame[[self.ui.POIxspinBox.value()], [self.ui.POIyspinBox.value()]]
                # self.ui.intensityLabel.setText('Intensity: ' + str(self.intensity))
            else:
                print "Waiting for new frame"
        except:
            print "Could not find last frame"
            self.frame = np.array([list(range(512)) for i in range(512)]) / 2 + 500
            self.draw_frame(self.frame)
            # self.ui.mplwidget.axes.imshow(frame)
            # self.ui.mplwidget.draw()
            # self.intensity = frame[[self.ui.POIxspinBox.value()], [self.ui.POIyspinBox.value()]]
            # self.ui.intensityLabel.setText('Intensity: ' + str(self.intensity))

    def draw_frame(self, frame):
        self.intensity = frame[[self.ui.POIyspinBox.value()], [self.ui.POIxspinBox.value()]]
        self.ui.intensityLabel.setText('Intensity: ' + str(self.intensity))
        if self.ui.showPOIButton.isChecked():
            POI_frame = np.zeros((frame.shape[0], frame.shape[1]))
            POI_frame[[self.ui.POIyspinBox.value()], [self.ui.POIxspinBox.value()]] = 511  # Position relative to the frame, not the camera array
            self.ui.mplwidget.axes.imshow(POI_frame + frame, interpolation='nearest')
        else:
            self.ui.mplwidget.axes.imshow(frame, interpolation='nearest')
        self.ui.mplwidget.draw()

    def getProperties(self, camera):
        cam_props = self.mmc.getDevicePropertyNames(camera)
        prop_dict = {}
        for i in range(len(cam_props)):
            this_prop = cam_props[i]
            val = self.mmc.getProperty(camera, this_prop)
            prop_dict[str(this_prop)] = str(val)
        return prop_dict

    def slot_prop_changed(self, *args):
        print "args", args
        self.ui.propertylabel.setText(self.cam_props[str(self.ui.propertycomboBox.currentText())])
        print "Possible values: ", self.mmc.getAllowedPropertyValues(DEVICE[0], str(self.ui.propertycomboBox.currentText()))
        print "Is read-only?: ", self.mmc.isPropertyReadOnly(DEVICE[0], str(self.ui.propertycomboBox.currentText()))
        if self.mmc.hasPropertyLimits(DEVICE[0], str(self.ui.propertycomboBox.currentText())):
            print "Lower limit ", self.mmc.getPropertyLowerLimit(DEVICE[0], str(self.ui.propertycomboBox.currentText()))
            print "Upper limit ", self.mmc.getPropertyUpperLimit(DEVICE[0], str(self.ui.propertycomboBox.currentText()))

    def closeEvent(self, ce):
        self.mmc.stopSequenceAcquisition()
        self.close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyCam()
    myapp.show()

    sys.exit(app.exec_())