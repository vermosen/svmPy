'''
svmPython
Created on Sep 24, 2014
@author: jean-mathieu vermosen
'''


import datetime
import mysql.connector
import pandas as pd
import numpy as np
import pylab as pl
from mysql.connector import errorcode
from bar import bar

try:
    
    ''' connection configuration '''
    config = {'user'              : 'root'                                  ,
              'password'          : ''                                      ,
              'host'              : 'localhost'                             ,
              'database'          : 'fixdb'                                 ,
              'port'              : '3308'                                  ,
              'unix_socket'       : '/opt/local/var/run/mysql56/mysqld.sock',
              'option_files'      : '/opt/local/etc/mysql56/my.cnf'         ,
              'raise_on_warnings' : True                                     }
    
    ''' connection to the database '''
    cnx = mysql.connector.connect(**config)

except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exists")
    else:
        print(err)

cursor = cnx.cursor()

query = ("SELECT BAR_DATETIME, BAR_OPEN, BAR_CLOSE, "
         "BAR_HIGH, BAR_LOW, BAR_VOLUME, BAR_LENGTH "
         "FROM table_bar "
         "WHERE (INSTRUMENT_ID = 256 AND BAR_DATETIME "
         "BETWEEN %s AND %s)")

''' select 1 day of trading '''
queryStart = datetime.datetime(2014, 3, 3, 14, 30, 0)
queryEnd   = datetime.datetime(2014, 3, 3, 21, 0 , 0)

''' execute the query '''
cursor.execute(query, (queryStart, queryEnd))

bars = []

for (BAR_DATETIME, 
     BAR_OPEN, 
     BAR_CLOSE, 
     BAR_HIGH, 
     BAR_LOW, 
     BAR_VOLUME, 
     BAR_LENGTH) in cursor:
    
    ''' create a bar '''
    bars.append(bar(BAR_DATETIME, 
                    BAR_LENGTH, 
                    BAR_OPEN, 
                    BAR_CLOSE, 
                    BAR_HIGH, 
                    BAR_LOW, 
                    BAR_VOLUME))
    
''' close and cleanup '''
cursor.close(); cnx.close()
del cursor; del cnx

print('number of bars: %s' % len(bars))

''' create the series '''
idx_    = []; close_  = []; volume_ = []

''' feed the series '''
for i in bars:                   
    idx_.append    (i.startDate)
    close_.append  (i.close    )
    volume_.append (i.volume   )
    
''' create the data frame '''
data = pd.DataFrame({'close' : close_  , 
                     'volume': volume_
                    }, index = idx_)
    
''' add columns '''
data['price diff'] = pd.Series(data['close'] - data['close'].shift(1), 
                               index=data.index)

data['close change'] = pd.Series(np.sign(data['price diff']),
                           index = data.index)

''' print data types '''
print(data.dtypes)

''' print the head '''
print(data.head())

''' means '''
print(data.mean())

''' std dev '''
print(data.std())

''' histogram '''
data.hist()

pl.show()
    