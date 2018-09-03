import ast
import glob
import json

import numpy as np
import pandas as pd
from flatten_json import flatten
from pandas.io.json import json_normalize

filenames = glob.glob("/home/az/dev/atvisor/Test1-20180820/out_file_mappings_*.json")
appended_data = []
for file in filenames:
    f = open(file, 'r')
    d = json.loads(f.read())
    df = json_normalize(d)
    df = df.fillna(method='ffill')
    df = df.dropna()
    storage = []
    for x in range(len(df['included_symptoms'].tolist()[0])):
        included_symptoms_data = df['included_symptoms'].tolist()[0][x]
        # print(included_symptoms_Falsedata['bf'], included_symptoms_data['bs'])
        severity = included_symptoms_data['sev']
        # print(included_symptoms_data['bf'])
        location = included_symptoms_data['loc']
        storage += [{"bf": included_symptoms_data['bf'],
                     "bs": included_symptoms_data['bs'],
                     "sev": severity,
                     "loc": location}]  # maybe add loc as a dict as well
    test = pd.DataFrame(storage)
    s = test['sev'].apply(ast.literal_eval)
    s1 = test['loc'].apply(ast.literal_eval)
    df1 = pd.concat([pd.DataFrame(x) for x in s], keys=s.index)
    df2 = pd.concat([pd.DataFrame(x) for x in s1], keys=s1.index).drop('title', 1).rename({'value': 'loc_value'},
                                                                                          axis=1)
    test = test.drop('sev', 1).join(df1.reset_index(level=1, drop=True)).reset_index(drop=True)

    df_new = test.drop('loc', 1).drop('title', 1).rename({'value': 'sev_value'}, axis=1)
    df_new = df_new.join(df2.reset_index(level=1, drop=True)).reset_index(drop=True)
    appended_data.append(df_new)
appended_data = pd.concat(appended_data, axis=0)
appended_data.to_csv('appended.csv')


