import sys
sys.path.append('../')
import process

INPUT = 'ACS_14_5YR_S1601_with_ann.csv'
OUTPUT = 'language'
VAR_MAP = {'HC01_EST_VC01': 'pop_5+',
           'HC02_EST_VC03': 'ne_very_pct',
           'HC03_EST_VC03': 'ne_less_pct',
           'HC01_EST_VC10': 'spanish',
           'HC01_EST_VC14': 'other_indo_euro',
           'HC01_EST_VC18': 'asian_pacific',
           'HC01_EST_VC22': 'other'}

def calc_and_drop(data_frame):

    # Calculate needed numbers
    # We need the numbers of people whose home language is English only ('eng_only'),
    # a non-English language and speak English 'very well' ('ne_very'), and
    # a non-English language and speak English 'less than very well' ('ne_less').
    # The numbers should sum to 'pop_5+'.
    OTHER_LANG = ['spanish', 'other_indo_euro', 'asian_pacific', 'other']
    data_frame['not_eng_only'] = sum([data_frame.loc[:,lang] for lang in OTHER_LANG])
    data_frame['eng_only'] = data_frame.loc[:,'pop_5+'] - data_frame.loc[:,'not_eng_only']
    data_frame['ne_very'] = (data_frame.loc[:,'not_eng_only'] *
                           data_frame.loc[:,'ne_very_pct'] * 0.01)
    data_frame['ne_less'] = (data_frame.loc[:,'not_eng_only'] *
                           data_frame.loc[:,'ne_less_pct'] * 0.01)

    # Drop unneeded variables
    # data_new_with_extras = data_frame
    TO_DROP = ['ne_very_pct', 'ne_less_pct', 'not_eng_only'] + OTHER_LANG
    result = data_frame.drop(TO_DROP, axis=1)

    return result

process.process(INPUT, OUTPUT, VAR_MAP, calc=calc_and_drop)




##
##
##import pandas as pd
##import sys
##sys.path.append('../')
##
##import cleandata as cd
##import aggregate as agg
##import percentages as pct
##
##
##VALUES = {'HC01_EST_VC01': 'pop_5+',
##          'HC02_EST_VC03': 'ne_very_pct',
##          'HC03_EST_VC03': 'ne_less_pct',
##          'HC01_EST_VC10': 'spanish',
##          'HC01_EST_VC14': 'other_indo_euro',
##          'HC01_EST_VC18': 'asian_pacific',
##          'HC01_EST_VC22': 'other'}
### 'ne_very_pct' and 'ne_less_pct' refer to the percent of people who
### speak a non-English language at home who speak English 'very well'
### and 'less than very well' (respectively); they add up to 100
##
##GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']
##
### Clean municipality data
##data = cd.clean_data('ACS_14_5YR_S1601_with_ann.csv')
##data_new = data[GEO_COLUMNS + sorted(VALUES)]
##data_new = data_new.rename(columns=VALUES)
##
### Calculate needed numbers
### We need the numbers of people whose home language is English only ('eng_only'),
### a non-English language and speak English 'very well' ('ne_very'), and
### a non-English language and speak English 'less than very well' ('ne_less').
### The numbers should sum to 'pop_5+'.
##OTHER_LANG = ['spanish', 'other_indo_euro', 'asian_pacific', 'other']
##data_new['not_eng_only'] = sum([data_new.loc[:,lang] for lang in OTHER_LANG])
##data_new['eng_only'] = data_new.loc[:,'pop_5+'] - data_new.loc[:,'not_eng_only']
##data_new['ne_very'] = (data_new.loc[:,'not_eng_only'] *
##                       data_new.loc[:,'ne_very_pct'] * 0.01)
##data_new['ne_less'] = (data_new.loc[:,'not_eng_only'] *
##                       data_new.loc[:,'ne_less_pct'] * 0.01)
##
### Drop unneeded variables
##data_new_with_extras = data_new
##TO_DROP = ['ne_very_pct', 'ne_less_pct', 'not_eng_only'] + OTHER_LANG
##data_new = data_new.drop(TO_DROP, axis=1)
##
### Aggregate
##data_agg = agg.aggregate(data_new)
##
### Calculate percentages
##PCT_LIST = ['eng_only', 'ne_very', 'ne_less']
##data_new_w_pct = pct.add_percentages(data_new, PCT_LIST, 'pop_5+')
##data_agg_w_pct = pct.add_percentages(data_agg, PCT_LIST, 'pop_5+')
##
### Export to CSV
##data_new_w_pct.to_csv('language_munis.csv', index=False)
##data_agg_w_pct.to_csv('language_areas.csv', index=True)
