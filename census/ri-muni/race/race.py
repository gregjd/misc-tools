import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd


RACES = {'HD01_VD01': 'total',
         'HD01_VD03': 'white',
         'HD01_VD04': 'black',
         'HD01_VD05': 'native',
         'HD01_VD06': 'asian',
         'HD01_VD07': 'pac',
         'HD01_VD08': 'other',
         'HD01_VD09': 'multi',
         'HD01_VD12': 'hispanic'}
RACE_LIST = [RACES[i] for i in sorted(RACES)]
GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']

# Export municipality data
data = cd.clean_data('ACS_14_5YR_B03002_with_ann.csv')
data_new = data[GEO_COLUMNS + sorted(RACES)]
data_new.rename(columns=RACES, inplace=True)
for race in RACE_LIST:
    if race != 'total':
def calc_pct(row): return row[race]/float(row['total'])
        data_new['pct_' + race] = data_new.apply(calc_pct, axis=1)
data_new.to_csv('race_munis.csv', index=False)
