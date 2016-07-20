import pandas as pd
import sys
import cleandata as cd
import aggregate as agg
import percentages as pct


GEO_COLUMNS = ['geoID_long', 'geoID_short', 'muni_long', 'muni_short']

def process(input_file, output_name, var_map, agg_areas=True):

    # Clean municipality data
    data = cd.clean_data(input_file)
    data_new = data[GEO_COLUMNS + sorted(var_map.keys())]
    data_new = data_new.rename(columns=var_map)

    # Other stuff: calc, drop

    # Aggregate
    if agg_areas:
        data_agg = agg.aggregate(data_new)

    # Calculate percentages
    var_list = [var_map[i] for i in sorted(var_map)]
    data_new_w_pct = pct.add_percentages(data_new, var_list, var_list[0])
    if agg_areas:
        data_agg_w_pct = pct.add_percentages(data_agg, var_list, var_list[0])

    # Export to CSV
    data_new_w_pct.to_csv(output_name + '_munis.csv', index=False)
    print('Saved file: ' + output_name + '_munis.csv')
    if agg_areas:
        data_agg_w_pct.to_csv(output_name + '_areas.csv', index=True)
        print('Saved file: ' + output_name + '_areas.csv')

    return (data_new_w_pct, data_agg_w_pct)
