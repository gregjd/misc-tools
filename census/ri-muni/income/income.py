import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd


# Export municipality data
data = cd.clean_data('ACS_14_5YR_B19013_with_ann.csv')
data.drop('HD02_VD01', axis=1, inplace=True)
data.rename(columns={'HD01_VD01': 'med_hh_inc'}, inplace=True)
data.to_csv('income_munis.csv', index=False)
