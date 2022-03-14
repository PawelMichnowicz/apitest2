from lib2to3.pgen2.pgen import DFAState
import pandas as pd
import json
import re


def exact_model(my_list, brand="SAMSUNG"):

    if brand == 'SAMSUNG':
        galaxy_ind = my_list.index("GALAXY")

        if len(my_list[galaxy_ind+1]) == 1:
            model = my_list[galaxy_ind+1: galaxy_ind+4]
            return " ".join(model)
        if my_list[galaxy_ind+1] == "ULTRA" or my_list[galaxy_ind+1] == "FE":
            model = my_list[galaxy_ind+1: galaxy_ind+3]
            return " ".join(model)
        else:
            return my_list[galaxy_ind+1]

    if brand == 'APPLE':
        iphone_ind = my_list.index("IPHONE")

        if my_list[iphone_ind+2][0].isdigit():
            return my_list[iphone_ind+1]

        elif my_list[iphone_ind+3][0].isdigit():
            model = my_list[iphone_ind+1: iphone_ind+3]
            return " ".join(model)

        else:
            model = my_list[iphone_ind+1: iphone_ind+4]
            return " ".join(model)

    if brand == 'XIAOMI':
        xiaomi_ind = my_list.index("XIAOMI")

        for word in my_list:
            if word == '5G' or '/' in word:
                end_ind = my_list.index(word)
                break
        model = my_list[xiaomi_ind+1: xiaomi_ind+end_ind-1]
        if len(model) == 0:
            model = my_list[xiaomi_ind+1: xiaomi_ind+end_ind]

        return " ".join(model)


def shop_max(brand="SAMSUNG"):
    means = {}
    list_of_shops = ['avans', 'neo', 'xkom']
    for shop_name in list_of_shops:

        with open(f'json_files/{shop_name}_{brand}.json', 'r') as f:
            data = json.loads(f.read())

        df = pd.json_normalize(data, record_path=[brand])

        try:
            df['price'] = df.price.astype("int")
        except ValueError:
            df['price'] = df['price'].str.split(
                ',').apply(lambda x: x[0].replace(" ", ""))
            df['price'] = df.price.astype("int")

        df['split_name'] = df.name.str.upper().str.split(" ")
        df['model'] = df['split_name'].apply(exact_model,  args=[brand])
        df = df[['model', 'price']]

        df = df.groupby('model').mean().round(2)
        df. rename(columns={'price': shop_name}, inplace=True)
        means[shop_name] = df
    return pd.concat([means[shop_name] for shop_name in list_of_shops], axis=1, join="outer")
