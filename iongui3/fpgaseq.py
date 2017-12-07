'''
Created on 19-Apr-2011

@author: cqt
'''
from PyQt4 import QtCore
# from usb_ftdi import ftdi_usb
import random
from socket_thread import socket_t, socket_read_thread 

usingUSB = 0

# represents one line of the time sequence (bit pattern + delay)
class SeqLine():
    def __init__(self, delay, scanned, bitarray):
        self.delay      = delay
        self.bitarray   = bitarray
        self.scanned    = scanned
        
    def write(self):
        print self.delay, self.scanned, self.bitarray

# class Net_Transfer(PORT,ADDRESS):
#     def __init__(self):


class FPGA_Seq(QtCore.QObject):
    
    hready   = QtCore.pyqtSignal()
    
    def __init__(self):
        super(FPGA_Seq, self).__init__()
        
        self.guiseq   = []
        self.fpgaseq  = []
        self.oldfpgaseq = []
        self.fpgastr  = ""
        self.nrep     = 100 # Number of repetitions
        self.mask     = {0:1, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0} # counter mask
        self.data     = ''      # I don't know the purpose of this variable. It gets written AND erased in "data_ready_slot" RH
        self.hist     = [] # histrograms collected but not displayed
        self.HISTSIZE = 256
        self.hcurrent    =   {}
        self.fpga_data =   [] # list with the counter readings
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Open USB device 

        try:
            self.usb      = ftdi_usb(baud = 8 * 57600) 
            self.usbstatus = self.usb.open("FPGA Sequencer A")
        except :
            self.usbstatus = -1

        self.usb    = socket_t()
        self.usbstatus = 0

#        self.usbstatus = self.usb.open("Dual RS232-HS A")
        if (self.usbstatus != 0):
            print "Can't connect to FPGA sequencer, check USB connection, error code: ", self.usbstatus
        else:
            QtCore.QObject.connect(self.usb.read_thread, QtCore.SIGNAL('data_ready(QByteArray)'), self.data_ready_slot)
            print "FPGA Sequencer A opened"




        self.timer = QtCore.QTimer() # Timer to generate fake debugging data. 

    # process data from the FPGA and returns a histrogram
    # bytes is a string of triples of the form "(letter)(\x hex)(\x hex)". when letter = s, generate histogram RH
    def data_ready_slot(self, bytes):
        # print "bytes", bytes
        self.data += bytes      # I don't see the point of using "+=". RH
        while (len(self.data) > 2):
            # extract data for the next run
            key = self.data[0]
            d   = bytearray(self.data[1:3])
#            print "key, data:", key, self.data[1].encode("hex"), self.data[2].encode("hex")
#            index = d[0] * 256 + d[1]
            index = d[1] * 256 + d[0]
 
            if (index >= self.HISTSIZE):
                print "Index", index, "overshoot in key", str(key) + ". Set to max value."
                index = self.HISTSIZE - 1
            if (key == 's'):
                # Process last bytes in this dataset and notify everyone about the new histrogram
                # print self.hcurrent
                self.hist.append( (self.hcurrent.copy(), self.fpga_data[:]) )
                self.hcurrent   = {}
                self.fpga_data  = []
                self.hready.emit()
                # self.emit(QtCore.SIGNAL('histrogram_ready()'))
            else:
                # append another data point to the histrogram
                # print "counter: ", key, " value: ", index
                # adds the histrogram for a counter if it was not there yet
                if (key not in self.hcurrent):
                    self.hcurrent[key] = [0] * self.HISTSIZE  
                self.hcurrent[key][index] += 1
                self.fpga_data.append( (key, index) )
            # discard processed data
            self.data = self.data[3:]
    
    # Generates fake data for debugging
    def fake_data_ready_slot(self):
        self.hcurrent['a'] = [0] * self.HISTSIZE
        for i in range(self.nrep):
            index =  random.randint(0, self.HISTSIZE / 16 - 1)
            self.hcurrent['a'][index] += 1
            self.fpga_data.append( ('a', index) )
        
        self.hist.append( (self.hcurrent.copy(), self.fpga_data[:] ) )
        self.hcurrent    = {}
        self.fpga_data = []
        self.hready.emit()
    
    # Sets mask for the photon counters
    def setCntrMask(self, mask):
        for i in range(8):
            if (((1<<i) & mask ) == 0):
                self.mask[i] = 0
            else:
                self.mask[i] = 1
#        print self.mask
#
        
    # Sets number of repetitions
    def setNrep(self, nrep):
        self.nrep = max(0, min(nrep, 65535) )
    
    # takes the new time sequence from the gui and prepares it for loading
    def setSeq(self, seq, changes_only = False):
        self.guiseq  = seq
#        print "prepare to write", self.guiseq
        self.fpgaseq = []
        if (len(seq) == 0):
            return
        
        # first line 
        current = self.guiseq[0].bitarray   # dictionary of first row {number: state}, where number runs from 0 to 39 (4 bytes outputs and 1 byte counter gate) and state is in {-1, 0, 1}
        # print "guiseq[0].bitarray is", current
        current = self.bound(current)   # maps state -1 or 0 -> 0 and 1 -> 1. State 0 is "copy previous", but there is no previous in the first row.
        # print "bound is", current
        self.fpgaseq.append(SeqLine(self.guiseq[0].delay, self.guiseq[0].scanned, current.copy() ) )
        # the rest of the lines
        for l in self.guiseq[1:]:
            current = self.nextline(current, l.bitarray)
            self.fpgaseq.append(SeqLine(l.delay, l.scanned, current.copy())) 

        if (changes_only):
            self.seqStringChanged()
        else:
            self.seqString()

        print "going to write to fpga: \n", self.fpgastr
        self.write()
#        self.usb.write(self.fpgastr)
#        self.oldfpgaseq = list(self.fpgaseq) # To copy elements, not the reference

    # writes the sequence to the fpga and saves it locally, so that we know what FPGA has
    def write(self):
        self.usb.write(self.fpgastr)        
        self.oldfpgaseq = list(self.fpgaseq) # To copy elements, not the reference

    # Convert sequence to a string that can be sent to FPGA
    def seqString(self):
        self.fpgastr = ''

        for lnum, l in enumerate(self.fpgaseq):
            delay = max(1, int( l.delay / 0.02) )
            self.fpgastr += 'm' + self.convertInt(lnum, 4) + self.convertInt(delay-2, 8) + self.convertBits(l.bitarray) + '\r\n'
            # delay-2 to account for the inherent 2-cycle delay in FPGA
            # temporary : in the future output data should be a longer bit array, not repeating one bitarray

            '''
            memory address
            bits from 0 to 39 (but for now we control from 0 to 31)
            delay, I don't know why to divide by 0.02
            '''
        self.fpgastr += 'r' + self.convertInt(len(self.fpgaseq) - 1, 4) + '-----+++++-----+++++----' + '\r\n' # placeholder to make lines equal in length
#        print self.fpgastr


    # Converts the sequence to a string,
    # tries not to resend lines that are already in the fpga memory to save time
    def seqStringChanged(self):
        self.fpgastr = ''
        for lnum, l in enumerate(self.fpgaseq):
            if (lnum < len(self.oldfpgaseq)): # old sequence is too short
                lold = self.oldfpgaseq[lnum]
                if(lold.bitarray == l.bitarray and lold.delay == l.delay): # line did not change
                    continue
            delay = max(1, int( l.delay / 0.02) )
            self.fpgastr += 'm' + self.convertInt(lnum, 4) + self.convertInt(delay-2, 8) + self.convertBits(l.bitarray) + '\r\n'
        self.fpgastr += 'r' + self.convertInt(len(self.fpgaseq) - 1, 4) + '-----+++++-----+++++----' + '\r\n' # placeholder to make lines equal in length
        print "FPGA string", self.fpgastr


    # updates next line of a bit array
    def nextline(self, current, next):
        for i in range(len(current)):
            current[i] = current[i] + next[i]
        return self.bound(current)
        
    
# keeps bitarray between 0 and 1
    def bound(self, bitarray):
        for i in range(len(bitarray)):
            if (bitarray[i] < 0):
                bitarray[i] = 0
            if (bitarray[i] > 1):
                bitarray[i] = 1
        return bitarray        
        
        
    def display(self):
#        print "FPGA Sequence:"
        for i in self.fpgaseq:
            i.write()

# load the timesequence to FPGA    
    def load(self):
        self.usb.write(self.fpgastr)
        self.oldfpgaseq = list(self.fpgaseq) # To copy elements, not the reference

        
# sends the command to start time sequence
    def run(self):
        if (self.usbstatus == 0):
            line = 'n' + self.convertInt(self.nrep, 4) + self.convertBits(self.mask) + '-----+++++-----+++++--' + '\r\n' # + and - are placeholders to keep lines equal in length 
#            print "line is", line
            self.usb.write(line)
        else: # emulate the board if the device driver was not connected
            self.fake_run()

# Fake start of the time sequence
    def fake_run(self):
#        self.fake_data_ready_slot()
#        self.timer.start()
        print "Fake run"
        self.timer.singleShot(400, self.fake_data_ready_slot)

# converts integer value to the fpga encoding
    def convertInt(self, value, len):
#        strval = QtCore.QString.number(value, 16).toUpper()
        fstr = "{0:0" + str(len) + "X}"
        strval = fstr.format(value)
#        print "converted", fstr, "with value", value, "to", strval
        return self.substitute(strval)        

# Converts bit array to a FPGA encoding
    def convertBits(self, bits):
        strval = ''
        for i in range(len(bits)/4):
            chr = 8*bits[4*i+3] + 4*bits[4*i+2] + 2*bits[4*i+1] + bits[4*i]
            strval = "{0:X}".format(chr) + strval
#        print "converted", bits, "to", strval
        return self.substitute(strval)
            
# private function to converts hex string to an fpga encoding  
    def substitute(self, strval):
        strval = strval.replace('A',':')
        strval = strval.replace('B',';')
        strval = strval.replace('C','<')
        strval = strval.replace('D','=')
        strval = strval.replace('E','>')
        strval = strval.replace('F','?')
        return strval


# main function to test GUI
def main():
    app = FPGA_Seq()
#    print app.convertInt(946396, 8)
#    print app.convertBits( [1,0,0,0,1,1,1,1] )
    app.data_ready_slot('a\x00\x00a\x00\x01a\x00\x08a\x00\x00s\x00\x00')
    print app.hist

if __name__ == "__main__":
    main()

