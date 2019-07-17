#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:47:45 2019

@author: hmatthyseniv
"""
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

# Here we set how pandas will display its float/large numbers
pd.options.display.float_format = '{:.2f}'.format

# Master file 



def init_master_file(file_in, numerical_columns):
    #####LOAD AND CLEAN DATA
    # DataFrame containing the information for all subsidies 
    s_m_out = pd.read_csv(file_in) 
    # Now we clean up the data removing all special characters from subsidy values 
    s_m_out['Subsidy Value'].replace({'\$':'',',':''}, regex=True, inplace=True)
    # And then convert all them from strings to intergers
    for i in numerical_columns:
        s_m_out.iloc[:,i] = pd.to_numeric(s_m_out[s_m_out.columns[i]], errors='coerce')
    # Finally we can drop all rows containing empty subsidy values
    s_m_out.dropna(subset=['Subsidy Value',], inplace=True)
    
    #Now we can create a list of all the states/territories in the dataset. 
    list_of_states_out = s_m_out['State in Which Facility Is Located'].unique()    
    
    return s_m_out,list_of_states_out

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