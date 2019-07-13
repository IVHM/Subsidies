#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 22:33:41 2019

@author: hmatthyseniv
"""
''' Structure of subsidies CSV columns
		0-Company					1-Parent Company 			2-Location
		3-City						4-County							5-Address	
		6-Zip							7-Project Description	8-NAICS 
		9-Industry Code		10-Year								11-Subsidy Value	
		12-Megadeal Contribution      					13-Subsidy Value Adjusted For Megadeal	
		14-Program name 	15-Awarding Agency		16-Type of Subsidy	
		17-Jobs/Training Slots							    18-Wage Data	
		19-Wage Data Type	20-Investment Data		21-Source of Data	
		22-Notes					23-Subsidy Source 		24-CFDA Program Number	
		25-Loan Value	 					26-State in Which Facility Is Located	
		27-HQ State of Parent										28-HQ	 Country of Parent	
		29-Ownership Structure									30-Major Industry of Parent		
		31-Specific Industry of Parent
'''


import numpy as np
import matplotlib as plt
import pandas as pd
from pandas import Series,DataFrame

# Here we set how pandas will display its float/large numbers
pd.options.display.float_format = '{:.2f}'.format


#file_in = 'path/to/file.csv'
file_in = 'export_2018.csv'
numerical_columns = [6,8,9,10,11,12,16,23,24]


#####LOAD AND CLEAN DATA
# DataFrame containing the information for all subsidies 
s_m = pd.read_csv(file_in) 
# Now we clean up the data removing all special characters from subsidy values 
s_m['Subsidy Value'].replace({'\$':'',',':''}, regex=True, inplace=True)
# And then convert all them from strings to intergers
for i in numerical_columns:
    s_m.iloc[:,i] = pd.to_numeric(s_m[s_m.columns[i]], errors='coerce')
# Finally we can drop all rows containing empty subsidy values
s_m.dropna(subset=['Subsidy Value',], inplace=True)

#Now we can create a list of all the states/territories in the dataset. 
list_of_states = s_m['State in Which Facility Is Located'].unique()
state_instances = []  

# Class for organizing subsidy data by state    
class States():
    
    def __init__(self,name_in):
        # The name of the state
        self.name = name_in
        #       
        
        # need to implement >>   self.industries = None
        
    def populate_data(self):
        # These are the different statistics about each state
        self.subsidy_types = Series()
        awarding_agencies = Series()
        awarding_agencies_amt = Series()
        self.awarding_agencies_stats = DataFrame()
        self.program_names = Series()
        
        
        # Will create a new index containg only the entries linked to the state
        self.reference_index = s_m.index[s_m['State in Which Facility Is Located']==self.name]
        
        # This is a second way to do it involving string matching, the plus to this method is it can take regex expressions
        #self.reference_index = s_m.index[s_m['State in Which Facility Is Located'].str.match(str(self.name))]
        
        # Here we just get the total number of subsides listed for this state            
        self.number_of_subsidies = self.reference_index.shape[0]


       
        self.total_subsidies = 0
        # This is where we can run any calculations for this category
        for i in self.reference_index:
            crrnt_subsidy_value =s_m.at[i,'Subsidy Value']
            # Here we are getting the values of each row(i) and adding it to the subsidy value total      
            self.total_subsidies += crrnt_subsidy_value
                 
            # Now we check for the kinvd of sibsidies and how many of them
            crrnt_type = s_m.at[i,'Type of Subsidy']
        
            # Here we try to create and populate a dictionary of the different catagories in the subsidies dataset
            if crrnt_type not in self.subsidy_types:
                self.subsidy_types[crrnt_type] = 1
            else:
                self.subsidy_types[crrnt_type] += 1
                
            crrnt_awarding_agency = s_m.at[i,'Awarding Agency']
            if crrnt_awarding_agency not in awarding_agencies:
                awarding_agencies[crrnt_awarding_agency] = 1
                awarding_agencies_amt[crrnt_awarding_agency] = crrnt_subsidy_value
            else:
                awarding_agencies[crrnt_awarding_agency] += 1
                awarding_agencies_amt[crrnt_awarding_agency] += crrnt_subsidy_value

            crrnt_program_name = s_m.at[i, 'Program Name']
            
            if crrnt_program_name not in self.program_names:
                self.program_names[crrnt_program_name] = 1
            else:
                self.program_names[crrnt_program_name] += 1
                
        
        self.avg_subsidy = self.total_subsidies / self.number_of_subsidies 

        # Now we turn the two series of stats into a dtaframe
        self.awarding_agencies_stats = DataFrame([awarding_agencies.index,awarding_agencies.values, 
                                                  awarding_agencies_amt.values]).T
        self.awarding_agencies_stats.columns = ['Agency','Amt','Tot $ Amt']       
        #Here we set all of our temporary dictionaries to their more permanent Series format
        self.subsidy_types.sort_values(ascending=False, inplace=True)
        self.program_names.sort_values(ascending=False, inplace=True)        
#'''
        
total_of_all_subsidies = 0
for j in list_of_states:
    a = States(j)
    a.populate_data()
    total_of_all_subsidies += a.total_subsidies
    state_instances.append(a)

print('--------------------------------')
print('Total of all subsidies:', f'${total_of_all_subsidies:,.2f}')
print('--------------------------------')

# Here we create a temporary list we'll append to before intiating the final DataFrame
# This is mainly because pandas doesn't handle appending lists as rows that well 
temp_states_subsidies_financial_plt = []
for i in state_instances:
    print('\n--------------------------------')
    print('      ',i.name)
    print('Total subsidy value :', f'${i.total_subsidies:,.2f}')
    print('Average subsidies   :', f'${i.avg_subsidy:,.2f}')
    print('Number of subsidies :', i.number_of_subsidies)
    print('-----Top Three Types-----')
    print(i.subsidy_types)
    print('----Awarding Agencies----')
    print(i.awarding_agencies_stats)
    print('----Program Names--------')
    print(i.program_names)
    
    if i.name != ' ':
        temp_states_subsidies_financial_plt.append([i.name,i.total_subsidies,i.avg_subsidy,i.number_of_subsidies])

states_subsidies_financial_plt = DataFrame(temp_states_subsidies_financial_plt, columns=['State','$Amt','$Avg','Num'])

print(states_subsidies_financial_plt)
states_subsidies_financial_plt.plot.bar(rot=0,subplots=True,x='State')
    
'''
foo = States('_')
foo.populate_data()
print(foo.reference_index)        
print(foo.total_subsidies)    
print(foo.number_of_subsidies)    
print(foo.avg_subsidy)   
''' 