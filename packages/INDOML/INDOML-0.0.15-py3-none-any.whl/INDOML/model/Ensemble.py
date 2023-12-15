import numpy as np
from statistics import mode

class Bagging:
    def __init__(self,model, n_model:int = 5,random_state:int=None):
        self.__model = model
        self.__label:np.ndarray = None
        self.__random_state = random_state
        self.__n_model = n_model
    
    def fit(self,x:np.ndarray,y:np.ndarray):

        if self.__random_state :
            np.random.seed(self.__random_state)
        record_x = [i for i in range(len(x))]
        predict_model = []

        for i in range(self.__n_model):
            data_x = []
            data_y = []
            for _  in range(len(x)):
                rd_c = np.random.choice(record_x,1,replace=True)
                data_x.append(x[rd_c])
                data_y.append(y[rd_c])
            obj = self.__model
            obj.fit(data_x,data_y)
            predict_model.append(obj)
            pred = obj.predict(x)
            print(
                f"model-{i+1} akurasi : {self.score_accuracy(pred,y)}"
            )

        
        predict = []
        for data in x:
            temp_predict = []
            for m in predict_model:
                temp_predict.append(m.predict(data))
            
            predict.append(mode(temp_predict))


        
        self.__label = np.array(predict)
    
    def fit_predict(self,x:np.ndarray,y:np.ndarray):
        self.fit(x,y)
        return self.__label
    
    def score_accuracy(self,y_pred:np.ndarray,y_true:np.ndarray):
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true/len(y_pred)


class Boosting:

    def __init__(self,model, n_model:int = 5,random_state:int=None):
        self.__model = model
        self.__n_model = n_model
        self.__random_state = random_state
        self.__label = None
    
    def fit(self,x:np.ndarray,y:np.ndarray):
        sample_weight = np.ones(len(x))/len(x)

        if self.__random_state :
            np.random.seed(self.__random_state)
        predict_model = []
        weight_model = []
        final_prediksi = None

        for i in range(self.__n_model):
            selected_indices = np.random.choice(len(x), size=len(x), p=sample_weight)
            data_x = [x[i] for i in selected_indices]
            data_y = [y[i] for i in selected_indices]
            data_x = np.array(data_x)
            data_y = np.array(data_y)
            obj = self.__model
            obj.fit(data_x,data_y)
            predict_model.append(obj)
            prediksi = obj.predict(x)
            error = np.sum(sample_weight * (prediksi != y))
            model_weight = 0.5 * np.log((1 - error) / error)
            weight_model.append(model_weight)
            sample_weight *= np.exp(-model_weight * y * prediksi)
            sample_weight /= np.sum(sample_weight)
            if final_prediksi == None:
                final_prediksi = model_weight*prediksi
            else:
                final_prediksi += model_weight*prediksi
            
            print(
                f"model-{i+1} akurasi : {self.score_accuracy(prediksi,y)}"
            )
            
        self.__label = np.argmax(final_prediksi,axis=1)
    
    def fit_predict(self,x:np.ndarray,y:np.ndarray):
        self.fit(x,y)
        return self.__label

    def score_accuracy(self,y_pred:np.ndarray,y_true:np.ndarray):
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true/len(y_pred)












            
            
            


            





        
