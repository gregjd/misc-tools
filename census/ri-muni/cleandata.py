import pandas


# Main function

def clean_data(file_path):
    """Runs everything and exports a CSV."""

    orig_data = remove_bad_place(import_data(file_path))
    data = sort_munis(rename_columns(insert_short_muni(orig_data)))

    new_file_name = file_path.replace('_with_ann', '_reformatted')
    export_csv(data, new_file_name)

    return data


# Helper functions
# (Didn't name with underscores because they could maybe be useful elsewhere)

def import_data(file_path):
    """Imports the data from a CSV and returns a DataFrame.

    Note: will skip second row of header and replace '(X)' values with null."""

    data_frame = pandas.read_csv(file_path, skiprows=[1],
                                 na_values=['(X)', '-', '**'])

    return data_frame

def remove_bad_place(data_frame):
    """Returns a copy of the DataFrame with the
    'County subdivisions not defined' row removed."""

    bad_place = 'County subdivisions not defined, Newport County, Rhode Island'

    return data_frame[data_frame['GEO.display-label'] != bad_place]

def insert_short_muni(data_frame):
    """Returns a copy of the DataFrame with a new column with the clean
    municipality name."""

    def get_muni(name):
        
        return name.split(', ')[0].replace(' city', '').replace(' town', '')

    new_location = data_frame.columns.get_loc('GEO.display-label') + 1
    data_frame.insert(loc=new_location,
                      column='muni_short',
                      value=data_frame['GEO.display-label'].map(get_muni))

    return data_frame

def rename_columns(data_frame):
    """Returns a copy of the DataFrame with the first three columns renmaed."""

    new_columns = {'GEO.display-label': 'muni_long',
                   'GEO.id': 'geoID_long',
                   'GEO.id2': 'geoID_short'}
    
    return data_frame.rename(columns=new_columns)

def sort_munis(data_frame):
    """Returns a copy of the DataFrame with rows sorted by muni name."""

    return data_frame.sort_values('muni_short')

def export_csv(data_frame, new_file_name):

    data_frame.to_csv(new_file_name, index=False)

    return
