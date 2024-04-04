import pandas as pd
import darts.datasets

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pickle
import copy

from package.query import *
from package.plot import *
from package.seriealize import *
from package.dic_mgt import *

dic_dataSet = ["bitcoin", "bitcoin_return", "AirPassenger", "Istanbul"]
dic_mode = ["naive", "return", "bin"]



def convert_date_good(input_length, end_date, predict_last_date) :
    ending_predict_date_num = datetime.strptime(end_date, '%Y-%m-%d')
    new_date = ending_predict_date_num - timedelta(days=input_length) - timedelta(days=predict_last_date)
    start_date = new_date.strftime('%Y-%m-%d')
    return start_date


def convert_date_good_month(input_length, end_date, predict_last_date) :
    
    ending_predict_date_num = datetime.strptime(end_date, '%Y-%m-%d')
    new_date = ending_predict_date_num - relativedelta(days=input_length) - relativedelta(days=predict_last_date)
    start_date = new_date.strftime('%Y-%m-%d')
    print("end date :", end_date)
    print("start date :", start_date)
    return start_date



def check_all_correct(data, start_date, day = True) :

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(data.end_date, '%Y-%m-%d')
    
    if day :
        diff = (end_date_obj - start_date_obj).days
    else :
        diff = (end_date_obj.year - start_date_obj.year) * 12 + (end_date_obj.month - start_date_obj.month)
    
    for i,input in enumerate(data.input_length) :
        if diff < input + data.predict_interval[-1] :
            print(f"Not enough data with the current preset. Starting date is set as {start_date}, ending date is set as {data.end_date}, input_length is set as {data.input_length} and the predict interval is set as {data.predict_interval}. So with these preset you need to have at least {diff} DataPoints available. The input_length has been troncatenated to {data.input_length[:i]}. Let's remember that for the current DataSet {data.name} the first dataPoint is {data.start_data} and the last DataPoint is {data.end_data}")
            data.input_length = data.input_length[:i]
            
            return False
    
    return True

def make_prediction(data , model = "gpt-4-vision-preview") :
    
    end_date = data.end_date
    list_input_length = data.input_length
    savefig = data.mode + "/" + data.name + "/"

    dic_error = get_specific_dic(list_input_length)
    dic_error_median = get_specific_dic(list_input_length)

    for input_length in list_input_length :
        data.current_input_length = input_length

        data.get_data(input_length, end_date)
        df_raw = data.df_raw
        train = data.train

        input_str = str_convert(train.values)
        print("Input str : ", input_str)

        try :
            list_response = request_gpt(input_str)
            print("GPT Answer : ", list_response)
        except Exception as e:
            print("An error occurred:", e)
            continue  

        final_dic_int_list = data.seriealize(list_response)
        print("serialized list : ", final_dic_int_list)

        compute_error(final_dic_int_list, df_raw, input_length,  dic_error, dic_error_median)
        
        index_save = input_length
        current_folder = savefig + str(index_save)
        data.draw_function(df_raw, train, final_dic_int_list, "gpt-4-vision-preview", savefig = current_folder)

    dic_name = "pickle/dic_error_" + data.mode + "_" + data.name + ".pkl"
    dic_name_median =  "pickle/dic_error_" + data.mode + "_" + data.name + "_median" + ".pkl"
    with open(dic_name, 'wb') as fichier:
        pickle.dump(dic_error, fichier)

    with open(dic_name_median, 'wb') as fichier:
        pickle.dump(dic_error_median, fichier)

    print("Two pickle files have been created one with MSE/MAE among all samples and the second with MSE/MAE among median only")
    print(f"The path for the pickle file are the following : ")
    print(dic_name)
    print(dic_name_median)


def compute_error(final_dic_int_list, df_raw, input_length, dic_error, dic_error_median) :

    full_Mae_dict, full_Mse_dict = MAE_MSE_calculator(final_dic_int_list, df_raw, input_length)
    dic_error["input_length"][input_length]["Mae"] = full_Mae_dict.copy()
    dic_error["input_length"][input_length]["Mse"] = full_Mse_dict.copy()
    print("dic_error : ",dic_error)

    full_Mae_dict_median, full_Mse_dict_median = MAE_MSE_median_calculator(final_dic_int_list, df_raw, input_length)
    dic_error_median["input_length"][input_length]["Mae"] = full_Mae_dict_median.copy()
    dic_error_median["input_length"][input_length]["Mse"] = full_Mse_dict_median.copy()
    print("dic_error_median : ",dic_error_median)




def get_the_data(data, input_length, start_date = None, end_date = None) :
    if data.name == "bitcoin" :
        return get_data_set("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
    elif data.name == "bitcoin_return" :
        return get_data_set_return("datasets/BTC_Daily_ohlc.csv", input_length, start_date, end_date)
    elif data.name == "AirPassenger" :
        return get_data_darts(input_length)
    elif data.name == "Istanbul" :
        return get_data_set_simple(input_length)
    else :
        print("Your request data set is : ", name)
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

    return (df_raw, train)

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
        
    return (df_raw, train)


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

    return (df_raw, train)


def get_data_darts(data, input_length, end_date) :

    predict_last_date = data.predict_interval[-1]
    start_date = data.convert_date(input_length, end_date, predict_last_date)

    print("start_date :", start_date)
    print("end_date : ", end_date)

    dsname = data.name
    darts_ds = getattr(darts.datasets,dsname)().load()
    
    df = darts_ds.pd_dataframe()
    df = df.reset_index()
    df = df.rename(columns={"Month": "date", "#Passengers": "close"})

    mask = (df["date"] >= start_date) & (df["date"] <= end_date)
    df = df.loc[mask]

    df['close'] = df['close'].astype(float)

    series = pd.Series(df['close'].values, index=df['date'])
    train = series.iloc[:input_length]
    print("train :", train)
    print("df :", df)

    return (df, train)

