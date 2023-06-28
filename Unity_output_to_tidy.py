# Import Relevant Library. 
import dropbox
import pandas as pd
import io

# Set up the Dropbox API client

# Constants
ACCESS_TOKEN = 'sl.BhJy-0WNKzGdm2lLmgtcs5uvCMp_YP8TGl14fMi4lSBOJXuogOl6vz_lraPVXjy6VPuvL1bBaU6CPBOJgxwfIduZc1bNW9IVov0E4BHGCIuVnsrf2IaVf4DoKiLJnRwlcIeY9j7lfZmI'

dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Specify the path to the file you want to access

FOLDER_PATH='/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'

########################### FUNCIONES

# Geting names and folder paths. 
def get_partc_fold(fld_path):
    """
    Load folders within the given path and remove __MACOSX.
    """
    list_folders = []
    list_names = []
    try:
        response = dbx.files_list_folder(fld_path)
        # Iterate over the entries in the root directory
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                # Display the folder path
                folder_path = entry.path_display
                folder_name = entry.name
                list_folders.append(folder_path)
                list_names.append(folder_name)
                #print("Folder path:", folder_path)
        return list_folders, list_names
    except dropbox.exceptions.HttpError as err:
        print(f"Error listing folder: {err}")

# Getting data_sets for on participant.

def read_ptcp_sets_from_dropbox(list_sets):
    """
    read csv files
    """
    
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
    column_types = ['string','integer', 'integer', 'integer',
                'string', 'string', 'string', 'string', 'string',
                'string', 'boolean', 'boolean', 'category',
                'boolean', 'boolean', 'string', 'string',
                'boolean', 'boolean', 'boolean', 'string',
                'boolean', 'string', 'boolean', 'boolean',
                'string', 'string', 'object']
    
    accumulated_data = []  # Accumulate individual CSV data

    for i, folder in enumerate(list_sets):
        path= folder + "/everything.csv"
        _, response = dbx.files_download(path)

        csv_data = response.content

        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')),
                      # There is some curruption in the files, so we skip first second
                      skiprows=133, delimiter=';', 
                      names=column_names, dtype=dict(zip(column_names, column_types))).to_dict('records')
        
        # Add 'trail_set' column with iteration number and 'ptcp' column
        for record in df:
            record['trial_set'] = (i + 1)
            record['ptcp'] = list_names[1]

        accumulated_data.extend(df)  # Accumulate the data
    
        # Create a single DataFrame directly from the accumulated data
        combined_df = pd.DataFrame(accumulated_data)

        # Convert 'ECG' column decimal separators from commas to decimal points
        combined_df['ECG'] = combined_df['ECG'].str.replace(',', '.').astype('float32')
        combined_df['time'] = pd.to_datetime(combined_df['time'], format='%Y-%m-%d %H:%M:%S.%f')
    # Return the DataFrame or perform additional processing
    return combined_df





########################### Excecution of Functions. 
list_fold,list_names = get_partc_fold(FOLDER_PATH)
list_ptcp_fold, list_ptcp_names = get_partc_fold(list_fold[1])
combined_dfs = read_ptcp_sets_from_dropbox(list_ptcp_fold)

