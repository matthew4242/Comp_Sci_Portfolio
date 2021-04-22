#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 18:19:26 2019

@author: mah60
"""
import pandas as pd
import numpy as np
import csv

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RandomizedSearchCV
from sklearn.impute import SimpleImputer
from sklearn import feature_selection as fs
from sklearn import metrics

# import training and test data
train_feat = pd.read_csv("./data/ecg/train_feat.csv")
test_feat = pd.read_csv("./data/ecg/test_feat.csv")

# determine the class
y = train_feat['Type']

# determine the individual features
features = [col for col in train_feat if col.startswith('F')]

# remove misclassified features
miss_class_feat = ['F158', 'F170', 'F171','F98','F100','F144','F181','F82','F184',
                   'F4','F3']
for f in miss_class_feat:
    features.remove(f)
X = train_feat[features]

# cleans missing values within the data
imp_freq = SimpleImputer(missing_values=np.NaN, strategy='most_frequent')
imp_freq.fit(X, y)
X = imp_freq.transform(X)

# apply feature selection techniques
selector = fs.SelectKBest(fs.f_classif, k=100)
selector.fit_transform(X,y)
col = selector.get_support(indices=True)
new_feat = []
for i in col:
    new_feat.append(features[i])

X = train_feat[new_feat]
# as new features clean null values
imp_freq = SimpleImputer(missing_values=np.NaN, strategy='most_frequent')
imp_freq.fit(X, y)
X = imp_freq.transform(X)

# check if both y and X are same size
if X.shape[0] != y.shape[0]:
    raise Exception("Sample counts do not align! Try again!")
# create classifier
# -----------------------------------------------
# find optimal hyperparameters
# create random grid for setting - 
random_grid = {
        'n_estimators': [10,50,100,150,200,250,300,350,400],
        'max_features': ['auto','sqrt'],
        'max_depth': [5,10,30,50,70, 80, 90],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1 ,2 ,4],
        'bootstrap': [True, False]
               }
# classifier , with optimal parameters from RandomizedSearchCV
clf = RandomForestClassifier(bootstrap=False, class_weight=None, criterion='gini',
                       max_depth=50, max_features='auto', max_leaf_nodes=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=300,
                       n_jobs=None, oob_score=False, random_state=0, verbose=0,
                       warm_start=False)
# RandomizedSearchCV used for grid search method and cross validation of each model
#rf_random_para = RandomizedSearchCV(estimator = clf, param_distributions=random_grid,
#                                    n_iter = 100, cv = 5, verbose=2, 
#                                    random_state=42, n_jobs = -1)
# -----------------------------------------------

# apply cross validation - to measure the value of the model
cross_validation = cross_validate(clf, X, y, cv=5) # gets samples from all the data
print("The 5-Fold Cross Validation Results are: {}".format(cross_validation['test_score']))

# make 80/20 split - to generate testing and training data. From known values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, train_size = 0.8)

# fit the data
clf.fit(X_train, y_train)
#print('-------------------------------------')
#print(rf_random_para.best_params_)
#print('-------------------------------------')
#print(rf_random_para.best_estimator_)
#print('-------------------------------------')
#print(rf_random_para.best_score_)
#print('-------------------------------------')

# make prediction
y_pred = clf.predict(X_test)

# compare results
print(classification_report(y_test, y_pred))
print(metrics.confusion_matrix(y_test, y_pred))

# get test data and apply preprocessing
X = test_feat[new_feat]

# remove null values, with SimpleImputer
X = imp_freq.transform(X)

# predict y using the classifier
y_pred = clf.predict(X) 

# collect results
output = [['ID','Predicted']]

# make 2D array to transfer to csv file
for test_id, predict in zip(test_feat['ID'], y_pred):
    #print(test_id)
    output.append([test_id, predict])

# write csv file
with open('assignment_RF_results.csv', 'w') as writeFile:
    write = csv.writer(writeFile)
    write.writerows(output)
    
writeFile.close()