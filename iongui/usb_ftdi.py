# import the PyUSB module
import ftd2xx as d2xx
import time
from PyQt4 import QtCore
import threading

ftdi_thread_lock = threading.Lock()

# Includes ftdi USB interfacs
class ftdi_usb():
    def __init__(self, baud = 115200):
        self.baud   = baud
        self.name   = ""
        self.dev_list  = d2xx.listDevices(d2xx.defines.OPEN_BY_DESCRIPTION)
        self.data = ''
        self.read_thread = QtCore.QThread()
        print self.dev_list

    # calls USB to Serial configuration dialog
    def config(self):
        print self.dev_list
        return
    
    # opens FTDI USB device by name        
    def open(self, name):
        if (name in self.dev_list):
            ftdi_thread_lock.acquire()
            try:
                self.handle = d2xx.open(self.dev_list.index(name))
            finally:
                ftdi_thread_lock.release()            
        else:
            print name, " Device not found"
            print "Avalible devices: "
            print self.dev_list
            self.handle = None
            return -1
        
        # Sets parameters for serial communications
        ftdi_thread_lock.acquire()
        try:
            self.handle.resetDevice()
            self.handle.setDataCharacteristics(d2xx.BITS_8, d2xx.STOP_BITS_1, d2xx.PARITY_NONE)
            self.handle.setFlowControl(d2xx.FLOW_NONE)
            self.handle.setBaudRate(self.baud)
            self.handle.purge(d2xx.PURGE_RX | d2xx.PURGE_TX)
            self.handle.setDtr()
            self.handle.setRts()
        finally:
            ftdi_thread_lock.release()     
        
        self.read_thread = usb_read_thread(self.handle)
        self.read_thread.begin()
        return 0
        
            
    # reads data from the USB device
    def read(self):
        if (self.handle == None):
            return ""
        ftdi_thread_lock.acquire() 
        try:    
            qlen = self.handle.getQueueStatus()
        finally:
            ftdi_thread_lock.release()       
        if (qlen > 0):
            ftdi_thread_lock.acquire()
            try:                
                data = self.handle.read(qlen)
            finally:
                ftdi_thread_lock.release() 
            return data
        else: 
            return ""
        
    
    # writes data to the usb device
    def write(self, data):
        if (self.handle == None):
            return 0
        ftdi_thread_lock.acquire()
        try:  
            errcode = self.handle.write(data)
        finally:
            ftdi_thread_lock.release() 
        return errcode
    
        
    # closes USB device 
    def close(self):
        if (self.handle != None):
            ftdi_thread_lock.acquire()
            try:
                self.handle.close()
            finally:
                ftdi_thread_lock.release() 
        self.handle = None
    

# Class to read data from USB chip
class usb_read_thread(QtCore.QThread): 
    # constructor
    def __init__(self, handle): 
        QtCore.QThread.__init__(self)
        super(usb_read_thread, self).__init__(self) 
        self.handle = handle


    # Main loop that reads data from FPGA. It terminates on error
    def run(self):
        error = 0 
        while(error == 0):
            time.sleep(0.1)
            ftdi_thread_lock.acquire() 
            try:
                qlen = self.handle.getQueueStatus()
            finally:
                ftdi_thread_lock.release() 
            if (qlen > 0): 
                # print qlen, "bytes read from FPGA"
                self.emit(QtCore.SIGNAL('data_ready(QByteArray)'), self.handle.read(qlen))
            if (qlen < 0):
                print "Error reading data from device, queue status: ", qlen
                error = qlen

    # Dummy function that pyqt needs
    def begin(self): 
        self.start()



# main function to test USB module
def main():
    ftdi = ftdi_usb()
    ftdi.config()
    ftdi.open("FPGA Sequencer A")
    print "wrote", ftdi.write("a"), "bytes"
    time.sleep(1)
    print "wrote", ftdi.write("b"), "bytes"
    time.sleep(1)
    print "wrote", ftdi.write("c"), "bytes"
    time.sleep(1)
    print ftdi.read()
    ftdi.close()
    

if __name__ == "__main__":
    main()

