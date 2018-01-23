# import the PyUSB module
#import ftd2xx as d2xx
import time
from PyQt4 import QtCore
import threading
import socket

# HOST = '192.168.171.51'
HOST = '192.168.101.203'
#HOST = '192.168.101.177'
# PORT = 5555
PORT = 8888

# Includes the interaction over the network
class socket_t():
    def __init__(self, host=HOST, port=PORT):
        self.data = ''
        self.host      = host
        self.port      = port

        self.read_thread = socket_read_thread(self.host, self.port)
        self.read_thread.begin()

    # calls USB to Serial configuration dialog
    def config(self):
        print "Host = ",self.host, "Port = ", self.port
        if self.read_thread.connected:
            print "Connected ... "
        else:
            print "Not connected"
        return
    
    # opens network connection to device by name
    def open(self, host, port):
        self.read_thread = socket_read_thread(host, port)
        self.read_thread.begin()
        
    # closes USB device 
    def close(self):
        self.read_thread.close()

    

# Class to read data from socket
class socket_read_thread(QtCore.QThread): 
    # constructor
    def __init__(self, host, port):
        # input("entering socket read thread init\n")
        QtCore.QThread.__init__(self)
        super(socket_read_thread, self).__init__(self)
        self.host      = host
        self.port      = port
        self.connected = False
        self.socket    = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # opens network connection to device by name
    def open(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
        except:
            print "Can not connect to ", self.host
            self.connected = False
            self.emit(QtCore.SIGNAL('socket_status(QString)'), "Can not connect to counter at " + self.host)
            return -1
        self.emit(QtCore.SIGNAL('socket_status(QString)'), "Connected to " + self.host)
        return 0

    # reads data from the network socket
    def read(self):
        message = self.socket.recv(1024)
        print "read:",message
        return message

    # writes data to the network socket
    def write(self, data):
        errcode = self.socket.send(data)
        if errcode < 0:
            self.connected = False
            self.emit(QtCore.SIGNAL('socket_status(QString)'), "Socket write error to " + self.host)
        return errcode

    # closes USB device
    def close(self):
        self.socket.close()
        self.connected = False
        self.emit(QtCore.SIGNAL('socket_status(QString)'), "Connection to " + self.host + " closed")

    # Main loop that reads data from FPGA. It terminates on error
    def run(self):
        if self.open() < 0:
            return

        buffer=[]
        loopcount=0
        while (True):
            try:
                message=self.socket.recv(1024)
            except:
                self.connected = False
                self.emit(QtCore.SIGNAL('socket_status(QString)'), "Connection to " + self.host + " aborted")
                return

            if len(message)==0:
                continue
            
            self.emit(QtCore.SIGNAL('data_ready(QByteArray)'), message)


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

