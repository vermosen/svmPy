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
from sklearn.linear_model import LogisticRegression as LR
from sklearn.svm import SVC as SVM
from sklearn.svm import LinearSVC as SVM_l
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
queryEnd   = datetime.datetime(2014, 3, 4, 21, 0 , 0)

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
    
''' close the connection and cleanup '''
cursor.close(); cnx.close()
del cursor    ; del cnx

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
    
''' compute price change '''
data['price diff'] = pd.Series(data['close'] - data['close'].shift(1), 
                               index=data.index)

data['close change'] = pd.Series(np.sign(data['price diff']),
                                 index = data.index)

''' intercept '''
data['intercept'] = 1.0

''' suppress the extra columns '''
data = data.ix[:,['intercept', 'close change', 'volume']]

''' creates the lagged change '''
for i in range(1, 10):
    data['lag ' + str(i)] = data['close change'].shift(i)

train_sz = int(len(data) * .6)          # training sample size
data = data.ix[10:,:]                   # drop NaNs
data_train = data.ix[:,:train_sz]       # training sample

''' data studies '''
print('number of bars: %s' % len(data)) # total number of bars
print('training sample size: %s' 
      % len(data_train))
print(data.dtypes)                      # data types
print(data.mean())                      # means
print(data.std())                       # stdev
data['volume'].plot(); pl.show()        # volume histograms

''' resulting train sample '''
print(data_train.head())

''' 1 - logistic regression '''
logit = LR(C=1.0, fit_intercept=False)
logit.fit(X = data_train.drop('close change', axis=1), 
          y = data_train['close change'])

''' misclassification rate '''
res_logit = logit.predict(X = data.drop('close change', axis=1))
print('Logistic regression misclassification '
      'rate on the test sample: %s' 
      % np.mean(data['close change'] != res_logit))

''' 2 - radial function basis svm '''
svm = SVM(C = 1.0, kernel = 'rbf', gamma = 0.1, max_iter = 5000)
svm.fit(X = data_train.drop('close change', axis=1), 
        y = data_train['close change'])

''' misclassification rate '''
res_svm = svm.predict(X = data.drop('close change', axis=1))
print('Radial basis-SVM misclassification '
      'rate on the test sample: %s' 
      % np.mean(data['close change'] != res_svm))

''' linear SVM'''
linear = SVM_l(C = 1.0, fit_intercept = False)
linear.fit(X = data_train.drop('close change', axis=1), 
           y = data_train['close change'])

''' misclassification rate '''
res_linear = linear.predict(X = data.drop('close change', axis=1))
print('linear-SVM misclassification '
      'rate on the test sample: %s' 
      % np.mean(data['close change'] != res_linear))
