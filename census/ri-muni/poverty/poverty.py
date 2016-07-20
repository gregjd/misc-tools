import sys
sys.path.append('../')
import process

INPUT = 'ACS_14_5YR_S1701_with_ann.csv'
OUTPUT = 'poverty'
VAR_MAP = {'HC01_EST_VC01': 'total_det',
           'HC02_EST_VC01': 'below_pov'}
# These numbers are out of the subset of people for whom
# poverty status is determined, which is most of the population.

process.process(INPUT, OUTPUT, VAR_MAP)
