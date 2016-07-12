import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


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
data_new = data_new.rename(columns=RACES)

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
data_new_w_pct = pct.add_percentages(data_new, RACE_LIST)
data_agg_w_pct = pct.add_percentages(data_agg, RACE_LIST)

# Export to CSV
data_new_w_pct.to_csv('race_munis.csv', index=False)
data_agg_w_pct.to_csv('race_areas.csv', index=True)
