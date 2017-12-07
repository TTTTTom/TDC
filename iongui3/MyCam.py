import sys
from PyQt4 import QtCore, QtGui
from CamGUI import Ui_Cam
import MMCorePy
#import matplotlib.pyplot as plt
import numpy
import pickle

DEVICE=['Camera-1','PrincetonInstruments','Camera-1']
#DEVICE=['Camera','DemoCamera','DCam']
STATES = ['Open', 'Camera', 'PMT']

# Main widget
class MyCam(QtGui.QDialog):
    def __init__(self, parent=None):
        self.mmc=MMCorePy.CMMCore()
        print "__init__ is called"
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Cam()
        self.ui.setupUi(self)
        self.active = False
        self.mmc.enableDebugLog(False)
        self.mmc.enableStderrLog(False)
        print self.mmc.getVersionInfo()
        print self.mmc.getAPIVersionInfo()
        #self.mmc.loadDevice('Camera-1','PrincetonInstruments','Camera-1')
        self.mmc.loadDevice(*DEVICE)
        self.mmc.initializeAllDevices()
        self.mmc.setCameraDevice(DEVICE[0])
        #self.mmc.setCameraDevice('Camera-1')
        rawImage=numpy.array([list(range(512)) for i in range(512)])
        self.intensity = 0
        #print "data", rawImage, "type", type(rawImage), "shape", rawImage.shape
        #testimg = QtGui.QPixmap("tux.png")
        self.myQImg = QtGui.QImage(512, 512, QtGui.QImage.Format_RGB32)
        for x in xrange(512):
            for y in xrange(512):
                self.myQImg.setPixel(x, y, QtGui.qRgb(rawImage[x][y], rawImage[x][y], rawImage[x][y]))

        pix = QtGui.QPixmap.fromImage(self.myQImg)
        myPixMap=QtGui.QPixmap(pix)
        #print "Pixmap", myPixMap.size()
        self.ui.image.setPixmap(myPixMap)
        self.ui.image.show()
        #plt.imshow(img,cmap='gray')
        #plt.show()

        QtCore.QObject.connect(self.ui.startButton,    QtCore.SIGNAL('clicked()'), self.slot_start_clicked)
        QtCore.QObject.connect(self.ui.applyROIButton,    QtCore.SIGNAL('clicked()'), self.slot_update_ROI)
        #QtCore.QObject.connect(self.ui.xspinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_ROI)
        #QtCore.QObject.connect(self.ui.yspinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_ROI)
        #QtCore.QObject.connect(self.ui.xSizespinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_ROI)
        #QtCore.QObject.connect(self.ui.ySizespinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_ROI)
        QtCore.QObject.connect(self.ui.showPOIButton,    QtCore.SIGNAL('pressed()'), self.slot_update_ROI)
        QtCore.QObject.connect(self.ui.showPOIButton,    QtCore.SIGNAL('released()'), self.slot_update_ROI)
        #QtCore.QObject.connect(self.ui.POIxspinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_POI)
        #QtCore.QObject.connect(self.ui.POIyspinBox,    QtCore.SIGNAL('valueChanged(int)'), self.slot_update_POI)
        self.timer = QtCore.QTimer(self)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"), self.check_for_new_image)
        self.connect(self.ui.exposurespinBox, QtCore.SIGNAL('valueChanged(int)'), self.slot_update_exposure)
        QtCore.QObject.connect(self.ui.cameraButton,    QtCore.SIGNAL('clicked()'), self.slot_camera_clicked)
        QtCore.QObject.connect(self.ui.PMTButton,    QtCore.SIGNAL('clicked()'), self.slot_PMT_clicked)
        QtCore.QObject.connect(self.ui.propertycomboBox,    QtCore.SIGNAL('currentIndexChanged(int)'), self.slot_prop_changed)
        QtCore.QObject.connect(self.ui.ResetButton,    QtCore.SIGNAL('clicked()'), self.slot_reset_clicked)

        self.mmc.setProperty(DEVICE[0], 'Port', 'LowNoise')
        #self.mmc.setProperty(DEVICE[0], 'TriggerMode', 'ExternalFirst')
        self.cam_props = self.getProperties(DEVICE[0])
        self.ui.propertycomboBox.addItems(self.cam_props.keys())

        self.ROI_state = STATES[0]

        try:
            self.load_state()
        except:
            print "Could not load previous state"
            self.params = {'PMT': {'ROI': [201, 257, 30, 30], 'POI': [216, 271]}, 'Camera': {'ROI': [210, 283, 30, 30], 'POI': [224, 297]}}

        self.slot_update_ROI()

    # saves parameters to file
    def save_state(self):
        with open('cam_params.dat', 'w') as f:
            pickle.dump(self.params, f)
        f.closed

    # loads parameters from file
    def load_state(self):
        with open('cam_params.dat', 'r') as f:
            self.params = pickle.load(f)
        f.closed

    def slot_prop_changed(self, *args):
        self.ui.propertylabel.setText(self.cam_props[str(self.ui.propertycomboBox.currentText())])
        print self.mmc.getAllowedPropertyValues(DEVICE[0], str(self.ui.propertycomboBox.currentText()))

    def getProperties(self, camera):
        cam_props = self.mmc.getDevicePropertyNames(camera)
        prop_dict = {}
        for i in range(len(cam_props)):
            this_prop = cam_props[i];
            val = self.mmc.getProperty(camera, this_prop);
            prop_dict[str(this_prop)] = str(val)
            #print "Name: " + prop + ", value: " + val
        return prop_dict

    def slot_camera_clicked(self):
        self.ROI_state = STATES[1]
        values = self.params[STATES[1]]
        self.ui.xspinBox.setValue(values['ROI'][0])
        self.ui.yspinBox.setValue(values['ROI'][1])
        self.ui.xSizespinBox.setValue(values['ROI'][2])
        self.ui.ySizespinBox.setValue(values['ROI'][3])
        self.ui.POIxspinBox.setValue(values['POI'][0])
        self.ui.POIyspinBox.setValue(values['POI'][1])
        self.slot_update_ROI()

    def slot_reset_clicked(self):
        self.ROI_state = STATES[0]
        self.ui.xspinBox.setValue(0)
        self.ui.yspinBox.setValue(0)
        self.ui.xSizespinBox.setValue(512)
        self.ui.ySizespinBox.setValue(512)
        self.ui.POIxspinBox.setValue(255)
        self.ui.POIyspinBox.setValue(255)
        self.slot_update_ROI()

    def slot_PMT_clicked(self):
        self.ROI_state = STATES[2]
        values = self.params[STATES[2]]
        self.ui.xspinBox.setValue(values['ROI'][0])
        self.ui.yspinBox.setValue(values['ROI'][1])
        self.ui.xSizespinBox.setValue(values['ROI'][2])
        self.ui.ySizespinBox.setValue(values['ROI'][3])
        self.ui.POIxspinBox.setValue(values['POI'][0])
        self.ui.POIyspinBox.setValue(values['POI'][1])
        self.slot_update_ROI()

    def slot_update_exposure(self, exp_time):
        self.mmc.setExposure(exp_time)
        print "Exposure: ", self.mmc.getProperty(DEVICE[0], "Exposure")
        if self.active:
            self.timer.start(exp_time)

    def slot_update_ROI(self, *args):
        #self.xscaled = self.linearScale512(self.ui.xspinBox.value(), self.ui.xSizespinBox.value())
        #self.yscaled = self.linearScale512(self.ui.yspinBox.value(), self.ui.ySizespinBox.value())
        self.xscaledCut = self.linearScale512(0, self.ui.xSizespinBox.value())
        self.yscaledCut = self.linearScale512(0, self.ui.ySizespinBox.value())
        if self.ROI_state == STATES[1]:
            self.params[STATES[1]]['ROI'] = [self.ui.xspinBox.value(), self.ui.yspinBox.value(), self.ui.xSizespinBox.value(), self.ui.ySizespinBox.value()]
            self.params[STATES[1]]['POI'] = [self.ui.POIxspinBox.value(), self.ui.POIyspinBox.value()]
        elif self.ROI_state == STATES[2]:
            self.params[STATES[2]]['ROI'] = [self.ui.xspinBox.value(), self.ui.yspinBox.value(), self.ui.xSizespinBox.value(), self.ui.ySizespinBox.value()]
            self.params[STATES[2]]['POI'] = [self.ui.POIxspinBox.value(), self.ui.POIyspinBox.value()]
        self.save_state()
        #print "xlimits", self.xscaled(0), self.xscaled(512)
        self.printImage()
        #print 'params', self.params

    def slot_start_clicked(self):
        self.active = not self.active
        if self.active:
            self.ui.startButton.setText("Stop")
            self.mmc.startContinuousSequenceAcquisition(1)
            #print "Exposure1: ", self.mmc.getProperty("Camera-1", "Exposure")
            print "exposure spin box", self.ui.exposurespinBox.value()
            self.slot_update_exposure(self.ui.exposurespinBox.value())
            #self.mmc.snapImage()
            #img = self.mmc.getImage()
        else:
            self.ui.startButton.setText("Start")
            self.timer.stop()
            self.mmc.stopSequenceAcquisition()
            #self.mmc.reset()

    def check_for_new_image(self):
        #if self.mmc.getRemainingImageCount() > 0:
        #    self.last_image = self.mmc.getLastImage()
        #    self.printImage()
        #else:
        #    print('No frame')
        self.last_image = self.mmc.getLastImage()
        # print "shape", self.last_image.shape
        self.printImage()

    def linearScale512(self, x0, xs):
        def f(x):
            return int(x0 + x * xs/512.0)
            # This is the inverse: return 512*(x-x0)/xs
        return f

    def printImage(self):
        try:
            #rawImage= self.last_image # in format uint16
            rawImage = numpy.int32(self.last_image)
        except:
            print "Could not find last image"
            rawImage=numpy.array([list(range(512)) for i in range(512)])/2 + 500
        cutImage = rawImage[self.ui.xspinBox.value():(self.ui.xspinBox.value()+self.ui.xSizespinBox.value()),self.ui.yspinBox.value():(self.ui.yspinBox.value()+self.ui.ySizespinBox.value())]
        cutImageShape = cutImage.shape
        #print "cutimage", cutImage
        mymin = min(cutImage.min(axis=1))
        myrange = max(cutImage.max(axis=1)) - mymin
        #mymin = min(rawImage.min(axis=1))
        #myrange = max(rawImage.max(axis=1)) - mymin
        scaledImage = ((rawImage - mymin)*255)/myrange
        scaledCutImage = ((cutImage - mymin)*255)/myrange
        #print "scaledcut", scaledCutImage
        #for x in xrange(512): # This method is waaaay to slow, remove this by using scaledCutImage
        #    for y in xrange(512):
        #        if scaledImage[x,y]<0:
        #            scaledImage[x,y]=0
        #print 'max', max(rawImage.max(axis=1)) ,max(scaledImage.max(axis=1)), "should be", ((max(rawImage.max(axis=1)) - mymin)*255)/(myrange)
        #print 'min' , mymin, min(scaledImage.min(axis=1))
        #print "data", rawImage, "type", type(rawImage), "shape", rawImage.shape
        #testing = QtGui.QPixmap("tux.png")
        #self.myQImg = QtGui.QImage(512, 512, QtGui.QImage.Format_RGB32)
        self.myQImg = QtGui.QImage(512, 512, QtGui.QImage.Format_RGB16)
        #scaled_x = [self.xscaled(x) for x in range(512)]
        #scaled_y = [self.yscaled(x) for x in range(512)]
        scaledCut_x = [self.xscaledCut(x) for x in range(512)]
        scaledCut_y = [self.yscaledCut(x) for x in range(512)]
        #print "scaled cut x", [(x,self.xscaledCut(x)) for x in range(512)]
        for x in xrange(512): # This method is waaaay to slow. It is to "zoom-in"
            for y in xrange(512):
        #for x in xrange(self.ui.xspinBox.value(), min(self.ui.xSizespinBox.value() + self.ui.xspinBox.value(),512)):
        #    for y in xrange(self.ui.yspinBox.value(), min(self.ui.ySizespinBox.value() + self.ui.yspinBox.value(),512)):
                #if scaledCut_x[x] < self.ui.xSizespinBox.value() and scaledCut_y[y] < self.ui.ySizespinBox.value(): #What is this for? assert?
                if self.ui.showPOIButton.isDown() and scaledCut_x[x]+self.ui.xspinBox.value() == self.ui.POIxspinBox.value()-1 and scaledCut_y[y]+self.ui.yspinBox.value() == self.ui.POIyspinBox.value()-1:
                    self.myQImg.setPixel(x, y, QtGui.qRgb(255,0,0))
                else:
                    #print "indices", self.xscaled(x), self.yscaled(y)
                    if scaledCut_x[x] < cutImageShape[0] and scaledCut_y[y] < cutImageShape[1]:
                    #try:
                        mylist = [scaledCutImage[scaledCut_x[x]][scaledCut_y[y]]]*3
                    else:
                    #except IndexError:
                        #print "indices", scaledCut_x[x], ',', scaledCut_y[y]
                        #print "cut image", scaledCutImage
                        print "scaledCut_x[x] < cutImageShape[0]", scaledCut_x[x] ,cutImageShape[0]
                        self.myQImg.setPixel(x, y, QtGui.qRgb(0,255,0))
                    self.myQImg.setPixel(x, y, QtGui.qRgb(*mylist))
                #else:
                #    self.myQImg.setPixel(x, y, QtGui.qRgb(0,255,0))

        #for x in xrange(512): # This method is waaaay to slow. It is to "zoom-in"
        #    for y in xrange(512):
        ##for x in xrange(self.ui.xspinBox.value(), min(self.ui.xSizespinBox.value() + self.ui.xspinBox.value(),512)):
        ##    for y in xrange(self.ui.yspinBox.value(), min(self.ui.ySizespinBox.value() + self.ui.yspinBox.value(),512)):
        #        if scaled_x[x] < 512 and scaled_y[y] < 512:
        #            if self.ui.showPOIButton.isDown() and scaled_x[x] == self.ui.POIxspinBox.value() and scaled_y[y] == self.ui.POIyspinBox.value():
        #                self.myQImg.setPixel(x, y, QtGui.qRgb(255,0,0))
        #            else:
        #                #print "indices", self.xscaled(x), self.yscaled(y)
        #                mylist = [scaledImage[scaled_x[x]][scaled_y[y]]]*3
        #                #mylist = [rawImage[scaled_x[x]][scaled_y[y]]]*3
        #                self.myQImg.setPixel(x, y, QtGui.qRgb(*mylist))

        pix = QtGui.QPixmap.fromImage(self.myQImg)
        myPixMap=QtGui.QPixmap(pix)
        #print "Pixmap", myPixMap.size()  # To test if the picture was loaded
        self.ui.image.setPixmap(myPixMap)
        self.ui.image.show()
        self.intensity = rawImage[self.ui.POIxspinBox.value()-1][self.ui.POIyspinBox.value()-1]
        self.ui.intensityLabel.setText('Intensity: ' + str(self.intensity))
        #plt.imshow(img,cmap='gray')
        #plt.show()

    def get_intensity(self):
        return self.intensity


# execute this if we started this file
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyCam()
    myapp.show()

    sys.exit(app.exec_())