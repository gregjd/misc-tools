import sys
sys.path.append('../')
import process

INPUT = 'ACS_14_5YR_S0101_with_ann.csv'
OUTPUT = 'sex'
VAR_MAP = {'HC01_EST_VC01': 'total',
           'HC02_EST_VC01': 'male',
           'HC03_EST_VC01': 'female'}

process.process(INPUT, OUTPUT, VAR_MAP)
