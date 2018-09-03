import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
from flatten_json import flatten
import ast
import json
import glob

filenames = glob.glob("/home/az/dev/atvisor/Test1-20180820/out_file_mappings_*.json")
appended_data = []
for file in filenames:
    f = open(file, 'r')
    d = json.loads(f.read())
    df = json_normalize(d)
    df = df.fillna(method='ffill')
    df = df.dropna()
    storage = []
    if 'excluded_symptoms' in df:
        for x in range(len(df['excluded_symptoms'].tolist()[0])):
            excluded_symptoms_data = df['excluded_symptoms'].tolist()[0][x]  # change to excluded or included symptoms
            severity = excluded_symptoms_data['sev']
            location = excluded_symptoms_data['loc']
            storage += [{"bf": excluded_symptoms_data['bf'],
                         "bs": excluded_symptoms_data['bs'],
                         "sev": severity,
                         "loc": location,
                         "mappings": filenames[x][54:58]}]
        test = pd.DataFrame(storage)
        if 'sev' in test:
            s = test['sev'].apply(ast.literal_eval)
            s1 = test['loc'].apply(ast.literal_eval)
            df1 = pd.concat([pd.DataFrame(x) for x in s], keys=s.index)
            df2 = pd.concat([pd.DataFrame(x) for x in s1], keys=s1.index).drop('title', 1).rename(
                {'value': 'loc_value'},
                axis=1)
            test = test.drop('sev', 1).join(df1.reset_index(level=1, drop=True)).reset_index(drop=True)

            df_new = test.drop('loc', 1).drop('title', 1).rename({'value': 'sev_value'}, axis=1)
            df_new = df_new.join(df2.reset_index(level=1, drop=True)).reset_index(drop=True)
        appended_data.append(df_new)
appended_data = pd.concat(appended_data, axis=0)
appended_data.to_csv('appended_mappings_excl.csv')

excluded = appended_data.drop_duplicates(appended_data.columns.difference(['mappings']))
excluded.to_csv('excluded_mappings_data.csv')

head_mappings = set(excluded['mappings'].values)
data = excluded['mappings']
test_new = pd.DataFrame(columns=head_mappings)
test_new['mappings'] = excluded['mappings'].values
test_new = test_new.set_index('mappings')

test_new.index.values
for y in test_new.index.values.tolist():
    for x in list(test_new):
        if x == y:
            test_new.loc[x, y] = 1
        else:
            test_new.loc[x, y] = 0

test_new.to_csv('matrix_excluded_mappings.csv')

