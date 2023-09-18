import pandas as pd
def find_ball_position_changes(data):
    B = pd.DataFrame()
    for set_val in range(1, 4):
        for lvl in range(0, 36):
            meanwhile = data[(data['levelCounter'] == lvl) & (data['trial_set'] == set_val)]
            if meanwhile['buttonCurrentlyPressed'].nunique() >= 2 and data[(data['levelCounter'] == lvl - 1) & (data['trial_set'] == set_val)]['buttonCurrentlyPressed'].nunique() < 2:
                print(f"Button pressed in lvl {lvl} - set {set_val}. Need to go for following change of ball position.")
                A = np.zeros(len(meanwhile))
                A2 = np.zeros(len(meanwhile))
                A3 = np.zeros(len(meanwhile))
                for r in range(1, len(meanwhile)):
                    if sum(A) < 1:
                        A[r] = (meanwhile.iloc[r - 1]['buttonHasBeenPressed'] == "TEMPLATE_IS_ACTIVE") & (meanwhile.iloc[r]['buttonHasBeenPressed'] == 'AFTER_TEMPLATE_IS_ACTIVE')
                    else:
                        A2[r] = (meanwhile.iloc[r - 1]['buttonHasBeenPressed'] == "TEMPLATE_IS_ACTIVE") & (meanwhile.iloc[r]['buttonHasBeenPressed'] == 'AFTER_TEMPLATE_IS_ACTIVE')
                        if sum(A2) >= 1:
                            A3[r] = meanwhile.iloc[r - 1]['redBallPosition'] != meanwhile.iloc[r]['redBallPosition']
                            break
                A = np.concatenate(([0], A3))
                A2 = np.zeros(0)
                A3 = np.zeros(0)
            else:
                print(f"Normal way to Start lvl in lvl {lvl} - set {set_val}")
                A = np.zeros(len(meanwhile))
                for r in range(1, len(meanwhile)):
                    A[r] = meanwhile.iloc[r - 1]['redBallPosition'] != meanwhile.iloc[r]['redBallPosition']
            B = pd.concat([B, pd.DataFrame(A)], ignore_index=True)
    # Find the rows where the ball position changes (A == 1)
    indx = np.where(B.to_numpy()[:, 0] == 1)[0]
    # Create a dataframe 'ver' merging row_start, levelCounter, and set
    ver = pd.DataFrame({'row_start': indx, 'levelCounter': data.iloc[indx]['levelCounter'].astype(int), 'trial_set': data.iloc[indx]['trial_set'].astype(int)})
    # Merge level, set, and start into one dataframe 'START'
    START = pd.DataFrame()
    for j in range(data['trial_set'].min(), data['trial_set'].max() + 1):
        for k in range(ver['levelCounter'].min(), ver['levelCounter'].max()+1):
            sub_vect = ver[(ver['trial_set'] == j) & (ver['levelCounter'] == k)]
            if len(sub_vect) < 1:
                sub_vect = pd.DataFrame([["no start", k, j]], columns=['row_start', 'levelCounter', 'trial_set'])
            START = pd.concat([START, sub_vect.head(1)])
    # Reset index for the final START dataframe
    START.reset_index(drop=True, inplace=True)
    # Now you have the 'START' dataframe containing the start positions for each level and set
    return START


###########################################
# Initialize edit_df as an empty DataFrame
edit_df = pd.DataFrame()

for set_val in range(1, 4):
    for lvl in range(0, 36):
        vr_start = start_df[(start_df['trial_set'] == set_val) & (start_df['levelCounter'] == lvl)]['row_start']
        vr_close = close_df[(close_df['trial_set'] == set_val) & (close_df['levelCounter'] == lvl)]['indx']
        
        if not vr_start.empty and not vr_close.empty:
            start_index = vr_start.iloc[0]
            close_index = vr_close.iloc[0]
            
            if isinstance(start_index, int) or isinstance(close_index, int):
                a = f_ptcp_df.iloc[start_index:close_index, :]
                # Perform your analysis or processing on 'a' here
                edit_df = pd.concat([edit_df, a], ignore_index=True)  # Concatenate 'a' to edit_df
            else:
                print("Warning: Invalid indices - start_index and close_index must be integers")
                continue
        else:
            print("Warning: Empty indices for set_val =", set_val, "and lvl =", lvl)


        
###########################################
# Correct the press button. Condition. 

def find_ball_position_changes(data):
    B = pd.DataFrame()
    for set_val in range(1, 4):
        for lvl in range(0, 36):
            meanwhile = data[(data['levelCounter'] == lvl) & (data['trial_set'] == set_val)]
            if meanwhile['buttonCurrentlyPressed'].nunique() >= 2 and data[(data['levelCounter'] == lvl - 1) & (data['trial_set'] == set_val)]['buttonCurrentlyPressed'].nunique() < 2:
                print(f"Button pressed in lvl {lvl} - set {set_val}. Need to go for following change of ball position.")
                A = np.zeros(len(meanwhile))
                A2 = np.zeros(len(meanwhile))
                A3 = np.zeros(len(meanwhile))
                for r in range(1, len(meanwhile)):
                        A[r] = (meanwhile.iloc[r - 1]['buttonHasBeenPressed'] == "TEMPLATE_IS_ACTIVE") & (meanwhile.iloc[r]['buttonHasBeenPressed'] == 'AFTER_TEMPLATE_IS_ACTIVE')
                    #else:
                    #    A2[r] = (meanwhile.iloc[r - 1]['buttonHasBeenPressed'] == "TEMPLATE_IS_ACTIVE") & #(meanwhile.iloc[r]['buttonHasBeenPressed'] == 'AFTER_TEMPLATE_IS_ACTIVE')
                    #    if sum(A2) >= 1:
                    #        A3[r] = meanwhile.iloc[r - 1]['redBallPosition'] != meanwhile.iloc[r]['redBallPosition']
                    #        break
                #A = np.concatenate(([0], A3))
                #A2 = np.zeros(0)
                #A3 = np.zeros(0)
                '''
                Line 291305 first change in ball position. 
                Line 291755 strart the true value for button has been press
                Line 291809 stops the true value for button has been press 
                Line 291809 stops the level 
                '''
            else:
                print(f"Normal way to Start lvl in lvl {lvl} - set {set_val}")
                A = np.zeros(len(meanwhile))
                for r in range(1, len(meanwhile)):
                    A[r] = meanwhile.iloc[r - 1]['redBallPosition'] != meanwhile.iloc[r]['redBallPosition']

            B = pd.concat([B, pd.DataFrame(A)], ignore_index=True)
    # Find the rows where the ball position changes (A == 1)
    indx = np.where(B.to_numpy()[:, 0] == 1)[0]
    # Create a dataframe 'ver' merging row_start, levelCounter, and set
    ver = pd.DataFrame({'row_start': indx, 'levelCounter': data.iloc[indx]['levelCounter'].astype(int), 'trial_set': data.iloc[indx]['trial_set'].astype(int)})
    # Merge level, set, and start into one dataframe 'START'
    START = pd.DataFrame()
    for j in range(data['trial_set'].min(), data['trial_set'].max() + 1):
        for k in range(ver['levelCounter'].min(), ver['levelCounter'].max()+1):
            sub_vect = ver[(ver['trial_set'] == j) & (ver['levelCounter'] == k)]
            if len(sub_vect) < 1:
                sub_vect = pd.DataFrame([["no start", k, j]], columns=['row_start', 'levelCounter', 'trial_set'])
            START = pd.concat([START, sub_vect.head(1)])
    # Reset index for the final START dataframe
    START.reset_index(drop=True, inplace=True)
    # Now you have the 'START' dataframe containing the start positions for each level and set
    return START

### second try to unique feedbacktype
def get_one_feedback_per_trail(dataf):
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    crazy_unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique().reset_index()
    count=0

    # Split the values in the 'feedbackType' column
    split_feedback = crazy_unique_feedback_types['feedbackType'].apply(pd.Series)

    # Rename the columns
    split_feedback.columns = [f'{i + 1}st_term' for i in range(split_feedback.shape[1])]

    # Concatenate the split columns with the original DataFrame
    result_df = pd.concat([crazy_unique_feedback_types.drop(columns=['feedbackType']), split_feedback], axis=1)

    return result_df 

----

def get_one_feedback_per_trail(dataf):
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()
    count=0

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
                    count = +1 
            if last_element is not None and feedback_types[0] == last_element :
                feedback_types = feedback_types[1:]
        elif level_counter == 0  and feedback_types.size > 1:
            feedback_types = feedback_types[feedback_types != 'none']
        unique_feedback_types[index] = feedback_types
        feedback_df = pd.DataFrame({'unique_feedbackTypes': unique_feedback_types})

    return feedback_df 



