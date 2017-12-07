'''
Created on 18-Jul-2012

@author: dzmitry2
'''

import visa
from dummydevice import FreqGenerator

# DDS generator for debug purposes
class N5183AGenerator(FreqGenerator):
    def __init__(self, id = "USB0::0x0957::0x1F01::MY50142329::0::INSTR", offset = 12542.8170):
        FreqGenerator.__init__(self)
        
        try: 
            self.connected  = True
            self.agilent   = agilent_control(id)
            self.agilent.set_offset(offset)      
            self.name     = "N5183A" 
            self.description= "Agilent : " + self.agilent.get_description()
            self.properties = ["Frequency", "Power"]
            self.min     = {"Frequency": 0.100 - offset,      "Power" : -20.0}
            self.max     = {"Frequency": 32000.0000 - offset, "Power" : +15.0}
            self.value   = {"Frequency": 12642.8170 - offset, "Power" : 10.0}
            self.default = {"Frequency": 12642.8170 - offset, "Power" : 10.0}
            self.minscan = {"Frequency": 99.5 ,               "Power" : 5.0}
            self.maxscan = {"Frequency": 100.5 ,              "Power" : 12.0}
            self.stepscan= {"Frequency": 0.01,                "Power" : 0.5}
            self.agilent.reset()
#            time.sleep(0.1)        
            for p in self.default.iterkeys():
                self.setProperty(p, self.default[p] )
            self.agilent.switch_on()
                               
        except visa.VisaIOError:
            print "Agilent generator not found"
            self.connected = False

        except AttributeError:
            print "Agilent generator not found"
            self.connected = False

    # Return scan range for a corresponding property
    def getScanRange(self, property):
        if property not in self.properties:
            return 0.0, 0.0, 0.0
        else:
            return self.minscan[property], self.maxscan[property], self.stepscan[property]

    def setDefault(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        self.value[property] = value  # It should be self.default[property] = value
        return True

    
    def setProperty(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        if   (property == "Frequency"):
            self.agilent.set_frequency(value)
        elif (property == "Power"):
            self.agilent.set_amplitude(value)
           
        self.value[property] = value
        return True

class Echo():
    def ask(self, text):
        return "I'm Dummy. Don't ask me " + text

    def write(self, text):
        print "Dummy Agilent got", text

    def close(self):
        print "You cannot close me!"

class agilent_control():
    def __init__(self, id = "USB0::0x0957::0x1F01::MY50142329::0::INSTR"):
#        try:
#            self.agilent = visa.instrument(id)
#        except:
#            self.agilent = Echo()
#            print "Dummy Agilent loaded"
        self.agilent = visa.instrument(id)
        self.offset = 0.0

    def __del__(self):
        self.agilent.close()

# set offset to make the frequency setting more convenient to use.
    def set_offset(self, offset):
        self.offset = offset

#set frequency, make sure that the variable fre should be in string format,eg"10 HZ"       
    def set_frequency(self,fre):
        self.agilent.write(":FREQ:CW " +str(fre + self.offset) + "MHz")  
          
#set amplitude, make sure that the variable amp should be in string format,eg "10mVPP"       
    def set_amplitude(self,pwr):        
        self.agilent.write(":POW "+str(pwr)+"DBM")

# Initialise
    def reset(self):
        self.agilent.write("*RST")

#switch on
    def switch_on(self):
        self.agilent.write(":OUTP ON")
        
#switch off
    def switch_off(self):        
        self.agilent.write(":OUTP OFF")

#query the current configuration
    def query_configuaration(self):
        print self.agilent.write("APPLy?")
        
    def get_description(self):
        print self.agilent.ask("*IDN?")
        print "type", type(self.agilent.ask("*IDN?"))
        return "Offset: " + str(self.offset) + " " + self.agilent.ask("*IDN?")


if __name__ == '__main__':
    device = N5183AGenerator()
    device.setProperty("Frequency", 100.000)
    device.setProperty("Power", 50.0)
    

