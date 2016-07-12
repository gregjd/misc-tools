import pandas as pd
import sys
sys.path.append('../')

import cleandata as cd
import aggregate as agg
import percentages as pct


VARS = {'HC01_EST_VC03': 'total_det',
        'HC02_EST_VC03': 'below_pov'}
# These numbers are out of the subset of people for whom
# poverty status is determined, which is most of the population.
GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']

# Clean municipality data
data = cd.clean_data('ACS_14_5YR_S1701_with_ann.csv')
data_new = data[GEO_COLUMNS + sorted(VARS)]
data_new = data_new.rename(columns=VARS)

# Aggregate
data_agg = agg.aggregate(data_new)

# Calculate percentages
data_new_w_pct = pct.add_percentages(data_new, ['below_pov'], 'total_det')
data_agg_w_pct = pct.add_percentages(data_agg, ['below_pov'], 'total_det')

# Export to CSV
data_new_w_pct.to_csv('child_poverty_munis.csv', index=False)
data_agg_w_pct.to_csv('child_poverty_areas.csv', index=True)
