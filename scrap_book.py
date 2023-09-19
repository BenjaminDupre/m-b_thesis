import pandas as pd
'''
def get_correct(data):
    A = pd.DataFrame(columns=['Set Number', 'Level Counter', 'correctCounter', 'Change Flag'])

    for line in range(data.shape[0] - 1):
        if data['correctCounter'][line + 1] != data['correctCounter'][line]:
            A.loc[line, 'Change Flag'] = line  # Use the line number as the flag value
            A.loc[line, 'Set Number'] = data['trial_set'][line]
            A.loc[line, 'Level Counter'] = data['levelCounter'][line]
            A.loc[line, 'correctCounter'] = data['correctCounter'][line]

    # Optionally, you can reset the index if needed
    correct_df = A.reset_index(drop=True)
    return correct_df
'''

##------------------------ second try 

A = f_ptcp_df[['trial_set', 'levelCounter', 'correctCounter']]

# Initialize a list to store unique DataFrames
unique_dfs = []

for index, row in A.iterrows():
    trial_set = row['trial_set']
    level_counter = row['levelCounter']
    correctCounter = row['correctCounter']

    # Create a DataFrame for the current unique values
    unique_df = pd.DataFrame({'trial_set': [trial_set], 'levelCounter': [level_counter], 'correctCounter': [correctCounter]})

    # Check if the unique DataFrame is not already in the list
    if not any(df.equals(unique_df) for df in unique_dfs):
        unique_dfs.append(unique_df)

# Concatenate all unique DataFrames into one DataFrame
unique_values_df = pd.concat(unique_dfs, ignore_index=True)