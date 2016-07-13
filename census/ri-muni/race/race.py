import sys
sys.path.append('../')
import process

INPUT = 'ACS_14_5YR_B03002_with_ann.csv'
OUTPUT = 'race'
VAR_MAP = {'HD01_VD01': 'total',
           'HD01_VD03': 'white',
           'HD01_VD04': 'black',
           'HD01_VD05': 'native',
           'HD01_VD06': 'asian',
           'HD01_VD07': 'pac',
           'HD01_VD08': 'other',
           'HD01_VD09': 'multi',
           'HD01_VD12': 'hispanic'}

process.process(INPUT, OUTPUT, VAR_MAP)
