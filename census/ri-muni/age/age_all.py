import pandas as pd
import clean_metadata as cm
import sys
sys.path.append('../')
import process

INPUT = 'DEC_10_SF1_QTP2_with_ann.csv'

AGE_GROUPS = {'0_1': ('0', '1'),
              '2_4': ('2', '4'),
              '5_12': ('5', '12'),
              '13_18': ('13', '18'),
              '19_25': ('19', '25'),
              '26_64': ('26', '64'),
              '65+': ('65', '110+')}
F1519_GROUP = {'15-19': ('15', '19')}

def _age_map(sex='b'):  # for 'sex', you can use 'm' or 'f' if desired
    
    meta = cm.clean_metadata()
    meta_filtered = meta.loc[meta['sex'] == sex]
    meta_with_id = meta_filtered.set_index('id')
    meta_fewer_cols = meta_with_id.drop(['desc', 'sex'], axis=1)
    
    return meta_fewer_cols['age'].to_dict()

def _group(age_groups_dict):

    def _group_function(data_frame):

        data_frame_1 = _reorder_columns(data_frame)
        data_frame_2 = _sum_age_groups(data_frame_1, age_groups_dict)
        data_frame_3 = _drop_cols(data_frame_2, age_groups_dict)

        return data_frame_3

    return _group_function

def _reorder_columns(data_frame):
    
    cols = (process.GEO_COLUMNS + ['total'] + [str(i) for i in range(100)] +
            ['100-104', '105-109', '110+'])

    return data_frame[cols]

def _sort_age_groups(dict_):

    def _to_int(num_str):

        try:
            num_int = int(num_str)
        except ValueError:
            try:
                num_int = int(num_str.split('-')[0])
            except ValueError:
                try:
                    num_int = int(num_str.split('+')[0])
                except ValueError:
                    num_int = ''

        return num_int

    return sorted(dict_, key=(lambda x: _to_int(dict_[x][0])))

def _sum_age_groups(data_frame, age_groups):

    data_frame_new = data_frame.copy()

    for g in _sort_age_groups(age_groups):
        age0 = age_groups[g][0]
        age1 = age_groups[g][1]
        data_frame_new[g] = data_frame.loc[:, age0:age1].sum(axis=1)

    return data_frame_new

def _drop_cols(data_frame, age_groups):

    cols_to_keep = (process.GEO_COLUMNS + ['total'] +
                    _sort_age_groups(age_groups))

    return data_frame[cols_to_keep]


process.process(INPUT, 'age_each', _age_map(),
                calc=_reorder_columns)
process.process(INPUT, 'age_groups', _age_map(),
                calc=_group(AGE_GROUPS))
process.process(INPUT, 'age_f1519', _age_map(sex='f'),
                calc=_group(F1519_GROUP), agg_areas=False)
