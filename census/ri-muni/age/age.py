import pandas as pd
from clean_metadata import clean_metadata
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']
AGE_GROUPS = {'0-1': ('0', '1'),
              '2-4': ('2', '4'),
              '5-12': ('5', '12'),
              '13-18': ('13', '18'),
              '19-25': ('19', '25'),
              '26-64': ('26', '64'),
              '65+': ('65', '110+')}
ORDERED_AGE_GROUPS = ['0-1', '2-4', '5-12', '13-18', '19-25', '26-64', '65+']


def filter_metadata(sex='b'):  # for 'sex', you can use 'm' or 'f' if desired
    
    meta = clean_metadata()
    meta_filtered = meta.loc[meta['sex'] == sex]
    meta_with_id = meta_filtered.set_index('id')
    meta_fewer_cols = meta_with_id.drop(['desc', 'sex'], axis=1)
    
    return meta_fewer_cols['age']


# Clean municipality data
data = cd.clean_data('DEC_10_SF1_QTP2_with_ann.csv')
meta = filter_metadata()
data_new = data[GEO_COLUMNS + meta.index.tolist()]
data_new = data_new.rename(columns=meta.to_dict())

# Calculate age group summaries
for g in ORDERED_AGE_GROUPS:
    data_new[g] = data_new.loc[:, AGE_GROUPS[g][0]:AGE_GROUPS[g][1]].sum(axis=1)

# Drop unneeded variables
data_new_with_extras = data_new
cols_to_keep = GEO_COLUMNS + ['total'] + ORDERED_AGE_GROUPS
data_new = data_new[cols_to_keep]

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
data_new_w_pct = pct.add_percentages(data_new, ORDERED_AGE_GROUPS)
data_agg_w_pct = pct.add_percentages(data_agg, ORDERED_AGE_GROUPS)

# Export to CSV
data_new_w_pct.to_csv('age_munis.csv', index=False)
data_agg_w_pct.to_csv('age_areas.csv', index=True)
