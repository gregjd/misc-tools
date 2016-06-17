import pandas


df = pandas.read_csv('DEC_10_SF1_QTP2_metadata.csv',
                     skiprows=3, names=['id', 'desc'], header=None)
df['desc_split'] = df['desc'].map(lambda x: x.split(' - '))

# df_filtered = df[df['id'][0:2] != 'HD' and df['desc_split'][0:7] != 'Percent']



def filter_out_sex_ratio(data_frame):
    
    return data_frame.loc[data_frame['id'].str[0:2] != 'HD']

def filter_out_percents(data_frame):
    
    return data_frame.loc[data_frame['desc_split'].str[0] != 'Percent']

def filter_out_5yr_groups(data_frame):
    
    return data_frame.loc[data_frame['desc_split'].map(lambda x: len(x)) != 3]

def add_short_codes(data_frame):
    
    return

def split_and_map_sex(text):

    sex_map = {'Both sexes': 'b', 'Male': 'm', 'Female': 'f'}

    return sex_map[text.split('; ')]

##def calc_sex(data_frame):
##
##    sex_map = {'Both sexes': 'b', 'Male': 'm', 'Female': 'f'}
##    def split_and_map_sex(text): return sex_map[text.split('; ')]
##
##    data_frame['sex'] = 
##    
##    return data_frame

def calc_age():

    # 0, 1 ... 99, 100-104, 105-109, 110+
    
    return



# Filter out 'Males per 100 females' cases
# df_f1 = df.loc[df['id'].str[0:2] != 'HD']

# Filter out 'Percent' cases
# df_f2 = df_f1.loc[df_f1['desc_split'].str[0] != 'Percent']

# Filter out 5-year groupings (leaving only totals and individual years)
# df_f3 = df_f2.loc[df_f2['desc_split'].map(lambda x: len(x)) != 3]
