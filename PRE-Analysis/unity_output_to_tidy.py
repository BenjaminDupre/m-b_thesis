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
import sys


# Set up the Dropbox API client

# Constants

ACCESS_TOKEN = 'sl.Bnq-yyhimQqxe-H-mmGyGe4YnWjFGEUDAEzRXCFoeOc9BI9o8Q7rQ3t07YV9bPefftxiJ8RntO2-V1l6ANGPHBVv_NLWvL3DERbVUEOF5X7-3LD12dLY-kKK4l_U10TW1mQUAkgesKxVOdqGR_CGxp4'

dbx = dropbox.Dropbox(ACCESS_TOKEN)

# FUNCIONES
# Geting names and folder paths.
folder_names = []
log_file_path = 'log.txt' # assigning path to logfile. 

# Custom logging function
def log(message):
    # Print to console or GUI
    print(message)
    
    # Write to log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

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
            # Filterin for __MACOSX  dta.    
            filtered_folders_path = [folder for folder in folder_paths if '__MACOSX' not in folder]
            fitered_folders_names = [folder for folder in folder_names if '__MACOSX' not in folder]
        return filtered_folders_path,fitered_folders_names        

    except dropbox.exceptions.HttpError as err:
        log(f"Error listing folder: {err}")

# Getting data_sets for on participant.


def read_ptcp_sets_from_dropbox(path_sets,ptcp_names,p):
    """
    read csv files
    """
    #global ptcp_names
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
                    'string', 'object', 'object', 'category',
                    'object', 'object', 'string', 'string',
                    'object', 'object', 'object', 'string',
                    'object', 'string', 'object', 'object',
                    'string', 'string', 'object']

    accumulated_data = []  # Accumulate individual CSV data
    combined_df = None  # Define combined_df outside the loop

    for i, folder in enumerate(path_sets):
        pathy = folder + "/everything.csv"
        _, response = dbx.files_download(pathy)
        csv_data = response.content
        # Read the CSV data into a Pandas DataFrame
        df_list = pd.read_csv(io.StringIO(csv_data.decode('utf-8')),
                         # There is some curruption in the files, so we skip first second
                         skiprows=266, delimiter=';',
                         names=column_names, \
                            dtype=dict(zip(column_names, \
                                            column_types))).to_dict('records')

        # Add 'trail_set' column with iteration number and 'ptcp' column
        for record in df_list:
            record['trial_set'] = i + 1
            record['ptcp'] = ptcp_names[p]

        accumulated_data.extend(df_list)  # Accumulate the data

        # Create a single DataFrame directly from the accumulated data
        combined_df = pd.DataFrame(accumulated_data)

        # Convert 'ECG' column decimal separators from commas to decimal points
        combined_df['ECG'] = combined_df['ECG'].str.replace(
            ',', '.').astype('float32')
        combined_df['time'] = pd.to_datetime(combined_df['time'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
    # Return the DataFrame or perform additional processing
    return combined_df

def find_ball_position_changes(data):
    min_trial_set = int(data['trial_set'].min())
    max_trial_set = int(data['trial_set'].max())
    min_levelCounter = int(data['levelCounter'].min())
    max_levelCounter = int(data['levelCounter'].max())
    B = pd.DataFrame()
    for set_val in range(min_trial_set, max_trial_set + 1):
        for lvl in range(min_levelCounter, max_levelCounter + 1):
            meanwhile = data[(data['levelCounter'] == lvl) & (data['trial_set'] == set_val)] # TO CHANGE (button pressed just skip)
            if meanwhile['buttonCurrentlyPressed'].nunique() >= 2 and data[(data['levelCounter'] == lvl - 1) & (data['trial_set'] == set_val)]['buttonCurrentlyPressed'].nunique() < 2: #previous level has not a button pressed
                n= f"Button pressed in lvl {lvl} - set {set_val}. Need to go for following change of ball position. No button pressed before"
                log(n)
                A = np.zeros(len(meanwhile))
                #A2 = np.zeros(len(meanwhile))
                #A3 = np.zeros(len(meanwhile))
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
            else:
                n = f"Normal way to Start lvl in lvl {lvl} - set {set_val}"
                log(n)
                A = np.zeros(len(meanwhile))
                for r in range(1, len(meanwhile)):
                    A[r] = meanwhile.iloc[r - 1]['redBallPosition'] != meanwhile.iloc[r]['redBallPosition']
            B = pd.concat([B, pd.DataFrame(A)], ignore_index=True)

    # Check if the size of B is correct 
    if len(B) > len(data):
    # Keep only rows up to and including the last row of data
        B = B.iloc[:len(data)]
    # Find the rows where the ball position changes (B == 1)
    indx = np.where(B.to_numpy()[:, 0] == 1)[0]
    # Create a dataframe 'ver' merging row_start, levelCounter, and set
    ver = pd.DataFrame({'row_start': indx, 'time_start': data.iloc[indx]['time'],
                        'levelCounter':  data.iloc[indx]['levelCounter'].astype(int), 'trial_set': data.iloc[indx]['trial_set'].astype(int)})

    # Merge level, set, and start into one dataframe 'START'
    START = pd.DataFrame()
    for j in range(data['trial_set'].min(), data['trial_set'].max() + 1):
        for k in range(ver['levelCounter'].min(), ver['levelCounter'].max()+1):
            sub_vect = ver[(ver['trial_set'] == j) & (ver['levelCounter'] == k)]
            if len(sub_vect) < 1:
                sub_vect = pd.DataFrame([[99, k, j]], columns=['time','row_start', 'levelCounter', 'trial_set']) ### this is to capture when there is a press button or bug
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
    time_close = data.iloc[row_close]['time']

    # Creating a new DataFrame to store the extracted values
    close_df = pd.DataFrame({
        'row_close': row_close,
        'levelCounter': levelCounter_values,
        'trial_set': trial_set_values,
        'time_close': time_close
    })
    close_df.reset_index(drop=True, inplace=True)
    return close_df 

def get_one_feedback_per_trail(dataf,close_df):
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()

    # Remove duplicate feedback types based on the specified conditions
    for index, feedback_types in unique_feedback_types.items():
        ptcp, set_val, level_counter = index
        feedback_types = feedback_types[np.isin(feedback_types, ['incongruent', 'none', 'congruent'])]
        #print(f'Going Through Level {level_counter} and Set {set_val}')
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
        # WARNING: Last resource condition. Not too Pro but effective 
        if  feedback_types.size > 1:
            log(f'WAS TRIGGERED LAST CASE FEEDBACKTYPE in level {level_counter} and set {set_val}')
            row_n = close_df[(close_df['levelCounter'] == level_counter) & (close_df['trial_set'] == set_val)]['row_close']
            feedback_types = np.asarray(dataf.loc[row_n]['feedbackType'])
        unique_feedback_types[index] = feedback_types
    feedback_df=unique_feedback_types.reset_index()
    feedback_df= pd.DataFrame(feedback_df) 

    return  feedback_df

def get_correct(data):
    A = pd.DataFrame(columns=['trial_set', 'levelCounter', 'correctCounter', 'ptcp', 'Change Flag'])

    for line in range(data.shape[0] - 1):
        if data['correctCounter'][line + 1] != data['correctCounter'][line]:
            A.loc[line, 'Change Flag'] = line  # Use the line number as the flag value
            A.loc[line, 'ptcp'] = data['ptcp'][line]
            A.loc[line, 'trial_set'] = data['trial_set'][line]
            A.loc[line, 'levelCounter'] = data['levelCounter'][line]
            A.loc[line, 'correctCounter'] = data['correctCounter'][line]
    # Optionally, you can reset the index if needed
    correct_df = A.reset_index(drop=True)
    return correct_df

def main():
    """
    Main Data Refinement Pipeline
    This function coordinates a sequence of modules to efficiently convert raw data into an analysis-ready format 
    """
    # FIXED: Specify the path to the file you want to access
    path = '/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/' \
    'P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'

    base=pd.DataFrame()
    open(log_file_path, 'w').close()
    for p in range(0,23):

        log(f'Going thorugh participant {p} :)')
        # 1.Get all participant folders and names
        folder_path, folder_names = get_fold(path)
        # 2.Get specific set subfolders for ptcpt
        g_ptcp_path, g_ptcp_names = get_fold(folder_path[p])
        # 3.Read participant datasets from Dropbox into DF.
        ptcp_df = read_ptcp_sets_from_dropbox(g_ptcp_path,g_ptcp_names,p)
        # 4. Find Trials Starts  (when ball changes first position)
        start_df = find_ball_position_changes(ptcp_df)
        # 5. Find Trials Closure (when level counter changes)
        close_df = creating_close_trial(ptcp_df) 
        # 6. Procces stimulus type ("Congruent", "Incongruent", "None")
        feedback_df = get_one_feedback_per_trail(ptcp_df,close_df)
        # 7 . Creating Correct DF 
        correct_df=get_correct(ptcp_df)
        # 8.  Merging Start and Close. 
        merged_df = pd.merge(close_df, start_df, on=['levelCounter', 'trial_set'], how='left')
        # 9. Creating time (seconds) and 
        merged_df["time_ms"] = (merged_df["time_close"] - merged_df["time_start"]).dt.total_seconds() * 1000        # 10. Addin participants label 
        merged_df["ptcp"] = folder_names[p] # needs to be equal to folders path - change when looping
        # 11. Merge Feedbacktype
        merged_df= pd.merge(merged_df, feedback_df, on=['ptcp','levelCounter', 'trial_set'], how='left')
        # 12. Merge Correct
        merged_df=pd.merge(merged_df, correct_df, on=['ptcp','levelCounter', 'trial_set'], how='left')
        base=pd.concat([merged_df,base],ignore_index=True)
    
    return  base
########################### Excecution of Main Function ##


if __name__ == '__main__':
    merged_df = main()

#merged_df_bugrun.to_csv('clean_merged.csv')    
### NEXT TO ADD CORRECT NUMBER AND ADD MORE ITERATIONS: 

merged_df.to_csv('database.csv')

# To stop redirecting output and revert to the console, you can do this:
sys.stdout = sys.__stdout__
 
#merged_df["Time_close"] - merged_df(["Time_start"])