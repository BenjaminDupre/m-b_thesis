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
# getting the almost ready file
edit_df=[]
for set_val in range(1, 4):
    for lvl in range(0, 36):
        vr_start = start_df[(start_df['trial_set'] == set_val) & (start_df['levelCounter'] == lvl)]['row_start']
        vr_close = close_df[(close_df['trial_set'] == set_val) & (close_df['levelCounter'] == lvl)]['indx']
        
        if not vr_start.empty and not vr_close.empty:
            start_index = vr_start.iloc[0]  # Get the first index value from the series
            close_index = vr_close.iloc[0]  # Get the first index value from the series
            
            if pd.notna(start_index) and pd.notna(close_index):
                a = f_ptcp_df.iloc[start_index:close_index, :]
                # Perform your analysis or processing on 'a' here
                edit_df.append(a)
            else:
                print("Warning: Invalid indices - start_index >= close_index")
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
