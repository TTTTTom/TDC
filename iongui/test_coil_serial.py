import serial
from time import sleep



class CoilSerial():
    def __init__(self, comport=10):
        try:
            self.ser = serial.Serial(comport,              # COM40
                                baudrate=9600,
                                parity='N',
                                bytesize=8,
                                stopbits=1,
                                rtscts=0,
                                timeout=1)
            print self.ser
        except:
            print "Error: Serial port already in use by other program or nothing is connected to the given COM port"
            raise

        self.ser.write("*IDN?\r")            # Identity
        idd = self.ser.read(11)
        if idd[0:3] != "CQT":            # I hope this will remain true in future versions of the board
            raise NameError("Wrong COM port: " + self.ser.portstr + ". This is not CQT Mini Analog")
        print idd



        #self.ser.write("*RST\r")                # Reset the board before use
        #print "Reset successful"

    # You need to turn on the analog in/output after reset.
    # To (sort of) "reset" this analog part, I switch it off first, and then on.
    # If you don't turn on this, you will get in principle fixed random values at the output
    # and you won't be able to control them.'''
        #self.ser.write("OFF\r")                # OFF
        #sleep(0.04)                        # Delay to turn OFF
        #print "Analog OFF"
#    ser.write("allin?\r")
#    IsOff = ser.read(40)
#    print IsOff
        #self.ser.write("ON\r")                # ON
        #sleep(0.1)                        # Delay to turn ON
        #print "Analog ON"


    def getinput(self):
        return self.ser.write("IN,0\r")
