
"""
THe main runtime for the different calls to state

"""
from state import *
import display 


# Initialization of master file 
csv_file = 'export_2018.csv'
numerical_columns_in = [6,8,9,10,11,12,16,23,24]

s_m,list_of_states = init_master_file(csv_file,numerical_columns_in)

print(s_m.loc[0:5,'Company'])


