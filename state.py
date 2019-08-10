#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:47:45 2019

@author: hmatthyseniv
"""
import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# Here we set how pandas will display its float/large numbers
pd.options.display.float_format = '{:.2f}'.format


# ####LOAD AND CLEAN DATA

def init_master_file(file_in, numerical_columns):

    # DataFrame containing the information for all subsidies
    s_m_out = pd.read_csv(file_in, na_values=[' ', "\"\"","$0"])


    # Now we clean up the data removing all special characters from the values
    s_m_out['Subsidy Value'].replace({'\$': '', ',': ''},
                                     regex=True, inplace=True)
    
    # And then convert all them from strings to intergers
    for i in numerical_columns:
        s_m_out.iloc[:, i] = pd.to_numeric(s_m_out[s_m_out.columns[i]],
                                           errors='coerce')
    # Finally we can drop all rows containing empty subsidy values
  #  s_m_out.dropna(subset=['Subsidy Value'], inplace=True)
   # print("######### Dropna: \n", s_m_out,"\n\n\n")
    # Values to calculte row
    tot_subsidies = s_m_out.shape[0]
    tot_area = tot_subsidies * s_m_out.shape[1]
    tot_missing = 0

    missing_data = DataFrame()
    tmp_missing_data = []

    for column_name in s_m_out.columns:
        number_missing = s_m_out[column_name].isna().sum(axis=0)
        percent_missing = (number_missing/tot_subsidies)*100
        tot_missing += number_missing
        tmp_missing_data.append([column_name, number_missing, percent_missing])

    tmp_missing_data = [['Total', tot_missing,
                         tot_missing / tot_area]] + tmp_missing_data

    missing_data = DataFrame(tmp_missing_data,
                             columns=['Column Name',
                                      'Total Missing',
                                      'Percent Missing'],
                             index=['Total'] + list(s_m_out.columns))

    missing_data.astype('float32', errors='ignore', copy=False)

    return s_m_out, missing_data


# Class for organizing subsidy data by state
class States():

    def __init__(self, name_in):
        # The name of the state
        self.name = name_in

    def populate_data(self, s_m):
        # These are the different statistics about each state
        self.subsidy_types = Series()
        awarding_agencies = Series()
        awarding_agencies_amt = Series()
        self.awarding_agencies_stats = DataFrame()
        self.program_names = Series()

        # Will create a new index containg only the entries linked to the state
        self.reference_index = s_m.index[s_m['State in Which Facility Is Located']==self.name]

        # Here we just get the total number of subsides listed for this state
        self.number_of_subsidies = self.reference_index.shape[0]

        # This is where we can run any calculations for this category
        self.total_subsidies = 0
        for i in self.reference_index:
            crrnt_subsidy_value = s_m.at[i, 'Subsidy Value']

            # Here we are getting the values of each row(i) and adding it to
            #  the subsidy value total
            self.total_subsidies += crrnt_subsidy_value

            # Now we check for the kinvd of sibsidies and how many of them
            crrnt_type = s_m.at[i, 'Type of Subsidy']
            crrnt_awarding_agency = s_m.at[i, 'Awarding Agency']
            crrnt_program_name = s_m.at[i, 'Program Name']

            # Here we try to create and populate a dictionary of the different
            # catagories in the subsidies dataset
            if crrnt_type not in self.subsidy_types:
                self.subsidy_types[crrnt_type] = 1
            else:
                self.subsidy_types[crrnt_type] += 1
            if crrnt_awarding_agency not in awarding_agencies:
                awarding_agencies[crrnt_awarding_agency] = 1
                awarding_agencies_amt[crrnt_awarding_agency] = crrnt_subsidy_value
            else:
                awarding_agencies[crrnt_awarding_agency] += 1
                awarding_agencies_amt[crrnt_awarding_agency] += crrnt_subsidy_value
            if crrnt_program_name not in self.program_names:
                self.program_names[crrnt_program_name] = 1
            else:
                self.program_names[crrnt_program_name] += 1

        if self.total_subsidies != 0:
            self.avg_subsidy = self.total_subsidies / self.number_of_subsidies
        else:
            self.avg_subsidy = 0

        # Now we turn the two series of stats into a dtaframe
        self.awarding_agencies_stats = DataFrame([awarding_agencies.index,
                                                  awarding_agencies.values,
                                                  awarding_agencies_amt.values]).T
        self.awarding_agencies_stats.columns = ['Agency', 'Amt', 'Tot $ Amt']

        # Set all of our temporary dictionaries to their more permanent Series
        self.subsidy_types.sort_values(ascending=False, inplace=True)
        self.program_names.sort_values(ascending=False, inplace=True)
