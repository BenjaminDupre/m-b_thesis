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
ACCESS_TOKEN = 'sl.Bh5QQ3X4EJGBF1YxhhHWK1vRMoQHWKd2GkUQ8LuSGm9IVJ6Svh'\
    '3WPCbOtNUp74C8Y20V9h38e9DLbYubTw6d51k8_cL4H8vCkWf1dBTBmW19sZqBuwTVXcZU2FstfMTXA-DqEOvWl9oK'
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


def main():
    """
    Main Function

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

    return g_ptcp_path, g_ptcp_names, ptcp_df

########################### Excecution of Main Function ##


if __name__ == '__main__':
    f_ptcp_path, f_ptcp_names, f_ptcp_df = main()
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


##### test to get only one stimuli 
# Remove duplicate feedback types based on the specified conditions
#import pandas as pd

# Assuming you already have the DataFrame 'f_ptcp_df' containing the data

# Group the data and extract unique feedbackType values per participant, set, and levelCounter
unique_feedback_types = f_ptcp_df.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()

# Remove duplicate feedback types based on the specified conditions
for index, feedback_types in unique_feedback_types.items():
    ptcp, set_val, level_counter = index
    if level_counter != 0:
        previous_level_counter = level_counter - 1
        previous_feedback_types = unique_feedback_types.get((ptcp, set_val, previous_level_counter))
        if previous_feedback_types is not None and feedback_types.size>=2:
            # Remove feedback types that are also present in the previous level
            feedback_types = [ft for ft in feedback_types if ft not in previous_feedback_types]           
    elif level_counter == 0 and feedback_types.size>=2:
        feedback_types = feedback_types[np.where(feedback_types != 'none')]

    

    unique_feedback_types[index] = feedback_types

# Print the unique feedbackType values after removing duplicates
for index, feedback_types in unique_feedback_types.items():
    ptcp, set_val, level_counter = index
    print(f"ptcp: {ptcp}, trial_set: {set_val}, levelCounter: {level_counter} - Unique feedbackType values: {feedback_types}")
 