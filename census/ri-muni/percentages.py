import pandas as pd


def add_percentages(data_frame, var_list, total_var_name='total'):

    def calc_pct(var_name):
        def calc_pct_for_row(row):
            return float(row[var_name])/float(row[total_var_name])
        return calc_pct_for_row

    for var in var_list:
        if var != total_var_name:
            data_frame['pct_' + var] = data_frame.apply(calc_pct(var), axis=1)

    return data_frame
