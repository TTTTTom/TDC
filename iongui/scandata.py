'''
Created on 13-May-2011

@author: cqt
'''

import csv
import time

# class to store data for a single plot
class ScanData():
    def __init__(self, maxsize = 200, refresh = 1):
        self.y         = []
        self.x         = []
        self.xextra    = []
        self.ysum      = []
        self.nsum      = []
        self.histogram = [] # Histogram
        self.counters  = [] # Data from all the counters
        self.fpga_data = [] # Raw fpga data
        self.nexp      = [] # Number of experiments per point
        self.timestamps= [] # timetsamp when this point was taken
        self.count     = 0
        self.maxsize   = maxsize    # Max length of a plot
    
    # add point to the data, limit the data size to maxsize 
    def add(self, value, histogram, counters, fpga_data ):
        self.y.insert(0, value)
        self.ysum.insert(0, value)
        self.nsum.insert(0, 1)
        self.x.insert(0, self.count)
        self.histogram.insert(0, histogram)
        self.nexp.insert(0, sum(histogram))
        self.counters.insert(0, counters)
        self.fpga_data.insert(0, fpga_data)
        self.timestamps.insert(0, [time.time()])
        self.count += 1
        if (len(self.y) > self.maxsize):
            del self.y[self.maxsize]
            del self.x[self.maxsize]
#            del self.xextra[self.maxsize]
            del self.ysum[self.maxsize]
            del self.nsum[self.maxsize]
            del self.histogram[self.maxsize]
            del self.nexp[self.maxsize]
            del self.counters[self.maxsize]
            del self.fpga_data[self.maxsize]
            del self.timestamps[self.maxsize]
             
    # add (x,y) pair to the data, and update average
    def add_pair(self, xp, yp, histogram, counters, fpga_data, *args):
        try:
            idx = self.x.index(xp)
            self.y[idx]     = yp
            self.ysum[idx] += yp
            self.nsum[idx] += 1
            for i in range(0, len(histogram)):
                self.histogram[idx][i] += histogram[i]
            for i in range(0, len(counters)):
                self.counters[idx][i] += counters[i]
            self.fpga_data[idx].extend(fpga_data)
            self.timestamps[idx].append(time.time())
        except:
            self.y.insert(0, yp)
            self.x.insert(0, xp)
            self.ysum.insert(0, yp)
            self.nsum.insert(0, 1)
            self.histogram.insert(0, histogram)
            self.counters.insert(0, counters)
            self.fpga_data.insert(0, fpga_data)
            self.timestamps.insert(0, [time.time()])
            if len(args) != 0:
                self.xextra.insert(0, args)

    
    # discards all the data
    def reset(self):
        self.x         = []
        self.xextra    = []
        self.y         = []
        self.ysum      = []
        self.nsum      = []
        self.histogram = []
        self.counters  = []
        self.fpga_data = []
        self.nexp      = []
        self.timestamps= []
        self.count     = 0
        
    # returns current data
    def get(self):
        return self.y
    
    # returns average value
    def get_avg(self):
        avg = [0] * len(self.ysum)
        for i in range(0, len(self.x)):
            avg[i] = self.ysum[i] / self.nsum[i]
        return avg
    
    # returns x, y arrays of current data
    def getx(self):
        return self.x

    # returns the data for the specified counter, before or after threshold
    def get_counter_data(self, counter, threshold):
        if threshold:
            shift = 0
        else:
            shift = 8

        out = []
        for i in range(len(self.x)):
            out.append(self.counters[i][counter + shift])
        return out

    # return average value and the number of experiments 
    def get_running_avg(self):
#        avg  = 0.0
#        nexp = 0
#       for i in range(0, len(self.x)):
#            avg  += self.ysum[i]
#            nrun += self.nsum[i]
        return sum(self.ysum), sum(self.nsum), sum(self.nexp)
    
    # set max size of the data array
    def set_maxsize(self, maxsize):
        self.maxsize = maxsize
        
    # save data to the file
    def save(self, fname):
        with open(fname, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0, len(self.x)):
                data = [ self.x[i], self.y[i], self.ysum[i]/self.nsum[i] ]
                if len(self.xextra) == len(self.x):
                    data.extend(self.xextra[i])
                data.extend([x/self.nsum[i] for x in self.counters[i]])
#                data.append(self.timestamps[i])
                writer.writerow( data )

                
    # Saves fpga data and histograms in addition to the counter data
    def save_with_histogram(self, fname):
        with open(fname, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0, len(self.x)):
                data = [ self.x[i], self.y[i], self.ysum[i]/self.nsum[i]]
                if len(self.xextra) == len(self.x):
                    data.extend(self.xextra[i])
                data.extend([x/self.nsum[i] for x in self.counters[i]])
                data.append(self.timestamps[i])
                data.append(self.histogram[i])
                data.append(self.fpga_data[i])
                writer.writerow( data )

if __name__ == "__main__":

    my_data=ScanData()