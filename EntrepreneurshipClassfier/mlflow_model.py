import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from urllib.parse import urlparse
import logging
import warnings
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    data = pd.read_csv('datanew.csv')
    warnings.filterwarnings("ignore")
    x_train, x_test,y_train,y_test = train_test_split(data.iloc[:,:-1],data.iloc[:,-1],test_size=0.33, random_state=0)

    with mlflow.start_run():
        parameteres={
    'rf__C':np.arange(1.0,5,0.1),       
    'rf__kernel':['linear','poly','rbf','sigmoid'],
    'rf__degree':np.arange(3,15,1),
    'rf__gamma':['scale','auto']}


        pipe = Pipeline([('sc',StandardScaler()),('rf', svm.SVC())])
        grid = GridSearchCV(pipe, param_grid=parameteres, cv=5).fit(x_train,y_train)
        
        mlflow.log_param('rf__C', grid.best_params_['rf__C'])
        mlflow.log_param('rf__kernel', grid.best_params_['rf__kernel'])
        mlflow.log_param('rf__degree', grid.best_params_['rf__degree'])
        mlflow.log_param('rf__gamma', grid.best_params_['rf__gamma'])

        mlflow.log_metric('score',float(grid.score(x_test,y_test)))

        mlflow.log_metric('f1-score',f1_score(y_test,grid.predict(x_test)))

        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(grid, "model", registered_model_name="startup mind")
            
        else:
            mlflow.sklearn.log_model(grid, "model")