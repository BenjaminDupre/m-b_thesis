def get_one_feedback_per_trail(dataf):
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()

    # Remove duplicate feedback types based on the specified conditions
    for index, feedback_types in unique_feedback_types.items():
        ptcp, set_val, level_counter = index
        feedback_types = feedback_types[np.isin(feedback_types, ['incongruent', 'none', 'congruent'])]
        if level_counter != 0 and feedback_types.size > 1:
            previous_level_counter = level_counter - 1
            previous_feedback_types = unique_feedback_types.get((ptcp, set_val, previous_level_counter))
            if previous_feedback_types is not None :
                if previous_feedback_types.size==1:
                    last_element = previous_feedback_types
                elif previous_feedback_types.size > 1:
                    last_element = np.asarray(previous_feedback_types)[-1]
                else:
                    last_element = None
            if last_element is not None and feedback_types[0] == last_element :
                feedback_types = feedback_types[1:]
        elif level_counter == 0  and feedback_types.size > 1:
            feedback_types = feedback_types[feedback_types != 'none']
        unique_feedback_types[index] = feedback_types
        feedback_df=unique_feedback_types.reset_index() 

    return feedback_df

get_one_feedback_per_trail(f_ptcp_df)
feedback_df
yogurt= feedback_df.index.names 
print(yogurt)

