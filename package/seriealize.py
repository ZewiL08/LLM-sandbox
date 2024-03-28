

def str_convert(data) :
    final_str = ""
    for elt in data :
        str_number = str(round(elt))
        final_str = final_str + str_number + ", "
    return final_str

def basic_seriealize(list_response) :
    dic_int_list = []
    for elt in list_response :
        try :
            sub_chains = elt.split(',')
            int_list = [int(sub_chain.strip()) for sub_chain in sub_chains]
            if (len(int_list) > 7) :
                int_list = int_list[:7]
            elif (len(int_list) < 7) :
                last_numb = int_list[-1]
                while (len(int_list) < 7) :
                    int_list.append(last_numb)
            dic_int_list.append(int_list)
        except :
            print("error in serialization")
            continue
    return dic_int_list


def bin_seriealize(list_response) :
    final_dic_int_list = []
    for elt in list_response :
        try :
            sub_chains = elt.split(',')
            dic_int_list = []
            for sub_chain in sub_chains :
                without_space = sub_chain.replace(" ", "")
                if (without_space == "U2") :
                    dic_int_list.append(1)
                elif (without_space == "U4") :
                    dic_int_list.append(3)
                elif (without_space == "U6") :
                    dic_int_list.append(5)
                elif (without_space == "U8") :
                    dic_int_list.append(7)
                elif (without_space == "U10") :
                    dic_int_list.append(9)
                elif (without_space == "U10+") :
                    dic_int_list.append(11)
                elif (without_space == "D2") :
                    dic_int_list.append(-1)
                elif (without_space == "D4") :
                    dic_int_list.append(-3)
                elif (without_space == "D6") :
                    dic_int_list.append(-5)
                elif (without_space == "D8") :
                    dic_int_list.append(-7)
                elif (without_space == "D10") :
                    dic_int_list.append(-9)
                elif (without_space == "D10+") :
                    dic_int_list.append(-11)
                else :
                    print("error : ", without_space)

            if (len(dic_int_list) > 7) :
                dic_int_list = dic_int_list[:7]
            elif (len(dic_int_list) < 7) :
                last_numb = dic_int_list[-1]
                while (len(dic_int_list) < 7) :
                    dic_int_list.append(last_numb)
            final_dic_int_list.append(dic_int_list)
        except :
            print("error in seriealization : ")
            continue
    
    return final_dic_int_list

def convert_bin_to_close(final_dic_int_list, df_raw, input_length) :
    final_dic = []
    col_index = df_raw.columns.get_loc('close')
    row_index = input_length - 1
    close = df_raw.iloc[row_index, col_index]
    for elt_l in final_dic_int_list :
        memory = close
        dic = []
        for elt in elt_l :
            dic.append(int(memory * (1 + 0.01* elt)))
            memory = dic[-1]
        final_dic.append(dic)
    return final_dic
        
def convert_return_to_close(final_dic_int_list, df_raw, input_length) :
    final_dic = []
    col_index = df_raw.columns.get_loc('close')
    row_index = input_length - 1
    open = df_raw.iloc[row_index, col_index]
    for elt_l in final_dic_int_list :
        memory = open
        dic = []
        for elt in elt_l :
            dic.append(float((elt/10000 + 1) * memory))
            memory = dic[-1]
        final_dic.append(dic)
    return final_dic