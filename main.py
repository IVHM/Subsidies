
"""
THe main runtime for the different calls to state

"""
import state
from state import States
import display 
import interface


#### Initialization of master file

# file_in = 'path/to/file.csv'
csv_file = 'export_2018.csv'
numerical_columns_in = [6,8,9,10,11,12,16,23,24]

# This is just a DataFrame that contains the list of states and their abbreviations 
# and serves as an index for retrieving info from the instance master array
states_instance_dict = pd.read_csv('state_abbreviations.csv')


s_m, list_of_states, missing_data = state.init_master_file(csv_file,
                                                         numerical_columns_in)

# List of all instances of the state
state_instances = []

# This just tracks the total amount of money across all subsidies
total_of_all_subsidies = 0

# Here we intialize the instances of the state class into their master array
for state_name in states_instance_dict['State']:
    a = States(state_name)
    a.populate_data(s_m)
    total_of_all_subsidies += a.total_subsidies
    state_instances.append(a)



# #### USER INPUT

print(len(state_instances), states_instance_dict.shape[0])

while True:
    print("\n\n-----------------------------------------")
    print("Enter the name of the state you would like to\n",
          "see more information on.\n",
          "For list of all state data type (all).\n",
          "For a brief synopsis of state data type (brief).\n",
          "To quit type (q)",
          "For help_doc type (help)",
          "for missing data type (m)")
         
    choice = input("Enter choice:")
    if choice in ('q','Q','quit','Quit'):
        break
    #Lists full data about every state
    elif choice in ('all', 'All'):
        for state_name in state_instances:
            display.state_full(state_name)

    elif choice in ('brief', 'Brief'):
        for state_name in states_instance_dict.index:
            display.state_brief(state_instances[state_name])

    elif choice in ('missing', 'm', 'M' ):
        display.missing_data(missing_data)        

    elif choice in ('help','Help'):
        display.help_doc()
    # lists full data about a state by abbreviation

    elif choice in states_instance_dict.Abbreviation.values:
        index = states_instance_dict.index[states_instance_dict['Abbreviation']==choice]
        display.state_full(state_instances[index[0]])
    # Lists full data about a specfic state by name
    elif choice in states_instance_dict.State.values:
        index = states_instance_dict.index[states_instance_dict['State']==choice]
        display.state_full(state_instances[index[0]])
    else:
        print('invalid choice')
        
        