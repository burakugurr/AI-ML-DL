import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import _pickle as cPickle

data = pd.read_csv('train.csv')
###################################################
# define train data
Y = data.iloc[:,-1]
X = data.iloc[:,0:20]
# define test data
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
# create classification model
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
# predict score
# 0(low cost), 1(medium cost), 2(high cost) and 3(very high cost)
target_names = ['low cost)','medium cost','high cost','very high cost']
print(classification_report(y_test, y_pred, target_names=target_names))
print("\n\nTRAIN ACCURACY: ",clf.score(X,Y),' TRAIN PROBA: ',clf.predict_proba(X)[:, 1])

# SAVE MODEL #
with open('mobclass.pkl', 'wb') as fid:
    cPickle.dump(clf, fid)

"""
<<<< READ MODEL >>>>
with open('my_dumped_classifier.pkl', 'rb') as fid:
    gnb_loaded = cPickle.load(fid)
"""
