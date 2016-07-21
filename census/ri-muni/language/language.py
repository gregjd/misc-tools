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
    data_frame['not_eng_only'] = sum([data_frame[lang] for lang in OTHER_LANG])
    data_frame['eng_only'] = data_frame['pop_5+'] - data_frame['not_eng_only']
    data_frame['ne_very'] = (data_frame['not_eng_only'] * data_frame['ne_very_pct'] * 0.01)
    data_frame['ne_less'] = (data_frame['not_eng_only'] * data_frame['ne_less_pct'] * 0.01)

    # Drop unneeded variables
    # data_new_with_extras = data_frame
    TO_DROP = ['ne_very_pct', 'ne_less_pct', 'not_eng_only'] + OTHER_LANG
    result = data_frame.drop(TO_DROP, axis=1)

    return result

process.process(INPUT, OUTPUT, VAR_MAP, calc=calc_and_drop)
