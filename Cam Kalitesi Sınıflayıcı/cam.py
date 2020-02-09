import pandas as pd
import numpy as np

data=pd.read_csv('glass.csv')


X=data.iloc[:,:9].values
Y=data.iloc[:,-1].values

# slice data 
from sklearn.model_selection import train_test_split
x_train, x_test,y_train,y_test = train_test_split(X,Y,test_size=0.33, random_state=0)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)


#%% 2.CELL

#1- Decision Tree

# create models
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf.fit(x_train,y_train)
#PREDİCT
y_pred_dt=clf.predict(x_test)

# DT picture
tree.plot_tree(clf.fit(x_train,y_train))

#TESTİNG
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred_dt)
print(cm)
from sklearn.metrics import accuracy_score
print('\n DT Başarı Oranı:',accuracy_score(y_test,y_pred_dt))       #0.66
#%%   3.CELL

# 2-KNN 

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=7,weights='distance')
knn.fit(x_train,y_train)
#PREDİCT
y_pred_knn=knn.predict(x_test)


#Score
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred_dt)
print(cm)
from sklearn.metrics import accuracy_score
print('\n KNN Başarı Oranı:',accuracy_score(y_test,y_pred_knn))      #0.70


#%%     4.CELL

# 3- Naive Bayes Classifier

from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train,y_train)
#PREDİCT
y_pred_naive=gnb.predict(X_test)

#Score
from sklearn.metrics import confusion_matrix
cm=confusion_matrix(y_test,y_pred_dt)
print(cm)
from sklearn.metrics import accuracy_score
print('\n Naive Bayes Başarı Oranı:',accuracy_score(y_test,y_pred_dt))      #0.66

#%%     5.CELL
# 4- Neural network models(Sklearn)

from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='adam', activation='relu',alpha=1e-5,
                    hidden_layer_sizes=(7,1), random_state=66,max_iter=90000)

clf.fit(X_train,y_train)
#PREDİCT
y_pred_nn=clf.predict(X_test)

#Score

from sklearn.metrics import accuracy_score
print('\n  Neural network Başarı Oranı:',accuracy_score(y_test,y_pred_nn))  #0.64

#%%

#Result
result_data={
     'Decision Tree':[accuracy_score(y_test,y_pred_dt)],
     'KNN':[accuracy_score(y_test,y_pred_knn)],
     'Naive Bayes':[accuracy_score(y_test,y_pred_naive)],
     'Neural network':[accuracy_score(y_test,y_pred_nn)]
     }

Result_table=pd.DataFrame(result_data,columns =['Decision Tree','KNN','Naive Bayes','Neural network'])

print(Result_table)





