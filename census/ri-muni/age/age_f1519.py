import pandas as pd
from clean_metadata import clean_metadata
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']
AGE_GROUPS = {'15-19': ('15', '19')}
ORDERED_AGE_GROUPS = ['15-19']


def filter_metadata(sex='f'):  # for 'sex', you can use 'm' or 'f' if desired
    
    meta = clean_metadata()
    meta_filtered = meta.loc[meta['sex'] == sex]
    meta_filtered.set_index('id', inplace=True)
    meta_filtered.drop(['desc', 'sex'], axis=1, inplace=True)
    
    return meta_filtered['age']


# Clean municipality data
data = cd.clean_data('DEC_10_SF1_QTP2_with_ann.csv')
meta = filter_metadata()
data_new = data[GEO_COLUMNS + meta.index.tolist()]
data_new.rename(columns=meta.to_dict(), inplace=True)

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
data_new_w_pct.to_csv('age_f1519_munis.csv', index=False)
# data_agg_w_pct.to_csv('age_f1519_areas.csv', index=True)
