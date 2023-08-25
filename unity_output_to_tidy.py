'''
unity_output_to_tidy.py

version 1.1
last updated: July 2023

by Benjamin Dupré
Humboldt-Universität zu Berlin 
Berlin School of Mind and Brain 
10099 Berlin, Germany

Description:
Loading text from Cloud Dropbox Service 
and Loading into a ready to analyse pandas dataframe 
'''
import io
import dropbox
import pandas as pd
import numpy as np


# Set up the Dropbox API client

# Constants

ACCESS_TOKEN = 'sl.Bky2c0pxJS55-2iDyRTriq8_JS_BTk0hz0R2XjQwH0j_tGfuI56h_objIKxaOsLcLHU-Ib7uUKaRADZitRQJxtzfA_rRNeZtRCqHGtcdemvUwtdZ4vQzXGIUNnwV_AoD70Ck59SFcYEIY3zqV6mVx_0'

dbx = dropbox.Dropbox(ACCESS_TOKEN)

# FUNCIONES
# Geting names and folder paths.

folder_names = []

def get_fold(fld_path):
    """
    retrieves folder paths and 
    names from a given path in
    the Dropbox service. It iterates 
    over the entries in the specified folder,
    identifies subfolders, and stores their
    paths and names in the folder_paths
    and folder_names lists.
    """
    folder_paths = []
    #global folder_names 
    try:
        response = dbx.files_list_folder(fld_path)
        # Iterate over the entries in the root directory
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                # Display the folder path
                folder_path = entry.path_display
                folder_name = entry.name
                folder_paths.append(folder_path)
                folder_names.append(folder_name)
                # print("Folder path:", folder_path)
        return folder_paths, folder_names
    except dropbox.exceptions.HttpError as err:
        print(f"Error listing folder: {err}")

# Getting data_sets for on participant.


def read_ptcp_sets_from_dropbox(path_sets, ptcp_names):
    """
    read csv files
    """
    global folder_names
    column_names = ['time', 'Milliseconds', 'levelCounter', 'correctCounter',
                    'leftHandPosition', 'leftHandRotation', 'rightHandPosition',
                    'rightHandRotation', 'redBallPosition', 'redBallRotation',
                    'leftHandGrab', 'rightHandGrab', 'feedbackType',
                    'leftHandVibration', 'rightHandVibration', 'correctBallPosition',
                    'lastTemplateBallPosition', 'areCalibratingGhostHandsActive',
                    'areGrabbingGhostHandsActive', 'calibrationState',
                    'isCalibrationBlocked', 'grabbingState', 'buttonHasBeenPressed',
                    'buttonCurrentlyPressed', 'headPosition', 'headRotation',
                    'isExplosionTriggered', 'ECG']
    column_types = ['string', 'float32', 'float32', 'float32',
                    'string', 'string', 'string', 'string', 'string',
                    'string', 'boolean', 'boolean', 'category',
                    'boolean', 'boolean', 'string', 'string',
                    'boolean', 'boolean', 'boolean', 'string',
                    'boolean', 'string', 'boolean', 'boolean',
                    'string', 'string', 'object']

    accumulated_data = []  # Accumulate individual CSV data

    for i, folder in enumerate(path_sets):
        pathy = folder + "/everything.csv"
        _, response = dbx.files_download(pathy)
        csv_data = response.content
        # Read the CSV data into a Pandas DataFrame
        df_list = pd.read_csv(io.StringIO(csv_data.decode('utf-8')),
                         # There is some curruption in the files, so we skip first second
                         skiprows=133, delimiter=';',
                         names=column_names, \
                            dtype=dict(zip(column_names, \
                                            column_types))).to_dict('records')

        # Add 'trail_set' column with iteration number and 'ptcp' column
        for record in df_list:
            record['trial_set'] = i + 1
            record['ptcp'] = folder_names[1]

        accumulated_data.extend(df_list)  # Accumulate the data

        # Create a single DataFrame directly from the accumulated data
        combined_df = pd.DataFrame(accumulated_data)

        # Convert 'ECG' column decimal separators from commas to decimal points
        combined_df['ECG'] = combined_df['ECG'].str.replace(
            ',', '.').astype('float32')
        combined_df['time'] = pd.to_datetime(
            combined_df['time'], format='%Y-%m-%d %H:%M:%S.%f')
    # Return the DataFrame or perform additional processing
    return combined_df

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

        unique_feedback_types[index] = feedback_types
    return unique_feedback_types 

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


def main():
    """
    Main Data Refinement Pipeline
    This function coordinates a sequence of modules to efficiently convert raw data into an analysis-ready format 
    """
    # FIXED: Specify the path to the file you want to access
    path = '/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/' \
    'P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'

    # 1.Get participant folders and names
    folder_path, folder_names = get_fold(path)
    # 2.Get Sets folders and names for ptcpt
    g_ptcp_path, g_ptcp_names = get_fold(folder_path[1])

    # 3.Read participant datasets from Dropbox into DF.
    ptcp_df = read_ptcp_sets_from_dropbox(g_ptcp_path,g_ptcp_names)

    # 4. Find Trials Starts  (when ball changes first position)
    start_df = find_ball_position_changes(ptcp_df)
    # 5. Find Trials Closure (when level counter changes)
    close_df = creating_close_trial(ptcp_df) 
    # 6.  Meging Start and Close. 
    merged_df = pd.merge(close_df, start_df, on=['levelCounter', 'trial_set'], how='left')

    return g_ptcp_path, g_ptcp_names, ptcp_df, start_df , close_df, merged_df

########################### Excecution of Main Function ##


if __name__ == '__main__':
    f_ptcp_path, f_ptcp_names, f_ptcp_df,start_df, close_df = main()
    


##### test to get only one stimuli 
# Remove duplicate feedback types based on the specified conditions
# Group the data and extract unique feedbackType values per participant, set, and levelCounter
unique_feedback_types = f_ptcp_df.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()
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
    elif level_counter == 0 and feedback_types.size >1:
        feedback_types = feedback_types[feedback_types != 'none']
    unique_feedback_types[index] = feedback_types



for index, feedback_types in unique_feedback_types.items():
    ptcp, set_val, level_counter = index
    print(f"ptcp: {ptcp}, trial_set: {set_val}, levelCounter: {level_counter} - Unique feedbackType values: {feedback_types}")

###### Test to Get the start and end of the trails. 



# Replace 'all_data' with your actual DataFrame containing the data
#all_data =    Replace this line with your actual data
result = find_ball_position_changes(f_ptcp_df)



'''
########################### Testing Results.##
    # Group the data and extract unique feedbackType values per ptcp, set, and levelCounter
    unique_feedback_types = f_ptcp_df.groupby(
    ['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()
    # Print the unique feedbackType values
    for index, feedback_types in unique_feedback_types.items():
        ptcp, set_val, level_counter = index
        print(f"ptcp: {ptcp}, \
               trial_set: {set_val}, \
                 levelCounter: {level_counter} - Unique feedbackType values: {feedback_types}")
'''
 
