import numpy as np
from tabulate import tabulate
import pickle

dic_mode = ["naive", "return", "bin"]

def MAE_MSE_calculator(pred_dict, df_raw, index) :
    full_Mae_dict = []
    full_Mse_dict = []
    col_index = df_raw.columns.get_loc('close')


    for list_elt in pred_dict :
        Mae_dict = []
        Mse_dict = []

        for i,elt in enumerate(list_elt) :
            row_index = i + index
            Mae_dict.append(np.abs(elt - df_raw.iloc[row_index, col_index]))
            Mse_dict.append(np.square(elt - df_raw.iloc[row_index, col_index]))

        full_Mae_dict.append(Mae_dict)
        full_Mse_dict.append(Mse_dict)

    return full_Mae_dict, full_Mse_dict

def MAE_MSE_median_calculator(pred_dict, df_raw, index) :
    col_index = df_raw.columns.get_loc('close')

    medians = [sorted(sublist)[len(sublist)//2] if len(sublist) % 2 != 0 else
        (sorted(sublist)[len(sublist)//2 - 1] + sorted(sublist)[len(sublist)//2]) / 2
        for sublist in zip(*pred_dict)]  
        
    Mae_dict = []
    Mse_dict = []

    for i,elt in enumerate(medians) :
        row_index = i + index
        Mae_dict.append(np.abs(elt - df_raw.iloc[row_index, col_index]))
        Mse_dict.append(np.square(elt - df_raw.iloc[row_index, col_index]))

    return [Mae_dict], [Mse_dict]


def dic_mgt(dic_error, dic_error_3, dic_error_5, dic_error_7) :
    for elt in dic_error_3["input_length"].items() :
        list = dic_error["input_length"][elt[0]]["Mae"]
        sub_list_3 = []
        sub_list_5 = []
        sub_list_7 = []
        for sub_elt in list :
            sub_list_3.append(np.mean(sub_elt[:3]))
            sub_list_5.append(np.mean(sub_elt[:5]))
            sub_list_7.append(np.mean(sub_elt))

        dic_error_3["input_length"][elt[0]]["Mae"] = np.mean(sub_list_3)
        dic_error_5["input_length"][elt[0]]["Mae"] = np.mean(sub_list_5)
        dic_error_7["input_length"][elt[0]]["Mae"] = np.mean(sub_list_7)

        list = dic_error["input_length"][elt[0]]["Mse"]
        sub_list_3 = []
        sub_list_5 = []
        sub_list_7 = []
        for sub_elt in list :
            sub_list_3.append(np.mean(sub_elt[:3]))
            sub_list_5.append(np.mean(sub_elt[:5]))
            sub_list_7.append(np.mean(sub_elt))

        dic_error_3["input_length"][elt[0]]["Mse"] = np.mean(sub_list_3)
        dic_error_5["input_length"][elt[0]]["Mse"] = np.mean(sub_list_5)
        dic_error_7["input_length"][elt[0]]["Mse"] = np.mean(sub_list_7)



def table_display (dic_error_number) :
    table = []
    for key, value in dic_error_number['input_length'].items():
        row = [key, value['Mae'], value['Mse']]
        table.append(row)

    # En-tête du tableau
    headers = ['input_length', 'Mae', 'Mse']

    # Affichage du tableau
    print(tabulate(table, headers=headers))


def get_basic_dic() :
    dic = {"input_length" : {6: {"Mae": None, "Mse": None},
                                12: {"Mae": None, "Mse": None},
                                24: {"Mae": None, "Mse": None},
                                48: {"Mae": None, "Mse": None},
                                96: {"Mae": None, "Mse": None},
                                192: {"Mae": None, "Mse": None}}}
    return dic

def get_specific_dic(list_of_length) :

    dic = {"input_length" : {}}
    
    for elt in list_of_length :
        dic["input_length"][elt] = {"Mae": None, "Mse": None}
    return dic

def make_dic_MAE_MSE(path1, path2) :
    
    with open(path1, 'rb') as fichier:
        dict_error = pickle.load(fichier)

    with open(path2, 'rb') as fichier:
        dict_error_median = pickle.load(fichier)

    dic_error_3 = get_basic_dic()
    dic_error_5 = get_basic_dic()
    dic_error_7 = get_basic_dic()

    dic_error_3_median = get_basic_dic()
    dic_error_5_median = get_basic_dic()
    dic_error_7_median = get_basic_dic()

    print("dic_error :")
    print(dict_error)
    dic_mgt(dict_error, dic_error_3, dic_error_5, dic_error_7)
    dic_mgt(dict_error_median, dic_error_3_median, dic_error_5_median, dic_error_7_median)
    print(dic_error_3)

    return (dic_error_3, dic_error_5, dic_error_7, dic_error_3_median, dic_error_5_median, dic_error_7_median)


def display_tab(all_dic) :
    dic_error_3, dic_error_5, dic_error_7, dic_error_3_median, dic_error_5_median, dic_error_7_median = all_dic
    print("Global MAE/MSE")
    print("Mean error with 3 days forecasting")
    table_display(dic_error_3)
    print("Mean error with 5 days forecasting")
    table_display(dic_error_5)
    print("Mean error with 7 days forecasting")
    table_display(dic_error_7)

    print("##############################")
    print("Median MAE/MSE")
    print("Median error with 3 days forecasting")
    table_display(dic_error_3_median)
    print("Median error with 5 days forecasting")
    table_display(dic_error_5_median)
    print("Median error with 7 days forecasting")
    table_display(dic_error_7_median)
