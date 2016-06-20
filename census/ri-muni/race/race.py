import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg


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

# Clean municipality data
data = cd.clean_data('ACS_14_5YR_B03002_with_ann.csv')
data_new = data[GEO_COLUMNS + sorted(RACES)]
data_new.rename(columns=RACES, inplace=True)

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
def calc_pct(row): return row[race]/float(row['total'])
for race in RACE_LIST:
    if race != 'total':
        data_new['pct_' + race] = data_new.apply(calc_pct, axis=1)
        data_agg['pct_' + race] = data_agg.apply(calc_pct, axis=1)

# Export to CSV
data_new.to_csv('race_munis.csv', index=False)
data_agg.to_csv('race_areas.csv', index=True)
