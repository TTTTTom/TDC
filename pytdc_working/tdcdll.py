'''
Created on 01-Jun-2011

@author: cqt
'''

import ctypes

# Wrapper class for the Peters DLL function
class libTDC():
    def __init__(self):
        self.tdc = ctypes.windll.LoadLibrary('libtdc_dll.dll')
       
    
    def close(self):
        func = self.tdc.__getitem__("tdc_close@0")
        return func()


# Open the named TDC USB device.
    def open(self, name):
        func = self.tdc.__getitem__("tdc_open@4")
        cname = ctypes.c_char_p(name)
        return func(cname)
    

#  calibrate the carry chains of the TDC connect any signal that is NOT
#  synchronized to the TDC clock. The number of samples are taken and the
#  relative delay of the carry chain is determined.
#
#  This function blocks until the calibration is completed. 
    def calibrate(self, samples):
        func = self.tdc.__getitem__("tdc_calibrate@4")
        csamples = ctypes.c_uint(samples)
        return func(csamples)
    
#
#   Integrate the Start-Stop measurement. The measurement times are binned
#   in the given binwidth and the maximum correlation time. The integration is stopped
#   after samples samples are taken.
# 
#   This function blocks until the Integration is complete.
    def integrate(self, binwidth, correlationtime, samples ):
        func = self.tdc.__getitem__("tdc_integrate@20")
        cbinwidth        = ctypes.c_double(binwidth)
        ccorrelationtime = ctypes.c_double(correlationtime)
        csamples         = ctypes.c_uint(samples)
        return func(cbinwidth, ccorrelationtime, csamples)

#
#  DLL function gets the interated histogram. A pointer to the histogram is returned in buffer
#  and the number of samples is returned in size. The pointer is valid until the
#  next call to getHistogram or the unload of the dll
    def getHistogram(self, buffer):
        size = self.getHistogramSize()
        func = self.tdc.__getitem__("tdc_getHistogram@8")
        cbuffer     = ctypes.c_double(buffer)
        csize       = ctypes.c_uint(size)
        return func(cbuffer, csize)

# Returns histrogram size
    def getHistogramSize(self):
        func   = self.tdc.__getitem__("tdc_getHistogramSize@4")
        csize  = ctypes.c_uint()
        pcsize = ctypes.pointer(csize)
        res = func(pcsize)
        return pcsize.contents.value

#  record a bare histogram
    def recordHistogram(self, samples):
        func   = self.tdc.__getitem__("tdc_recordHistogram@4")
        csamples  = ctypes.c_uint(samples)
        return func(csamples)

#
# Start the integration. The data is binned with the provided binwidth and maximum
# correlation time. The integration stops after the given number of samples is reached.
# The function starts the integration in a new thread and returns immediately.
    def startIntegration(self, binwidth, correlationtime, samples):
        func = self.tdc.__getitem__("tdc_startIntegration@20")
        cbinwidth        = ctypes.c_double(binwidth)
        ccorrelationtime = ctypes.c_double(correlationtime)
        csamples         = ctypes.c_uint(samples)
        return func(cbinwidth, ccorrelationtime, csamples)

    def resumeIntegration(self, samples):
        func = self.tdc.__getitem__("tdc_resumeIntegration@4")
        csamples         = ctypes.c_uint(samples)
        return func(csamples)

# Stops a running integration.
    def stopIntegration(self):
        func = self.tdc.__getitem__("tdc_stopIntegration@0")
        return func()

#  Returns the currently taken number of samples.
    def getSamples(self):
        func = self.tdc.__getitem__("tdc_getSamples@4")
        csamples  = ctypes.c_uint()
        pcsamples = ctypes.pointer(csamples)
        res = func(pcsamples)
        return pcsamples.contents.value

    def getOutOfRangeEvents(self):
        func = self.tdc.__getitem__("tdc_getSamples@4")
        cevents  = ctypes.c_uint()
        pcevents = ctypes.pointer(cevents)
        res = func(pcevents)
        return pcevents.contents.value


# Get the current integration time in seconds.
    def getIntegrationTime(self):
        func = self.tdc.__getitem__("tdc_getIntegrationTime@4")
        ctime  = ctypes.c_uint()
        pctime = ctypes.pointer(ctime)
        res = func(pctime)
        return pctime.contents.value
        

# Get total integration time in seconds.
    def getTotalIntegrationTime(self):
        func = self.tdc.__getitem__("tdc_getTotalIntegrationTime@4")
        ctime  = ctypes.c_uint()
        pctime = ctypes.pointer(ctime)
        res = func(pctime)
        return pctime.contents.value
        
# Get the current Stop rate in counts/second.
    def getCoincidenceRate(self):
        func = self.tdc.__getitem__("tdc_getCoincidenceRate@4")
        crate  = ctypes.c_double()
        pcrate = ctypes.pointer(crate)
        res = func(pcrate)
        return pcrate.contents.value
        

# Start the calibration. This function returns immediately.
    def startCalibration(self, samples=100000):
        func   = self.tdc.__getitem__("tdc_startCalibration@4")
        csamples  = ctypes.c_uint(samples)
        return func(csamples)

# returns true if data is being taken
    def busy(self):
        func = self.tdc.__getitem__("tdc_busy@4")
        cbusy  = ctypes.c_uint()
        pcbusy = ctypes.pointer(cbusy)
        res = func(pcbusy)
        if (pcbusy.contents.value == 0):
            return False
        else:
            return True

#  Wait the given number of milliseconds for the completion.
#  The function returns after the given time. It returns true
#  if the measurement is finished.
    def waitForCompletion(self, duration):
        func = self.tdc.__getitem__("tdc_waitForCompletion@8")
        cduration   = ctypes.c_uint(duration)
        ccompleted  = ctypes.c_uint()
        pccompleted = ctypes.pointer(ccompleted)
        res = func(cduration, pccompleted)
        if (pccompleted.contents.value == 0):
            return False
        else:
            return True
        
# Get the status message. The returned pointer is valid until
# the next call to this function.
    def getStatusMessage(self, size = 256):
        func   = self.tdc.__getitem__("tdc_getStatusMessage@8")
        buffer = ctypes.create_string_buffer(size)
        res = func(buffer, size)
        return buffer.str()
        
    def getErrorMessage(self, size = 256):
        func   = self.tdc.__getitem__("tdc_getErrorMessage@8")
        buffer = ctypes.create_string_buffer(size)
        res = func(buffer, size)
        return buffer.str()

    def saveCalibrationText(self):
        func = self.tdc.__getitem__("tdc_saveCalibrationText@0")
        return func()
    
    def saveHistogram(self, fname):
        func   = self.tdc.__getitem__("tdc_saveHistogram@4")
        cfname = ctypes.c_char_p(fname)
        return func(cfname)
 
 
    def loadHistogram(self, fname):
        func   = self.tdc.__getitem__("tdc_loadHistogram@4")
        cfname = ctypes.c_char_p(fname)
        return func(cfname)

    def saveHistogramText(self, fname):
        func   = self.tdc.__getitem__("tdc_saveHistogramText@4")
        cfname = ctypes.c_char_p(fname)
        return func(cfname)


if __name__ == "__main__":
    tdc = libTDC()
    print tdc.open("FPGA")
    print tdc.getHistogramSize()
    print tdc.getTotalIntegrationTime()
#    print tdc.calibrate(10000)
    print tdc.close()
    
