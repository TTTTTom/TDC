'''
Created on 18-Jul-2012

@author: dzmitry2
'''

import visa
from dummydevice import FreqGenerator

# DDS generator for debug purposes
class KeithleyGenerator(FreqGenerator):
    def __init__(self, id = "usb0::0x05E6::0x3390::1373409::INSTR"):
        FreqGenerator.__init__(self)
        
        try: 
            self.connected  = True
            self.keithley   = keithley_control(id)      
            self.name       = "Keithley" 
            self.description= "Keithley Generator: " + self.keithley.get_description()
            self.properties = ["Frequency", "Amplitude", "Phase", "Offset", "Shape"]
            self.min     = {"Frequency": 0.1,        "Amplitude" : 0.01, "Phase" : 0.0,   "Offset" : -5.0, "Shape" : 0}
            self.max     = {"Frequency": 50000000.0, "Amplitude" : 10,   "Phase" : 360.0, "Offset" :  5.0, "Shape" : 3}
            self.value   = {"Frequency":   100000.0, "Amplitude" : 3.6,  "Phase" : 0.0,   "Offset" :  1.8, "Shape" : 1}
            self.default = {"Frequency":   0.1, "Amplitude" : 0.01,  "Phase" : 0.0,   "Offset" :    0, "Shape" : 3}
        
#            time.sleep(0.1)        
            for p in self.default.iterkeys():
                self.setProperty(p, self.default[p] )
            self.keithley.switch_on()
                               
        except visa.VisaIOError:
            print "Keithley generator not found"
            self.connected = False


    def setDefault(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        self.value[property] = value
        return True

    
    def setProperty(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        if   (property == "Frequency"):
            self.keithley.set_frequency(value)
        elif (property == "Amplitude"):
            self.keithley.set_amplitude(value)
        elif (property == "Phase"):
            self.keithley.set_phase(value)
        elif (property == "Offset"):
            self.keithley.set_offset(value)
        elif (property == "Shape"):
            self.keithley.set_shape(value)
            
        self.value[property] = value
        return True


class keithley_control():
    def __init__(self, id = "usb0::0x05E6::0x3390::1373409::INSTR"):
        self.keithley = visa.instrument(id)
        self.SINE   = 0
        self.RAMP   = 1
        self.SQUARE = 2
        self.PULSE  = 3

    def __del__(self):
        self.keithley.close()

#set different shape of output    
    def set_shape(self, shape):
        if   (shape == self.SINE):
            self.keithley.write("FUNCtion SINusoid")
        elif (shape == self.RAMP):
            self.keithley.write("FUNCtion RAMP")
        elif (shape == self.SQUARE):
            self.keithley.write("FUNCtion SQUare")
        elif (shape == self.PULSE):
            self.keithley.write("FUNCtion PULse")

#set frequency, make sure that the variable fre should be in string format,eg"10 HZ"       
    def set_frequency(self,fre):
        self.keithley.write("FREQuency "+str(fre)+" HZ")  
          
#set amplitude, make sure that the variable amp should be in string format,eg "10mVPP"       
    def set_amplitude(self,amp):        
        self.keithley.write("VOLTage "+str(amp)+" VPP")

#set off set, make sure that the variable offset should be in string format,eg "1 V"       
    def set_offset(self,offset):         
        self.keithley.write("VOLTage:OFFSet "+str(offset)+" V")
    
#set phase
    def set_phase(self,phase):
#first,set phase unit        
        self.keithley.write("UNIT:ANGLe DEGree")
#or we can use radian unit,the code is :        
#keithley.write("UNIT:ANGLe RADians")
# then,set phase
        self.keithley.write("PHASe "+str(phase))
        
#switch on
    def switch_on(self):
        self.keithley.write("OUTPut on")
        
#switch off
    def switch_off(self):        
        self.keithley.write("OUTPut off")

#set DC output
    def setDC_output(self,voltage):
        self.keithley.write("APPL:DC DEF, DEF, "+str(voltage))
        
#set sine wave frequency and amplitude and offset,make sure that the variable should be string format,for example:"20KHZ" "10mVPP" "2.5V"    
    def setsinefreq_ampl_offset(self,fre,amp,offset):
        self.keithley.write("APPL:SIN "+str(fre)+", "+str(amp)+", "+str(offset))

#query the current configuration
    def query_configuaration(self):
        print self.keithley.write("APPLy?")
        
    def get_description(self):
        return self.keithley.ask("*IDN?")



