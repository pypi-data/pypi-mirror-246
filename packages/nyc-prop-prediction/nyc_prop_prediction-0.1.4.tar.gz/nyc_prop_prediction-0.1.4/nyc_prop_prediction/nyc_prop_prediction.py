import pandas as pd
import time
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn import tree
from sklearn.ensemble import GradientBoostingRegressor
from joblib import dump, load


class predict:
 
    def __init__(self):
        
        self.inputmodel_grad = load('./inputmodel_grad.joblib')
        self.zipmodel_grad = load('./zipmodel_grad.joblib')

    def predict_price(self,input_type,model,inputs):
        if input_type == "zipcode":
            if model == 'rf':
                return None#zipmodel_rf.predict(inputs)
            elif model =='gradient':
                return self.zipmodel_grad.predict(inputs)
        elif input_type == "data":
            if model == 'rf':
                return None#inputmodel_rf.predict(inputs)
            elif model =='gradient':
                return (self.inputmodel_grad).predict(inputs)
        else:
            return None