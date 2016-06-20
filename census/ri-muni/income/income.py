import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd


# Export municipality data
data = cd.clean_data('ACS_14_5YR_B19013_with_ann.csv')
data.drop('HD02_VD01', axis=1, inplace=True)
data.rename(columns={'HD01_VD01': 'med_hh_inc'}, inplace=True)
data.to_csv('income_munis.csv', index=False)

### Hold off on the catchment areas - it doesn't make sense to aggregate medians
##
### Generate catchment area data
##areas = pd.read_csv('../catchment_areas.csv', index_col='muni')
##areas.rename(columns={'muni': 'muni_short'}, inplace=True)
#### data.join(areas, on='muni_short')
##data['area'] = data['muni_short'].map(areas['area'])
