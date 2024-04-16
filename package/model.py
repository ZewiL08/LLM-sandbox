from package.query import *
from package.seriealize import *
from package.dic_mgt import *
from statsmodels.tsa.arima.model import ARIMA


class model :
    def __init__(self) :
        self.name = None

    def predict(self, data, input_str) :
        pass

class gpt4(model) :
    def __init__(self) :
        self.name = "gpt-4-vision-preview"


    def predict(self, data) :
        train = data.train
        print("train :", train)
        input_str = str_convert(train.values)
        print("Input str : ", input_str)
        error = False
        try :
                list_response = request_gpt(input_str)
                print("GPT Answer : ", list_response)
        except Exception as e:
            print("An error occurred:", e)  
            error = True

        final_dic_int_list = data.seriealize(list_response)
        print("serialized list : ", final_dic_int_list)
        return final_dic_int_list, error
    

class base(model) :
    def __init__(self) :
        self.name = "base"

    def predict(self, data) :
        train = data.train
        print("train :", train)
        error = False
        final_dic_int_list = []

        try :
            final_dic_int_list = [round(train.values[-1]) for _ in range(7)]
        except Exception as e:
            print("An error occurred:", e)  
            error = True

        print("Last value get copied 7 times : ", final_dic_int_list)
        return [final_dic_int_list], error

class arima(model) :
    def __init__(self) :
        self.name = "arima"


    def predict(self, data) :
        train = data.train
        print("train :", train)
        error = False
        final_dic_int_list = []
        try :
            model = ARIMA(train.values, order=(1,1,1))
            fitted_model = model.fit()
            for _ in range(10) :
                predictions = fitted_model.forecast(steps=7)
                dic_int_list = [round(lot) for lot in predictions]
                final_dic_int_list.append(dic_int_list)
                print("Prédictions:", dic_int_list)

        except Exception as e:
            print("An error occurred:", e)  
            error = True

        print("final_dic_int_list : ", final_dic_int_list)
        return final_dic_int_list, error