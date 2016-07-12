import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


VARS = {'HC01_EST_VC01': 'total',
        'HC02_EST_VC01': 'male',
        'HC03_EST_VC01': 'female'}
GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']

# Clean municipality data
data = cd.clean_data('ACS_14_5YR_S0101_with_ann.csv')
data_new = data[GEO_COLUMNS + sorted(VARS)]
data_new = data_new.rename(columns=VARS)

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
data_new_w_pct = pct.add_percentages(data_new, ['total', 'male', 'female'])
data_agg_w_pct = pct.add_percentages(data_agg, ['total', 'male', 'female'])

# Export to CSV
data_new_w_pct.to_csv('sex_munis.csv', index=False)
data_agg_w_pct.to_csv('sex_areas.csv', index=True)
