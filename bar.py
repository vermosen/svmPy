'''
svmPython
Created on Sep 24, 2014
@author: jean-mathieu vermosen
'''

class bar:
    """Iterator for looping over a sequence backwards."""
    def __init__(self, startDate_, length_, open_, close_, high_, low_, volume_):
        
        '''feed the variables'''
        self.startDate = startDate_
        self.length    = length_
        self.open      = open_
        self.close     = close_
        self.high      = high_
        self.low       = low_
        self.volume    = volume_
         