# -*- coding:utf-8 -*-
"""
Created on Jul 5, 2011

@author: Dima
"""
from usb_ftdi import ftdi_usb
from PyQt4 import QtCore, QtGui
import time, sys
import pickle
import csv
import struct

class TDCAction():
    START, STOP, PAUSE, RESUME = range(4)
    

def frange(start, stop=None, step=None):
    list = []
    if stop is None:
        stop = float(start)
        start = 0.0
    if step is None:
        step = 1.0
    cur = float(start)
    while cur < stop:
        list.append(cur)
        cur += step
    return list

# Calibration error class
class CalibrationError():
    def __init__(self):
        pass

class event():
    def __init__(self, valid, coarse, finestart, finestop, parstart, parstop, filter_coarse, filter_finestop, parcoarsefilter):
        self.valid     = valid;
        self.coarse    = coarse;
        self.finestart = finestart;
        self.finestop  = finestop;
        self.parstart  = parstart;
        self.parstop = parstop;
        self.filter_coarse = filter_coarse;
        self.filter_finestop = filter_finestop;
        self.parcoarsefilter = parcoarsefilter

    def show(self):
        print "Coarse time, ns: ", 5.0 * self.coarse, "fine start time: ", self.finestart, "fine stop time: ",  self.finestop
        print "Coarse start parity: ", self.parstart, "Coarse stop parity:  ", self.parstop

# some defines
IDLE, CALIBRATE, ACQUIRE, PAUSE = range(4) 

# To save event delay data to file
class event_saver():
    def __init__(self):
        self.filename = ""
        self.file = None
                
    def open(self, fname):
        self.filename = fname
        try:
            self.file = open(fname, 'ab') # Append data, in binary mode
        except:
            print "Can't open file for timestamps"
            file = None
        
    def write(self, delay):
        if (self.file != None):
            self.file.write(struct.pack('d', delay))
        
    def close(self):
        if (self.file != None):
            self.file.close()
        self.file = None
        

class tdc_parser(QtCore.QObject):
    def __init__(self, tdcname = "CQT FPGA Board A"):
        QtCore.QObject.__init__(self)
        super(tdc_parser, self).__init__(self) 

        # Constants for the TDC board
        self.clock    = 5.0 # 200 MHz clock, 5.0 ns clock cycle
        self.finesize = 128 # Size of the fine calibration array
        self.calibration_fname = 'calibration.dat'


        # Hardware initialisation
        self.tdcdev = ftdi_usb(baud = 3000000)
        self.tdcdev.config()
        self.tdcdev.open(tdcname)
        self.data = ''
        self.state = IDLE
        
        # histogram for data
        self.xhist      = [] # intervals
        self.yhist      = [] # values
        self.histmin    = 0
        self.histmax    = 1
        self.histstep   = 1
        self.histevents = 0

        # Histrograms for calibration
        self.hcoarse    = {}
        self.hstart     = [0] * self.finesize # Array full of zeroes 
        self.hstop      = [0] * self.finesize # Array full of zeroes
        self.hpstart    = [0] * self.finesize # Calibrated delays for fine start
        self.hpstop     = [0] * self.finesize # Calibratied delays for fine stops
        self.ncalevents = 100000
        self.nevents    = 0

        # Calibration data
        self.calibrated = False
        self.cstart     = [0] * self.finesize # Calibrated delays for fine start
        self.cstop      = [0] * self.finesize # Calibratied delays for fine stops
        self.cstartofst = 0 # Start offset for fine histogram
        self.cstopofst  = 0 # stop offset for fine histogram

        # Indicates that we should save events to a file
        self.event_saver = event_saver()

        # try to load calibration data
        self.load_calibration(self.calibration_fname)

        # connect signals and slots
        QtCore.QObject.connect(self.tdcdev.read_thread, QtCore.SIGNAL('data_ready(QByteArray)'), self.read_slot)
        

    def get(self):
        return self.yhist

    def get_avg(self):
        return self.yhist

    def getx(self):
        return self.xhist

    def read(self):
        buf = self.tdcdev.read()
        
        
    def close(self):
        self.tdcdev.close()
        
        
    def read_slot(self, buf):
        # print "buffer:", ':'.join(x.encode('hex') for x in buf)
        # print len(buf), "bytes read"
        self.parse(buf)
        
    def process_data(self, ev):
        if (self.calibrated == False):
            return
        
        delay = self.event_delay(ev)
        index = int((delay - self.histmin)/self.histstep)
        if index < 0:
            print "Data skipped because index", index ,"is negative"
        else:
            try:
                self.yhist[index] += 1
                self.histevents   += 1
                self.emit(QtCore.SIGNAL('NewEvent()'))
            except:
                print "Delay ", delay, " is out of range, index = ", index
        
        if (self.histevents % 500 == 0) and (self.histevents > 0):
            print self.histevents, "events processed"
            # print "Current event: delay = ", delay
            # print "Current event: index = ", index
            ev.show()
            print "cstart ", self.cstart[int(ev.finestart)], "cstop ", self.cstop[int(ev.finestop)]
            self.emit(QtCore.SIGNAL('tdc_data_ready()'))
            
        self.event_saver.write(delay) # Write delay event to a file
        
    # process event in calibration mode
    def process_calibration(self, ev):
#        try:
#            self.hcoarse[ev.coarse] += 1
#        except KeyError:
#            self.hcoarse[ev.coarse] = 1
        
        # Add events to histograms
        self.hstart[ev.finestart] += 1
        self.hstop[ev.finestop]   += 1
        if (ev.parstart):
            self.hpstart[ev.finestart]   += 1
        if (ev.parstop):
            self.hpstop[ev.finestop] += 1
        self.nevents += 1
        
        if (self.nevents % 5000 == 0):
            self.emit(QtCore.SIGNAL('calibration_data_ready()'))
            print self.nevents, " events processed "

        if (self.nevents > self.ncalevents):
            self.state = IDLE
            print "hstart", self.hstart
            print "hpstart", self.hpstart
            print "hstop", self.hstop
            print "hpstop", self.hpstop
            self.make_calibration()
    
    # Returns delay for an event.
    def event_delay(self, ev):
        if (self.calibrated == False):
            raise CalibrationError()

        delay = (ev.coarse * self.clock - self.cstart[ev.finestart] + self.cstop[ev.finestop])
        # delay = (ev.coarse * self.clock - ev.finestart + ev.finestop)
       # delay = ( ev.coarse * self.clock + self.cstart[ev.finestart]
#                  - self.cstop[ev.finestop] ) 
        return delay
        
    def set_csetup(self, start, stop):
        self.cstartofst = start
        self.cstopofst  = stop
        
        
    # generate calibration arrays from histrogram and save them 
    def make_calibration(self):
        curstart = 0.0
        curstop  = 0.0

#        startofst = 0
#        stopofst  = 0

#        for i in xrange(self.finesize):
#            if ( (self.hstart[i] > 20) & (self.hpstart[i] < 0.5 * self.hstart[i]) ):
#                self.cstartofst = i
#                break

#        for i in xrange(self.finesize):
#            if ( (self.hstop[i] > 20)  & (self.hpstop[i] < 0.5 * self.hstop[i]) ):
#                self.cstopofst = i
#                break



#        for (i=1; i<DifferentialChannels  && StartHistogram[i]>0 && StartParityHistogram[i]<0.5*StartHistogram[i]; ++i);
#        StartOffset = i;
        
#        for i in range(self.)
        
#        for (i=1; i<DifferentialChannels && StopHistogram[i]>0  && StopParityHistogram[i]<0.5*StopHistogram[i]; ++i);
#        StopOffset = i;
        
        for i in range(0, self.finesize):
            curstart += self.hstart[(i + self.cstartofst) % self.finesize]
            curstop  += self.hstop[(i + self.cstartofst) % self.finesize]            
            self.cstart[(i + self.cstartofst) % self.finesize] = self.clock * curstart / self.nevents 
            self.cstop[(i + self.cstopofst) % self.finesize]   = self.clock * curstop  / self.nevents     
                 
        self.save_calibration(self.calibration_fname)
        self.calibrated = True
        self.emit(QtCore.SIGNAL('calibration_data_ready()'))
        print "start offset: ", self.cstartofst, "start offset: ", self.cstopofst
        
        
    # save calibration to file
    def save_calibration(self, fname):
        with open(fname, mode='w') as f:
            pickle.dump([self.cstart, self.cstop], f)
            print "calibration saved"
            print "cstart: ", self.cstart
            print "cstop:  ", self.cstop


    # load calibration from file 
    def load_calibration(self, fname):
        try:
            with open(fname) as f:
                [self.cstart, self.cstop] = pickle.load(f)
                self.calibrated = True
        except IOError:
            print "Calibration file ", fname, " not found" 

    def savehist(self, f_name):
        with open(f_name, mode='w') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerows(zip(self.xhist, self.yhist))
        pass

    # switches between acsquire and idle modes
    def toggle_mode(self, reset, min, max, step):
        if (self.state == IDLE):
            self.ascuire(reset, min, max, step)
        elif(self.state == ACQUIRE):
            self.idle()
            
    # switch to a different mode
    def switch_mode(self, action, min, max, step):
        if (action == TDCAction.START):
            self.ascuire(True, min, max, step)
        elif (action == TDCAction.STOP):
            self.idle()
        elif (action == TDCAction.PAUSE):
            self.pause()
        elif (action == TDCAction.RESUME):
            self.resume()
            
    # switch to calibration mode:
    # accumulate data and run calibration procedure        
    def calibrate(self, npoints):
        self.state = CALIBRATE
        
        # Initialise calibration histograms ...
        self.hcoarse    = {}
        self.hstart     = [0] * self.finesize # Array full of zeroes 
        self.hstop      = [0] * self.finesize # Array full of zeroes
        self.hpstart    = [0] * self.finesize # Calibrated delays for fine start
        self.hpstop     = [0] * self.finesize # Calibrated delays for fine stops
        self.ncalevents = npoints
        self.nevents    = 0

        # and calibration data
        self.calibrated = False
        self.cstart     = [0] * self.finesize # Calibrated delays for fine start
        self.cstop      = [0] * self.finesize # Calibrated delays for fine stops

    # Switch to measurement mode:
    # Ascuire data and build a histogram
    # reset = True : erase previous data
    # update_interval: send data update signal every X ms if we have new data
    def ascuire(self, reset, min, max, step):
        if (reset):
            self.xhist = frange(min, max, step)
            self.yhist = [0] * len(self.xhist)
            self.histmin    = min
            self.histmax    = max
            self.histstep   = step
            self.histevents = 0
            print "New measurement, min = ", min, " max = ", max, " step = ", step
        self.state = ACQUIRE
        print self.xhist
        print self.yhist
        
    # Resumes the measurements
    def resume(self):
        self.state = ACQUIRE

    
    # Switch to idle state, ignore all the data
    def idle(self):
        if (self.state == ACQUIRE):
            self.emit(QtCore.SIGNAL('tdc_data_ready()'))
        elif(self.state == CALIBRATE):
            self.emit(QtCore.SIGNAL('calibration_data_ready()'))
        self.event_saver.close()
        self.state = IDLE

    # Switch to idle state, ignore all the data
    def pause(self):
        if (self.state == ACQUIRE):
            self.emit(QtCore.SIGNAL('tdc_data_ready()'))
        elif(self.state == CALIBRATE):
            self.emit(QtCore.SIGNAL('calibration_data_ready()'))
        self.state = PAUSE

    # parse data that we got from USB
    def parse(self, buf):
        # Do nothing if we are in the IDLE state
        if (self.state == IDLE or self.state == PAUSE):
            return
        # print "buffer:", ':'.join(x.encode('hex') for x in buf)
        self.data += buf
        ptr = 0
        datalen = len(self.data)
        # print "current buffer length is", len(self.data)
        while (datalen - ptr > 13):
            # print "Processing byte ", ptr
            event = self.parse_event(bytearray(self.data[ ptr : ptr + 13 ]));
            if (event.valid):
                if (self.state == CALIBRATE):
                    self.process_calibration(event)
                elif (self.state == ACQUIRE):
                    self.process_data(event) 
                ptr += 13
            else:
                ptr += 1
                
        self.data = self.data[ptr:]
        #event.show()

    def parse_event(self, buf):
        lbuf = len(buf)
        print "current data:", ':'.join(x.encode('hex') for x in str(buf))
        if (lbuf == 13):
            finestart = buf[0] & 0x7F;
            # print "fine start:", chr(finestart).encode('hex')
            finestop  = buf[1] & 0x7F;
            # print "fine stop:", chr(finestop).encode('hex')
            parstart  = (buf[0] & 0x80) >> 7;
            # print "parity start:", chr(parstart).encode('hex')
            parstop   = (buf[1] & 0x80) >> 7;
            # print "parity stop:", chr(parstop).encode('hex')
            checksum  = buf[2];
            # print "checksum:", chr(checksum).encode('hex')
            coarse    = buf[3]*0x1000000 + buf[4]*0x10000 + buf[5]*0x100 +  buf[6]
            # print "coarse", ':'.join(x.encode('hex') for x in str(buf[3:7]))

            filter_finestop = buf[7] & 0x7F;
            parcoarsefilter = (buf[7] & 0x80) >> 7;
            filter_checksum = buf[8];
            filter_coarse = buf[9] * 0x1000000 + buf[10] * 0x10000 + buf[11] * 0x100 + buf[12]
            # print "filter coarse", ':'.join(x.encode('hex') for x in str(buf[9:13]))
            
            if (checksum & 0x0F != 0x0F):
                print "Checksum error", chr(checksum).encode('hex'), "does not end in F"
                evvalid = False
            elif(self.parityOf(finestop)  != ((checksum & 0x20) >> 5)):
                print "Fine stop error : finestop = ", finestop, "Parity = ", \
                self.parityOf(finestop), "Checksum = ", ((checksum & 0x20) >> 5)
                evvalid = False
            elif(self.parityOf(finestart) != ((checksum & 0x40) >> 6)):
                print "Fine start error : finestart = ", finestart, "Parity = ", \
                self.parityOf(finestart), "Checksum = ", ((checksum & 0x40) >> 6)
                evvalid = False
            elif(self.parityOf(coarse)    != ((checksum & 0x80) >> 7)):
                print "Coarse error"
                evvalid = False
            elif (filter_checksum & 0x3F != 0x3F):
                print "Filter checksum error", chr(filter_checksum).encode('hex'), "does not end in 3F"
                evvalid = False
            elif (self.parityOf(filter_finestop) != ((filter_checksum & 0x40) >> 6)):
                print "Filter stop error : filter_finestop = ", filter_finestop, "Parity = ", \
                    self.parityOf(filter_finestop), "Checksum = ", ((filter_checksum & 0x40) >> 6)
                evvalid = False
            elif (self.parityOf(filter_coarse) != ((filter_checksum & 0x80) >> 7)):
                print "Filter coarse error"
                evvalid = False
            else:
                evvalid = True   
                
            ev = event(evvalid, coarse, finestart, finestop, parstart, parstop, filter_coarse, filter_finestop, parcoarsefilter)
            # ev.show()
            # print "Checksum", bin(checksum)
            return ev
        else:
            print "Error: lenght of buffer is ", lbuf, " instead of 13"
            return event(False, 0, 0, 0, 0, 0, 0, 0)
        
    # Magic parity function
    def parityOf(self, int_type):
        parity = 0
        while (int_type):
            parity = ~parity
            int_type = int_type & (int_type - 1)
        if (parity == 0):
            return 0
        else:
            return 1

# main function to test USB module
def main():
    app = QtGui.QApplication(sys.argv)
    tdc = tdc_parser()
    tdc.read()
    tdc.calibrate(500000)
    print "waiting for data ..."
    sys.exit(app.exec_())
    tdc.close()        

if __name__ == "__main__":
    main()