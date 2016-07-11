import pandas as pd
import sys
sys.path.append('../census/ri-muni/')
import aggregate as agg


def aggregate_all():

    with open('kidscount_folder.txt') as folder_file:
        folder = folder_file.read()
    files = pd.read_csv('files_to_run.csv', index_col='file')
    calc_fields = pd.read_csv('calculated_fields.csv')

    for name in files.index:
##        if name == 'Early_HeadStart_2015a.csv':
##            aggregate_file(folder, name, calc_fields, files.loc[name, 'muni_field_name'])
        try:
            aggregate_file(folder, name, calc_fields,
                           files.loc[name, 'muni_field_name'])
        except Exception as e:
##            raise e
            print(e,)
            print('No result file saved.\n')
    print('Completed all files.')

    return

def aggregate_file(folder, file_name, calc_fields, muni_field_name,
                   new_file_name=None,
                   agg_file_path='../census/ri-muni/catchment_areas.csv'):

    print('Opening: ' + file_name)
    data = pd.read_csv(folder + file_name, thousands=',')
##    print 'data:', data
    file_vars = _get_vars(calc_fields, file_name)

##    print 'field_name:', file_vars['field_name']
    data_clean = data.drop(file_vars['field_name'], axis=1)
##    print 'data_clean:', data_clean
    data_agg = agg.aggregate(data_clean, agg_file=agg_file_path,
                             on_left=muni_field_name)
    data_w_pct = _add_calculated_values(data_agg, file_vars)

    new_path = folder + (new_file_name or file_name.replace('.csv', '_agg.csv'))
    data_w_pct.to_csv(new_path, index=True)
    print('Saved: ' + new_path + '\n')

    return data_w_pct

def _get_vars(calc_fields, file_name):

    return calc_fields[calc_fields['dataset'] == file_name]

def _add_calculated_values(data_frame, file_vars):

    for var in file_vars.to_dict(orient='index').values():
##        print 'df1:', data_frame
        parameters = {'df': data_frame,
                      'numerator': var['numerator'],
                      'denominator': var['denominator'],
                      'multiplier': var['multiplier']}
##        print 'num:', parameters['numerator']
##        print 'denom:', parameters['denominator']
##        print 'mult:', parameters['multiplier']
##        print 'df2:', data_frame
        data_frame[var['field_name']] = _calc_value(**parameters)

    return data_frame

def _calc_value(df, numerator, denominator, multiplier=1):

    return multiplier * (df[numerator] / df[denominator])


if __name__ == '__main__':
    aggregate_all()
