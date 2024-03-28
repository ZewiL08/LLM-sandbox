import numpy as np
from tabulate import tabulate

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

