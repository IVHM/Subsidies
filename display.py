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
    
def help_doc():
    print('You can do this, just believe in yourself.')    
#def state_bar_graph():

def missing_data(missing_in):
    col = [missing_in.columns[0],missing_in.columns[1],missing_in.columns[2]]
    
    print('\n\n--------------------------------',
          '          Missing Data\n',
          '----------------------------------\n',
          '| ',col[0]  ,'|', col[1] ,'|', col[2],
          '|---------------------------------\n',
            
          )
    for i in missing_in.index:
        print(
          '| ',missing_in.loc[i,col[0]],': ',f'{missing_in.loc[i,col[1]]:.2f}',' | ',f'{missing_in.loc[i,col[2]]:.2f}','%'
              )
    