import pandas as pd
import sys
import cleandata as cd
import aggregate as agg
import percentages as pct


GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']

def process(input_file, output_name, var_map, calc=None, agg_areas=True):

    def _add_pct(data_frame):

        var_list = list(data_frame.columns)
        for var in GEO_COLUMNS + ['area']:
            if var in var_list:
                var_list.remove(var)
        
        return pct.add_percentages(data_frame, var_list, var_list[0])

    def _export(data_frame, suffix, include_index=False):

        full_name = output_name + '_' + suffix + '.csv'
        data_frame.to_csv(full_name, index=include_index)
        print('Saved file: ' + full_name)

        return

    # Clean municipality data
    data = cd.clean_data(input_file)
    data_new = data[GEO_COLUMNS + sorted(var_map.keys())]
    data_new = data_new.rename(columns=var_map)

    # Perform any extra necessary calculations
    if calc:
        data_new = calc(data_new)

    # Aggregate
    if agg_areas:
        data_agg = agg.aggregate(data_new)
        data_ri = agg.aggregate(data_new, agg_var=(lambda x: True))

    # Calculate percentages
    data_new_w_pct = _add_pct(data_new)
    if agg_areas:
        data_agg_w_pct = _add_pct(data_agg)
        data_ri_w_pct = _add_pct(data_ri.drop('area', axis=1))

    # Export to CSV
    _export(data_new_w_pct, 'munis')
    if agg_areas:
        _export(data_agg_w_pct, 'areas', include_index=True)
        _export(data_ri_w_pct, 'state')

    return (data_new_w_pct, data_agg_w_pct, data_ri_w_pct)
