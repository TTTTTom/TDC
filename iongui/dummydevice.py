'''
Created on 19-May-2011

@author: cqt
'''

import sys

# Base class for the frequency generator. Defines all the functions for external interface
class FreqGenerator():
    def __init__(self, optional = ""):
        self.name = ""
        self.description = ""
        self.properties = []
        self.min      = {}
        self.max      = {}
        self.value    = {}
        self.default  = {}
        self.minscan  = {}
        self.maxscan  = {}
        self.stepscan = {}

    
    # sets frequency, returns true if successful
    # Should be reloaded in the derived class
    def setProperty(self, property, value):
        self.value[property] = value
        return True

    # dummy function to set default value.
    def setDefault(self, property, value):
        self.default[property] = value
        return True

    # dummy function to set scan limits
    def setScanRange(self, property, minscan, maxscan, step):
        self.minscan[property]  = minscan
        self.maxscan[property]  = maxscan
        self.stepscan[property] = step

    # returns frequency limits
    def getProperty(self, property):
        return self.value[property]

    def getDefault(self, property):
        return self.default[property]
    
    
    def getName(self):
        return self.name
    
    def getDescription(self):
        return self.description
    
    def getPropertiesList(self):
        return self.properties
    
    def getPropertyLimits(self, property):
        return self.min[property], self.max[property]

    # Returns the current scan range for the property scan
    def getScanRange(self, property):
        return self.minscan[property], self.maxscan[property], self.stepscan[property]

    def isConnected(self):
        return True

    # load settings
    def load_settings(self, data):
        print "Loading data:", data
        try:
            if (data['name'] != self.name or data['description'] != self.description):
                return False
            for prop in data['properties']:
                 try:
                     self.setDefault (prop, data['default'][prop])
                     self.setProperty(prop, data['value'][prop] )
                     self.setScanRange(prop, data['minscan'][prop], data['maxscan'][prop], data['stepscan'][prop])
                 except KeyError:
                     print  "Property does not exist: ", prop, sys.exc_info()

        except KeyError:
            print  sys.exc_info()[0]
        return True

# Dummy generator for debug purposes
class DummyGenerator(FreqGenerator):
    def __init__(self):
        FreqGenerator.__init__(self)
        self.name       = "Dummy"
        self.description= "Dummy generator for debug purposes"
        self.properties = ["Frequency", "Amplitude", "Phase"]
        self.min     = {"Frequency": 1,   "Amplitude" : 0,    "Phase" :0}
        self.max     = {"Frequency": 200, "Amplitude" : 1023, "Phase" :360}
        self.value   = {"Frequency": 100, "Amplitude" : 512,  "Phase" :0}
        self.default = {"Frequency": 120, "Amplitude" : 600,  "Phase" :180}
        self.minscan = {"Frequency": 1,   "Amplitude" : 0,    "Phase" :0}
        self.maxscan = {"Frequency": 200, "Amplitude" : 1023, "Phase" :360}
        self.stepscan =  {"Frequency": 1,   "Amplitude" : 1,    "Phase" :1}


    def setDefault(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        self.default[property] = value
        return True

    
    def setProperty(self, property, value):
        if property not in self.properties:
            return False
        
        if (value > self.max[property]):
            return False        
        if (value < self.min[property]):
            return False
        
        self.value[property] = value
        return True

