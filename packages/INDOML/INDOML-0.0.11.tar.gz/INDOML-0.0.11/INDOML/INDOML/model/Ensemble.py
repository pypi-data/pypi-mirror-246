import numpy as np
from statistics import mode

class Bagging:
    def __init__(self,model:list, random_state:int=None):
        self.__model = model
        self.__label:np.ndarray = None
        self.__random_state = random_state
    
    def fit(self,x:np.ndarray,y:np.ndarray):

        if self.__random_state :
            np.random.seed(self.__random_state)
        record_x = [i for i in range(len(x))]
        predict_model = {}
        predict = []

        for m in self.__model:
            data_x = []
            data_y = []
            for _  in range(len(x)):
                rd_c = np.random.choice(record_x,1,replace=True)
                data_x.append(data_x[rd_c])
                data_y.append(data_y[rd_c])
            
            m.fit_predict(x,y)
            predict_model[m.nama] = m.label__
        
        count = 0
        
        while count < len(x):
            temp_pred = []
            for key in predict_model.keys():
                temp_pred.append(predict_model[key][count])
            predict.append(mode(temp_pred))
            count += 1
        
        self.__label = np.array(predict)
    
    def fit_predict(self,x:np.ndarray,y:np.ndarray):
        self.bagging_fit(x,y)
        return self.__label

        
            
            
            


            





        
