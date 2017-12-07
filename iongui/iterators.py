__author__ = 'Dzmitry Matsukevich'

import random
import itertools
import csv

#def frange(start, stop, step):
#    if (step == 0):
#        return
#    while start < stop:
#        yield start
#        start += step


class axis_range:
    def __init__(self, start, stop, step, type="Linear", filename=""):
        self.start = start
        self.stop  = stop
        self.step  = step
        self.type  = type
        self.filename = filename

    def get(self):
        if (self.type == "From File"):
            return iter(frange_file_tuple(self.filename))
        elif (self.type == "Random"):
            return iter(frange_rnd_tuple(self.start, self.stop, self.step))
        else: # We assume linear scan was requested
            return iter(frange_lin_tuple(self.start, self.stop, self.step))


    def set_file_name(self, fname):
        self.filename = fname

class frange_lin:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop  = stop
        self.step  = step
        self.current = start

    def __iter__(self):
        return self

    def next(self):
        if self.start < self.stop:
            if self.current > self.stop:
                raise StopIteration
            else:
                self.current += self.step
                return self.current - self.step
        else:
            if self.current < self.stop:
                raise StopIteration
            else:
                self.current -= self.step
                return self.current + self.step


# The same iterator as above, but does it in the random order
class frange_rnd:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop  = stop
        self.step  = step
        self.range =list( frange_lin(self.start, self.stop, self.step) )
        random.shuffle(self.range)


    def __iter__(self):
        return iter(self.range)

# Iterate over several quantities at the same time
class frange_lin_tuple:
    def __init__(self, start, stop, step):
        self.iterators = []
        for i in range(len(start)):
            self.iterators.append(frange_lin(start[i], stop[i], step[i]))

    def __iter__(self):
        return itertools.izip(*self.iterators) # star (*) meand=s "unpacking arguments"

# Iterate over several quantities at the same time, but in the random order
class frange_rnd_tuple:
    def __init__(self, start, stop, step):
        self.range = list(frange_lin_tuple(start, stop, step))
        random.shuffle(self.range)

    def __iter__(self):
        return iter(self.range)


# Returns iterator over the values stored in the file
class frange_file_tuple:
    def __init__(self, fname):
        self.range = []
        print "Loading file " + fname
        with open(fname, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 1 :
                    self.range.append( (float(row[0]), float(row[0])) )
                else:
                    self.range.append( (float(row[0]), float(row[1])) )

    def __iter__(self):
        return iter(self.range)

# main function to test USB module
def main():
#    print list(frange(1.0, 99.6, 2.1) )

#    freq_iter = iter( frange_rnd(1.0, 99.6, 2.1) )

#    freq_iter1 = iter (frange_lin( 0.0, 20.0, 1.0 ))
#    freq_iter2 = iter (frange_lin( 10.0, 30.0, 1.0 ))
#    freq_iter  = itertools.izip(freq_iter1, freq_iter2)

#    freq_iter = iter(frange_rnd_tuple( (0.0, 10.0), (20.0, 30.0), (1.0, 1.0) ))

    freq_iter = iter(frange_file_tuple("C:\\Users\\Dima\\Desktop\\test.txt"))

    while (True):
        try:
            freq = freq_iter.next()
            print freq
        except StopIteration:
            print "Done ... "
            return


if __name__ == "__main__":
    main()
