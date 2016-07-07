import pandas as pd
from clean_metadata import clean_metadata
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']
AGES = [str(i) for i in range(100)] + ['100-104', '105-109', '110+']


def filter_metadata(sex='b'):  # for 'sex', you can use 'm' or 'f' if desired
    
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

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
data_new_w_pct = pct.add_percentages(data_new, AGES)
data_agg_w_pct = pct.add_percentages(data_agg, AGES)

# Export to CSV
data_new_w_pct.to_csv('age_all_munis.csv', index=False)
data_agg_w_pct.to_csv('age_all_areas.csv', index=True)