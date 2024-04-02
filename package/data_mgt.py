import pandas as pd
import darts.datasets

from datetime import datetime, timedelta
import pickle
import copy

from package.query import *
from package.plot import *
from package.seriealize import *
from package.dic_mgt import *

dic_dataSet = ["bitcoin", "bitcoin_return", "AirPassenger", "Istanbul"]
dic_mode = ["naive", "return", "bin"]

def make_prediction(mode, data , setup = None, model = "gpt-4-vision-preview") :
    if mode == "naive" :
        make_prediction_naive(data , setup , model)
    elif mode == "return" :
        make_prediction_return(data , setup , model)
    elif mode == "bin" :
        make_prediction_bin(data , setup , model)
    else :
        print("The mode does not exist. Existing mode are : ")
        for elt in dic_mode :
            print(elt)

def make_prediction_naive(data , setup = None, model = "gpt-4-vision-preview") :
    
    savefig = "naive/"
    index_save = 0
    dic_error = get_basic_dic()
    dic_error_median = get_basic_dic()

    if setup == None :
        ending_predict_date = '2023-11-01'
        ending_dates = ['2023-11-04', '2023-11-06', '2023-11-08']   
        list_input_length = [6, 12, 24, 48, 96, 192]
    else :
        ending_predict_date = setup["ending_predict_date"]
        ending_dates = setup["ending_dates"]
        list_input_length = setup["list_input_length"]

    for input_length in list_input_length :

        start_date, end_date = convert_date_good(input_length, ending_predict_date, ending_dates)

        df_raw, train, test = get_the_data( data, input_length, start_date, end_date)
        input_str = str_convert(train.values)

        print("Input str : ", input_str)
        list_response = request_gpt(input_str)
        print("GPT Answer : ", list_response)

        final_dic_int_list = basic_seriealize(list_response)
        print("serialized list : ", final_dic_int_list)

        compute_error(final_dic_int_list, df_raw, input_length,  dic_error, dic_error_median)
        
        index_save += 1
        current_folder = savefig + str(index_save)
        plot_preds_candles(df_raw, train, final_dic_int_list, "gpt-4-vision-preview", savefig = current_folder)

    with open('pickle/dic_error_naive.pkl', 'wb') as fichier:
        pickle.dump(dic_error, fichier)

    with open('pickle/dic_error_naive_median.pkl', 'wb') as fichier:
        pickle.dump(dic_error_median, fichier)


def make_prediction_return(data , setup = None, model = "gpt-4-vision-preview") :
    
    savefig = "return/"
    index_save = 0
    dic_error = get_basic_dic()
    dic_error_median = get_basic_dic()
    
    if setup == None :
        ending_predict_date = '2023-11-01'
        ending_dates = ['2023-11-04', '2023-11-06', '2023-11-08']   
        list_input_length = [6, 12, 24, 48, 96, 192]
    else :
        ending_predict_date = setup["ending_predict_date"]
        ending_dates = setup["ending_dates"]
        list_input_length = setup["list_input_length"]

    for input_length in list_input_length :

        start_date, end_date = convert_date_good(input_length, ending_predict_date, ending_dates)

        df_raw, train, test = get_the_data( data, input_length, start_date, end_date)
        input_str = str_convert(train.values)

        print("Input str : ", input_str)
        list_response = request_gpt(input_str)
        print("GPT Answer : ", list_response)

        dic_int_list = basic_seriealize(list_response)
        print("int list return")
        print(dic_int_list)
        
        final_dic_int_list = convert_return_to_close(dic_int_list, df_raw, input_length)
        print("int list, close")
        print(final_dic_int_list)

        compute_error(final_dic_int_list, df_raw, input_length, dic_error, dic_error_median)

        index_save += 1
        current_folder = savefig + str(index_save)
        plot_preds_candles(df_raw, train, final_dic_int_list, "gpt-4-vision-preview",  savefig = current_folder)


    with open('pickle/dic_error_return.pkl', 'wb') as fichier:
        pickle.dump(dic_error, fichier)

    with open('pickle/dic_error_return_median.pkl', 'wb') as fichier:
        pickle.dump(dic_error_median, fichier)


def make_prediction_bin(data , setup = None, model = "gpt-4-vision-preview") :
    
    savefig = "bin/"
    index_save = 0
    dic_error = get_basic_dic()
    dic_error_median = get_basic_dic()

    if setup == None :
        ending_predict_date = '2023-11-01'
        ending_dates = ['2023-11-04', '2023-11-06', '2023-11-08']   
        list_input_length = [6, 12, 24, 48, 96, 192]
    else :
        ending_predict_date = setup["ending_predict_date"]
        ending_dates = setup["ending_dates"]
        list_input_length = setup["list_input_length"]

    for input_length in list_input_length :

        start_date, end_date = convert_date_good(input_length, ending_predict_date, ending_dates)

        df_raw, train, test = get_the_data( data, input_length, start_date, end_date)
        input_str = str_convert(train.values)

        print("Input str : ", input_str)
        list_response = request_gpt(input_str)
        print("GPT Answer : ", list_response)

        final_dic_int_list = bin_seriealize(list_response)
        print("serialized : ", final_dic_int_list)

        final_dic_int_list = convert_bin_to_close(final_dic_int_list, df_raw, input_length)
        print("int list, close")
        print(final_dic_int_list)

        compute_error(final_dic_int_list, df_raw, input_length, dic_error, dic_error_median)

        index_save += 1
        current_folder = savefig + str(index_save)
        plot_preds_candles(df_raw, train, final_dic_int_list, "gpt-4-vision-preview", savefig= current_folder )


    with open('pickle/dic_error_bin.pkl', 'wb') as fichier:
        pickle.dump(dic_error, fichier)

    with open('pickle/dic_error_bin_median.pkl', 'wb') as fichier:
        pickle.dump(dic_error_median, fichier)


def convert_date_good(input_length, ending_predict_date, ending_dates) :
    ending_predict_date_num = datetime.strptime(ending_predict_date, '%Y-%m-%d')
    new_date = ending_predict_date_num - timedelta(days=input_length)

    start_date = new_date.strftime('%Y-%m-%d')
    end_date = ending_dates[-1]

    return (start_date, end_date)


def compute_error(final_dic_int_list, df_raw, input_length, dic_error, dic_error_median) :

    full_Mae_dict, full_Mse_dict = MAE_MSE_calculator(final_dic_int_list, df_raw, input_length)
    dic_error["input_length"][input_length]["Mae"] = full_Mae_dict.copy()
    dic_error["input_length"][input_length]["Mse"] = full_Mse_dict.copy()
    print("dic_error : ",dic_error)

    full_Mae_dict_median, full_Mse_dict_median = MAE_MSE_median_calculator(final_dic_int_list, df_raw, input_length)
    dic_error_median["input_length"][input_length]["Mae"] = full_Mae_dict_median.copy()
    dic_error_median["input_length"][input_length]["Mse"] = full_Mse_dict_median.copy()
    print("dic_error_median : ",dic_error_median)




def get_the_data(name, input_length, start_date = None, end_date = None) :
    if name == "bitcoin" :
        return get_data_set("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
    elif name == "bitcoin_return" :
        return get_data_set_return("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
    elif name == "AirPassenger" :
        return get_data_darts(input_length)
    elif name == "Istanbul" :
        return get_data_set_simple(input_length)
    else :
        print("Data set not found, available dataset : ")
        for elt in dic_dataSet :
            print(elt)





def get_data_set(name, input_length, start_date, end_date) :
    with open(name) as f:
        df = pd.read_csv(f, usecols=[0, 4], parse_dates=[0])
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        df = df.loc[mask]
        df['close'] = df['close'].astype(float)
        series = pd.Series(df['close'].values, index=df['date'])

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0])
        df_raw = df_raw.loc[mask]

        splitpoint = input_length
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]

    return (df_raw, train, test)

def get_data_set_return(name, input_length, start_date, end_date) :
    with open(name) as f:
        df = pd.read_csv(f, usecols=[0, 1, 4], parse_dates=[0])
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        df = df.loc[mask]
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['return'] = ((df['close'] / df['open']) - 1) * 10000
        df = df[['date', 'return']]

        series = pd.Series(df['return'].values, index=df['date'])

        splitpoint = input_length
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0])
        df_raw = df_raw.loc[mask]
        df_raw['close'] = df_raw['close'].astype(float)
        df_raw['open'] = df_raw['open'].astype(float)
        df_raw['return'] = ((df_raw['close'] / df_raw['open']) - 1) * 10000
        
    return (df_raw, train, test)


def get_data_set_simple(input_length) :
    with open('datasets/IstanbulTraffic.csv', 'rb') as f:
        df = pd.read_csv(f,  parse_dates=[0], names=['date', 'close'])
        df = df.head(input_length + 7)
        print(df)
        df['close'] = df['close'].astype(float)
        series = pd.Series(df['close'].values, index=df['date'])

        f.seek(0)
        df_raw = pd.read_csv(f, parse_dates=[0], names=['date', 'close'])
        df_raw = df_raw.head(input_length + 7)

    train = series.iloc[:input_length]
    test = series.iloc[input_length:]  

    return (df_raw, train, test)


def get_data_darts(input_length) :
    dsname = "AirPassengersDataset"
    darts_ds = getattr(darts.datasets,dsname)().load()
    
    df = darts_ds.pd_dataframe()
    df = df.head(input_length + 7)
    df = df.reset_index()
    df = df.rename(columns={"Month": "date", "#Passengers": "close"})

    df['close'] = df['close'].astype(float)

    series = pd.Series(df['close'].values, index=df['date'])
    train = series.iloc[:input_length]
    test = series.iloc[input_length:]  

    return (df, train, test)

