import pandas

FILE_PATH = 'DEC_10_SF1_QTP2_with_ann.csv'

# Import data
# Note: will skip second row of header and replace '(X)' values with null
df0 = pandas.read_csv(FILE_PATH,
                      skiprows=[1],
                      na_values=['(X)'])

# Cut 'County subdivisions not defined' row
bad_place = 'County subdivisions not defined, Newport County, Rhode Island'
df1 = df0[df0['GEO.display-label'] != bad_place]

# Insert new column with clean municipality field
def get_muni(name):
    return name.split(', ')[0].replace(' city', '').replace(' town', '')
new_location = df1.columns.get_loc('GEO.display-label') + 1
df1.insert(loc=new_location,
                 column='muni_short',
                 value=df1['GEO.display-label'].map(get_muni))

# Rename first three columns
df2 = df1.rename(columns={'GEO.display-label': 'muni_long',
                          'GEO.id': 'geoID_long',
                          'GEO.id2': 'geoID_short'})

# Sort columns based on muni name
df3 = df2.sort_values('muni_short')

# Export to CSV
data = df3
data.to_csv(FILE_PATH.replace('_with_ann', '_reformatted'), index=False)
