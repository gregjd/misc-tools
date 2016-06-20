import pandas as pd


# Main function

def aggregate(data_file, agg_file='catchment_areas.csv',
              on_left='muni_short', on_right='muni', agg_var='area'):
    
    data_orig = _import_data(data_file)
    agg_groups = _get_agg_file(agg_file, on_left, on_right)
    
    data_joined = data_orig.merge(agg_groups, how='left', on=on_left)
    data_grouped = data_joined.groupby(agg_var)

    return _sum(data_grouped)


# Helper functions

def _import_data(data_file):
    
    if (type(data_file) == str) or (type(data_file) == unicode):
        return pd.read_csv(data_file)
    elif type(data_file) == pd.DataFrame:
        return data_file
    else:
        raise Exception('data_file must be of type str, unicode, or DataFrame.'
                        + '\nType found: ' + type(data_file))

def _get_agg_file(agg_file, on_left, on_right):

    try:
        agg = _import_data(agg_file)
    except IOError:
        try:
            agg = pd.read_csv('../' + agg_file)
        except IOError:
            raise IOError(agg_file + ' file not found.')
    agg_renamed = agg.rename(columns={on_right: on_left})

    return agg_renamed

def _sum(groupby_object):
    
    data_agg = groupby_object.sum()
    try:
        return data_agg.drop('geoID_short', axis=1)
    except ValueError:
        return data_agg
