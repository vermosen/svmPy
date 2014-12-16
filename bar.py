'''
svmPython
Created on Sep 24, 2014
@author: jean-mathieu vermosen
'''

from enum import Enum

''' enumeration for built-in bar length '''
class barLength(Enum):
    ms100 = 1
    
class bar:
    
    ''' Some bar class '''
    def __init__(self, startDate_, length_, open_, close_, high_, low_, volume_):
        
        '''feed the variables'''
        self.startDate = startDate_
        self.length    =    length_
        self.open      =      open_
        self.close     =     close_
        self.high      =      high_
        self.low       =       low_
        self.volume    =    volume_
        
    ''' print() operator '''
    def __str__(self):
    
        return 'date: %s, open price: %s, close price: %s, volume:' \
        % (self.startDate.strftime('%m-%d-%Y'), 
           str(self.open),
           str(self.close),
           str(self(volume)))
        
    ''' calculate the end date'''
    def __end__(self):
        