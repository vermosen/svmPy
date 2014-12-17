'''
svmPython
Created on Sep 24, 2014
@author: jean-mathieu vermosen
'''

import bar

''' a container of bars '''
class bars:
    
    def __init__(self, bars_):
        
        ''' ensure the bar have the right type ''' 
        if not isinstance(bars_, bar):
            raise TypeError("bars must be set of type 'bar'")
        
        self.bars = bars_