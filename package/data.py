from package.query import *
from package.plot import *
from package.data_mgt import *
from package.seriealize import *
from package.dic_mgt import *


class data :
    def __init__(self, mode = None, end = None, input_length = None, predict_interval = None) :
        self.name = None
        self.end_data = None
        self.start_data = None
        self.draw_function = None
        self.df_raw = None
        self.train = None
        self.input_length = None
        self.current_input_length = None
        self.convert_date = None

        if input_length is not None :
            self.input_length = input_length
            self.current_input_length = input_length[0]
        if end is not None:
            self.end_date = end
        if predict_interval is not None :
            self.predict_interval = predict_interval

        if mode is None or mode == "naive" :
            self.mode = "naive"
            self.serialize = basic_seriealize
        elif mode == "return" :
            self.mode = "return"
            self.serialize = return_seriealize
        elif mode == "bin" :
            self.mode = "bin"
            self.serialize = bin_seriealize
        else :
            print("Please define correctly your mode. It can be naive, bin or return. Naive mode has been choosen by default for the serialization")
            self.mode = "naive"
            self.serialize = basic_seriealize

    def seriealize(self, list_response) :
        return self.serialize(self, list_response)
    
    def set_seriealize(self, function_name) :
        self.seriealize = function_name

    def get_data(self, input_length, start_date = None, end_date = None) :
        pass
    

class bitcoin_data(data):
    def __init__(self, mode = None, end = None, input_length = None, predict_interval = None) :
        super().__init__(mode, end, input_length, predict_interval)
        self.name = "bitcoin"
        self.end_data = "2024-02-20"
        self.start_data = "2017-08-18"
        self.draw_function = plot_preds_candles
        self.convert_date = convert_date_good


        if input_length is None:
            self.input_length = [6, 12, 24, 48, 96, 192]
            self.current_input_length = 6

        if end is None:
            self.end_date = '2023-11-01'

        if predict_interval is None :
            self.predict_interval = [3, 5, 7]

        check_all_correct(self, self.start_data, True)


    def get_data(self, input_length, start_date = None, end_date = None) :
        if end_date is None:
            end_date = self.end_date
        if start_date is None:
            start_date = convert_date_good(input_length, end_date, self.predict_interval[-1])

        if not check_all_correct(self, start_date, True) :
            start_date = convert_date_good(input_length, end_date, self.predict_interval[-1])


        if self.mode == "naive" or self.mode == "bin" :
            df_raw, train = get_data_set("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
        elif self.mode == "return" :
            df_raw, train = get_data_set_return("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
        else :
            print("Please define correctly your mode. It can be naive, bin or return. Naive mode has been choosen by default for the data collection")
            df_raw, train = get_data_set("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
        
        self.df_raw = df_raw
        self.train = train


class dart_data(data):
    def __init__(self, mode = None, end = None, input_length = None, predict_interval = None) :
        super().__init__(mode, end, input_length, predict_interval)
        self.name = "AirPassengersDataset"
        self.start_data = "1949-01-01"
        self.end_data = "1960-12-01"
        self.draw_function = plot_pred_classic
        self.convert_date = convert_date_good_month

        if input_length is None:
            self.input_length = [6, 12, 24, 48, 96, 192]
            self.current_input_length = 6

        if end is None:
            self.end_date = '1958-12-01'
        if predict_interval is None :
            self.predict_interval = [3, 5, 7]

        check_all_correct(self, self.start_data, False)


    def get_data(self, input_length, start_date = None, end_date = None) :
        if end_date is None:
            end_date = self.end_date

        df_raw, train = get_data_darts(self, input_length, end_date)
        
        self.df_raw = df_raw
        self.train = train
