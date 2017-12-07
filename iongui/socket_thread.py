# import the PyUSB module
# import d2xx
import time
from PyQt4 import QtCore
import threading
import socket

HOST = '192.168.101.79'
# PORT = 10004
PORT = 5555

ftdi_thread_lock = threading.Lock()

# Includes ftdi USB interfacs
class socket_t():
    def __init__(self):
        # input("entering socket_t init\n")
        self.data = ''
        self.read_thread = QtCore.QThread()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.connect((HOST, PORT))
        self.open(HOST = HOST, PORT = PORT)

    # calls USB to Serial configuration dialog
    def config(self):
        print self.dev_list
        return
    
    # opens FTDI USB device by name        
    def open(self, HOST, PORT):
        
        # if (name in self.dev_list):
        #     ftdi_thread_lock.acquire()
        #     try:
        #         self.handle = d2xx.open(self.dev_list.index(name))
        #     finally:
        #         ftdi_thread_lock.release()            
        # else:
        #     print name, " Device not found"
        #     print "Avalible devices: "
        #     print self.dev_list
        #     self.handle = None
        #     return -1
        
        # # Sets parameters for serial communications
        # ftdi_thread_lock.acquire()
        # try:
        #     self.handle.resetDevice()
        #     self.handle.setDataCharacteristics(d2xx.BITS_8, d2xx.STOP_BITS_1, d2xx.PARITY_NONE)
        #     self.handle.setFlowControl(d2xx.FLOW_NONE)
        #     self.handle.setBaudRate(self.baud)
        #     self.handle.purge(d2xx.PURGE_RX | d2xx.PURGE_TX)
        #     self.handle.setDtr()
        #     self.handle.setRts()
        # finally:
        #     ftdi_thread_lock.release()
        self.socket.connect((HOST, PORT))
        self.read_thread = socket_read_thread(self.socket)
        self.read_thread.begin()
        return 0
        
            
    # reads data from the USB device
    def read(self):
        # print "reading: ",data
        message=self.socket.recv(1024)
        return message
       
    
    # writes data to the usb device
    def write(self, data):
        # print "writing: ",data
        errcode = self.socket.send(data) 
        return errcode
        
    # closes USB device 
    def close(self):
        self.socket.close()

    

# Class to read data from socket
class socket_read_thread(QtCore.QThread): 
    # constructor
    def __init__(self, socket): 
        # input("entering socket read thread init\n")
        QtCore.QThread.__init__(self)
        super(socket_read_thread, self).__init__(self) 
        self.socket = socket


    # Main loop that reads data from FPGA. It terminates on error
    def run(self):
        # input("entering run\n")
        buffer=[]
        loopcount=0
        while (True):
            # self.socket.send("1") #telling server we are ready to receive next batch
            #loopcount+=1
            valid_flag=True #whether this buffer can be used for analysis (correct and complete)
            message=self.socket.recv(1024)
            # print "received message: ",message
            #print "begin\n",message,"end\n"
            if len(message)==0:
                continue
            
            #print "line:\n",line
            # if len(line)<3:
            #     continue
            #print "\nunpacking: ",line
            # counter_n,n_counts = line.split(" ");    
                # valid_flag=False;
        # if counter_n != 1:
        #     continue;
        # else:

            # buffer.append(n_counts)
                    
            # if counter_n == '8':
                # if len(buffer) == 8:
                    # for idx in range(8):
                        # self.line[idx+1].add(int(buffer[idx]))
                    # print "buffer!:",buffer
                    # self.readings += 1
                    # if (self.readings >= self.refresh):
                        # self.add_point()
                        # self.readings=0
                # buffer=[]

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














    # def update_data(self):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect((HOST, PORT))
    #     # self.parse_data(data)
    #     buffer=[]
    #     loopcount=0
    #     while (loopcount<100):
    #         loopcount+=1
    #         valid_flag=True #whether this buffer can be used for analysis (correct and complete)
    #         message=s.recv(1024)
    #         print "begin\n",message,"end\n"
    #         if len(message)==0:
    #             continue
    #         lines=message.split("\n")
    #         print "lines:\n",lines
    #         # for n_line,line in enumerate(lines):
    #         line = lines[0]
    #         if len(line)<3:
    #             continue
    #         print "line:\n",line
    #         # if len(line)<3:
    #         #     continue
    #         print "\nunpacking: ",line
    #         counter_n,n_counts = line.split(" ");    
    #             # valid_flag=False;
    #     # if counter_n != 1:
    #     #     continue;
    #     # else:

    #         buffer.append(n_counts)
                    
    #         if counter_n == '8':
    #             if len(buffer) == 8:
    #                 for idx in range(8):
    #                     self.line[idx+1].add(int(buffer[idx]))
    #                 print "buffer!:",buffer
    #                 self.readings += 1
    #                 if (self.readings >= self.refresh):
    #                     self.add_point()
    #                     self.readings=0
    #             buffer=[]
    #         s.send("1") #telling server we are ready to receive next batch
