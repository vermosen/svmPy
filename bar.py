'''
svmPython
Created on Sep 24, 2014
@author: jean-mathieu vermosen
'''

from enum import Enum
from datetime import timedelta

''' enumeration for built-in bar length '''
class barLength(Enum):
    
    ms100 = 1
    min1  = 2
    
class bar:
    
    ''' static variable ''' 
    lenDict = {barLength.ms100 : timedelta(milliseconds=100),
               barLength.min1  : timedelta(seconds=1)       }
        
    ''' Some bar class '''
    def __init__(self, startDate_, length_, open_, close_, high_, low_, volume_):
        
        '''feed the variables'''
        self.startDate = startDate_
        self.length    = barLength(length_)
        self.open      =      open_
        self.close     =     close_
        self.high      =      high_
        self.low       =       low_
        self.volume    =    volume_
        
    ''' print() operator '''
    def __str__(self):
    
        return 'date: %s, open price: %s, close price: %s, volume: %s' \
        % (self.startDate.strftime('%m-%d-%Y'), 
           str(self.open),
           str(self.close),
           str(self.volume))
     
        
    ''' calculate the end date '''
    def endDate(self):
        
        return self.startDate + self.lenDict[self.length]
    
    ''' insert the bar in some date frame '''
    def insert(self, df):   
        ''' insert '''
        return df