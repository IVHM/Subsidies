#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 21:12:47 2019

@author: hmatthyseniv

Module for displaying data
"""

def state_full(state_in):
    print('\n--------------------------------')
    print('      ',state_in.name)
    print('Total subsidy value :', f'${state_in.total_subsidies:,.2f}')
    print('Average subsidies   :', f'${state_in.avg_subsidy:,.2f}')
    print('Number of subsidies :', state_in.number_of_subsidies)
    print('-----Top Three Types-----')
    print(state_in.subsidy_types)
    print('----Awarding Agencies----')
    print(state_in.awarding_agencies_stats)
    print('----Program Names--------')
    print(state_in.program_names)

def state_brief(state_in):
    print('\n--------------------------------')
    print('      ',state_in.name)
    print('Total subsidy value :', f'${state_in.total_subsidies:,.2f}')
    print('Average subsidies   :', f'${state_in.avg_subsidy:,.2f}')
    print('Number of subsidies :', state_in.number_of_subsidies)    
#def state_bar_graph():
    
    