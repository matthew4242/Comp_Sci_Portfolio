#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 00:07:52 2019

@author: mah60
"""
import pandas as pd
import numpy as np
import csv
# data preprocessing
from sklearn.preprocessing import StandardScaler
from keras.utils import to_categorical
from sklearn.impute import SimpleImputer
# model developement
from keras.optimizers import SGD
from keras.models import Sequential
from keras import layers as l
from keras.wrappers.scikit_learn import KerasClassifier
# fiting data 
from keras import callbacks as cb
from sklearn.model_selection import train_test_split
# evaluate model
from sklearn.metrics import classification_report
from sklearn import metrics
# cross validation
from sklearn.model_selection import StratifiedKFold
   

def load_data():
    """
    Will load the data from the test and train signal csv files.
    
    args => None
    Return => 
        X - np.ndarray - array of training data with selected values
        y - np.ndarray - array of expected values from the training data, transformed to
              integers depending on their key values
        X2_test - np.ndarray - test data with selected features
        reverse_class_id - dict - Y IDs but reversed 
                for converting y back to orginal values
        test_ID - np.ndarray - list of test IDs for the testing data
    """
    # get test and training data
    train_signal = pd.read_csv("./data/ecg/train_signal.csv")
    test_signal = pd.read_csv("./data/ecg/test_signal.csv")
    
    # determine the class - the output values
    y = train_signal['Type']
    # translate classes to numbers
    # create dict
    class_id = {'N': 0, 'O': 1, 'A':2, '~':3}
    reverse_class_id = {0:'N', 1:'O', 2:'A', 3:'~'}
    # replace values
    y = y.replace(class_id)
    # determine the values
    points = [col for col in train_signal if col.startswith('X')]
    # pick out input values
    X = train_signal[points]
    X2_test = test_signal[points]
    
    # cleans missing values within the data
    imp_mean = SimpleImputer(missing_values=np.NaN, strategy='mean')
    imp_mean.fit(X, y)
    X = imp_mean.transform(X)
    X2_test = imp_mean.transform(X2_test)
    X = pd.DataFrame(X) # transform back to dataframe
    X2_test = pd.DataFrame(X2_test)
    
    # scale features to more suitable format
    std = StandardScaler()
    X = std.fit_transform(X[X.columns])
    X2_test = std.fit_transform(X2_test[X2_test.columns])
    
    # reshape the features to 3 dimensions [batch size, timesteps, input dim]
    X = np.reshape(X, (X.shape[0],1, X.shape[1]))
    X2_test = np.reshape(X2_test, (X2_test.shape[0],1, X2_test.shape[1]))
    
    # make array to create predict results labels/IDs 
    test_ID = test_signal['ID']
    
    return X, y, X2_test, reverse_class_id, test_ID

# load data
X, y, X2_test, reverse_class_id, test_ID = load_data()

# creating call back
data_path  = 'data/ecg/lstm'
checkpointer = cb.ModelCheckpoint(filepath=data_path + '/model_{epoch:02d}', verbose=0)

# cross_valadate the model
print('-----------starting cross validation-------------')
# manually cross validation

"""
Code used to help develop the manual K fold validation ;
----------------------------------------------------------------- 
Evaluate the Performance Of Deep Learning Models in Keras;
Jason Browniee; 23/05/2019;

https://machinelearningmastery.com/evaluate-performance-
deep-learning-models-keras/?fbclid=IwAR1ki4pVIz8qngDQ24N1ckGqAv6b
-CeWRqwo0i44ryjYsl13A6ucReSq5dQ
-----------------------------------------------------------------
"""
# create the splitter for 3 fold validation
Kfold = StratifiedKFold(n_splits=3, shuffle=True, random_state=7) 
cv_scores = [] # used to record scores
# preset parameters
epochs = 500
batch_size = 20
test_num = 1 # record the test number
Kfold_y = y # copy y - to not alter the orginal values
is_categorical_y = False
# start cross validation
for train, test in Kfold.split(X,Kfold_y):
    # create model
    cv_model = Sequential()
    
    cv_model.add(l.Bidirectional(l.LSTM(20, input_shape=(1, 6000)
                     , return_sequences=True, activation='relu')))
    cv_model.add(l.Dropout(0.5))
    cv_model.add(l.LSTM(20, return_sequences=False, activation='relu'))
    cv_model.add(l.Dropout(0.5))
    #model.add(l.Flatten())
    cv_model.add(l.Dense(4, activation='softmax'))
    #opt = SGD(lr=0.01, momentum=0.9)
    cv_model.compile(loss='categorical_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
    # print k fold test number and increase for next run
    print("K-Fold Test {}".format(test_num))
    test_num = test_num + 1
    # change y to catagorical, have to do after the split
    # only do once to ensure not doing multiple to catagorical
    if not is_categorical_y:
        Kfold_y = to_categorical(Kfold_y)
        is_categorical_y = True # ensures only occurs once
    # fir the cross validation model
    cv_model.fit(X[train], Kfold_y[train], epochs=epochs, batch_size=batch_size, callbacks=[checkpointer], verbose=0)
    # evaluate the score
    score = cv_model.evaluate(X[test], Kfold_y[test], verbose=0)
    # add to cv scores
    cv_scores.append(score[1]*100)
# print the overall scores as percentages
print("Scores : ")
print(cv_scores)
print('-----------ending cross validation-------------')

# convert y to catagorical
y = to_categorical(y)
# create same model as the one in the cross validation section
model = Sequential()

model.add(l.Bidirectional(l.LSTM(20, input_shape=(1, 6000)
                 , return_sequences=True, activation='relu')))
model.add(l.Dropout(0.5))
model.add(l.LSTM(20, return_sequences=False, activation='relu'))
model.add(l.Dropout(0.5))
#model.add(l.Flatten())
model.add(l.Dense(4, activation='softmax'))
#opt = SGD(lr=0.01, momentum=0.9)
model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
              
# make 80/20 split - to generate testing and training data. From known values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, train_size = 0.8)


# fit the model
model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[checkpointer], verbose=0)

# evaluate model
# make prediction
y_pred = model.predict(X_test)
y_pred = [np.argmax(pred) for pred in y_pred]
y_test = [np.argmax(test) for test in y_test]

# compare results
print(classification_report(y_test, y_pred))
print(metrics.confusion_matrix(y_test, y_pred))

# make prediction for testing signal data
y_pred = model.predict(X2_test)
# reverse keys back to NAO~
y_pred = [np.argmax(pred) for pred in y_pred]
#y_pred = y_pred.replace(reverse_class_id)
for i, y in enumerate(y_pred):
    y_pred[i] = reverse_class_id[y]

# collect results

output = [['ID','Predicted']]

# convert to 2D array to be sent to csv file
for i in range(0, len(y_pred)):
    output.append([test_ID[i], y_pred[i]])

# write csv file
with open('assignment_LSTM_results.csv', 'w') as writeFile:
    write = csv.writer(writeFile)
    write.writerows(output)
    
writeFile.close()

