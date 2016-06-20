import pandas as pd


def aggregate(data_file, agg_file='catchment_areas.csv',
              on_left='muni_short', on_right='muni', agg_var='area'):
    
    if (type(data_file) == str) or (type(data_file) == unicode):
        data_orig = pd.read_csv(data_file)
    elif type(data_file) == pd.DataFrame:
        data_orig = data_file
    else:
        d
    try:
        agg = pd.read_csv(agg_file)
    except IOError:
        try:
            agg = pd.read_csv('../' + agg_file)
        except IOError:
            raise IOError(agg_file + ' file not found.')
    agg_renamed = agg.rename(columns={on_right: on_left})
    data_joined = data_orig.merge(agg_renamed, how='left', on=on_left)
    data_grouped = data_joined.groupby(agg_var)

    data_agg = data_grouped.sum()
    try:
        data_agg.drop('geoID_short', axis=1, inplace=True)
    except ValueError:
        pass

    return data_agg
