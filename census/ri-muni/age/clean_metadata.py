import pandas


# Main function

def clean_metadata(file_path='DEC_10_SF1_QTP2_metadata.csv',
                   new_file_path='DEC_10_SF1_QTP2_metadata_clean.csv'):

    df = pandas.read_csv(file_path, skiprows=3,
                         names=['id', 'desc'], header=None)
    df_split = split_description(df)
    df_filter1 = filter_out_percents(filter_out_sex_ratio(df_split))
    df_w_ages = add_ages(df_filter1)
    df_filter2 = filter_out_5yr_groups(df_w_ages)
    df_w_sexes = add_sexes(df_filter2)

    df_w_sexes = df_w_sexes.drop('desc_split', axis=1)
    df_w_sexes.to_csv(new_file_path, index=False)

    return df_w_sexes


# Helper functions

def split_description(data_frame):

    data_frame['desc_split'] = data_frame['desc'].map(lambda x: x.split(' - '))

    return data_frame

def filter_out_sex_ratio(data_frame):
    
    return data_frame.loc[data_frame['id'].str[0:2] != 'HD']

def filter_out_percents(data_frame):
    
    return data_frame.loc[data_frame['desc_split'].str[0] != 'Percent']

def add_ages(data_frame):

    def calc_age(desc_split):

        old_age_ranges = {'100 to 104 years': '100-104',
                          '105 to 109 years': '105-109',
                          '110 years and over': '110+'}

        if len(desc_split) == 2:
            return 'total'
        elif len(desc_split) == 4:
            return desc_split[3].rstrip(' years').replace('Under 1', '0')
        elif len(desc_split) == 3:
            if desc_split[2] in old_age_ranges:
                return old_age_ranges[desc_split[2]]
            else:
                return 'GROUP5'
        else:
            raise Exception('Too many items in ' + desc_split)
            return ''

    data_frame['age'] = data_frame['desc_split'].map(calc_age)

    return data_frame

def filter_out_5yr_groups(data_frame):

    return data_frame.loc[data_frame['age'] != 'GROUP5']

def add_sexes(data_frame):

    def calc_sex(list_):

        sex_map = {'Both sexes': 'b', 'Male': 'm', 'Female': 'f'}

        return sex_map[list_[1].split('; ')[0]]

    # data_frame['sex'] = data_frame['desc_split'].str[1].map(calc_sex)
    
    data_frame['sex'] = data_frame['desc_split'].map(calc_sex)
    # data_frame['sex'] = data_frame['desc_split']

    return data_frame
