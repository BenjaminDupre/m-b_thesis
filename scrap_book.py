def creating_close_trial(data):
    # Creating Close Index 
    num_rows = data.shape[0]
    C = np.zeros((num_rows - 1, 1))
    for r in range(num_rows - 1):
        C[r, 0] = data['levelCounter'].iloc[r + 1] != data['levelCounter'].iloc[r]
    # Assuming 'indx' is a numpy array of indices
    row_close = np.where(C[:, 0] == 1)[0]
    levelCounter_values = data.iloc[row_close]['levelCounter']
    trial_set_values = data.iloc[row_close]['trial_set']


    # Creating a new DataFrame to store the extracted values
    close_df = pd.DataFrame({
        'row_close': row_close,
        'levelCounter': levelCounter_values,
        'trial_set': trial_set_values
    })
    close_df.reset_index(drop=True, inplace=True)
    return close_df 

def get_one_feedback_per_trail(dataf,close_df):
    skip=False
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()
    # Remove duplicate feedback types based on the specified conditions
    for index, feedback_types in unique_feedback_types.items():
        ptcp, set_val, level_counter = index
        feedback_types = feedback_types[np.isin(feedback_types, ['incongruent', 'none', 'congruent'])]
        print(f'going through level {level_counter} and set {set_val}')
        if feedback_types.size==1:
            continue 
        if feedback_types.size > 1 and level_counter != 0:
            previous_level_counter = level_counter - 1
            if not skip:
                previous_feedback_types = unique_feedback_types.get((ptcp, set_val, previous_level_counter))
            else:
                previous_feedback_types=
            if previous_feedback_types is not None:
                if previous_feedback_types.size==1:
                    last_element = previous_feedback_types
                elif previous_feedback_types.size > 1:
                    last_element = np.asarray(previous_feedback_types)[-1]
                else:
                    last_element = None
            if last_element is not None and feedback_types[0] == last_element:
                feedback_types = feedback_types[1:]
        elif feedback_types.size > 1 and level_counter == 0:
            feedback_types = feedback_types[feedback_types != 'none']
        
        # WARNING: Last resource condition. Not to pro but effective
        # It check again the size of the feedbacktype 
        if  feedback_types.size > 1:
            print(f'WAS TRIGGERED in level {level_counter} and set {set_val}')
            row_n = close_df[(close_df['levelCounter'] == level_counter) & (close_df['trial_set'] == set_val)]['row_close']
            feedback_types = dataf.loc[row_n]['feedbackType']
            skip_= True    
        unique_feedback_types[index] = feedback_types

    feedback_df=unique_feedback_types.reset_index()
    feedback_df= pd.DataFrame(feedback_df) 

    return  feedback_df


close_df = creating_close_trial(f_ptcp_df)
payasadaoe = get_one_feedback_per_trail(f_ptcp_df,close_df)
payasadaoe.to_csv('clean_merged.csv')

