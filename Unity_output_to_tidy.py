# Import Relevant Library. 
import dropbox
import pandas as pd
import io

# Set up the Dropbox API client
ACCES_TOKEN = 'sl.BhE9Z28Px03DlMr5EmEByZvYkBN58aRUNdg0VACf0SjoVcmYCIP-hoMUGKo9VwVgBD_Yj6hX7Uoy5FTS4pFzGUmbIZGi8rCbBB5PtxnhtONwSrEYmSeuWiG6Dbr9XzsZXb_qFhywBH7U'
dbx = dropbox.Dropbox(ACCES_TOKEN)


# Specify the path to the file you want to access

FOLDER_PATH='/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'

########################### FUNCIONES
def get_partc_fold(fld_path):
    """
    load folder within path given
    removes __MACOSX
    """
    list_folders=[]
    try:
        response = dbx.files_list_folder(fld_path)
        # Iterate over the entries in the root directory
        for entry in response.entries:
            if isinstance(entry, dropbox.files.FolderMetadata):
                # Display the folder path
                folder_path = entry.path_display
                list_folders.append(folder_path)
                #print("Folder path:", folder_path)
        return list_folders
                        
    except dropbox.exceptions.HttpError as err:
        print(f"Error listing folder: {err}")

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
    column_types = ['string', 'float64', 'float64', 'float64',
                'string', 'string', 'string', 'string', 'string',
                'string', 'boolean', 'boolean', 'category',
                'boolean', 'boolean', 'string', 'string',
                'boolean', 'boolean', 'boolean', 'string',
                'boolean', 'string', 'boolean', 'boolean',
                'string', 'string', 'object']
    
    accumulated_data = []  # Accumulate individual CSV data

    for folder in list_sets:
        path= folder + "/everything.csv"
        _, response = dbx.files_download(path)

        csv_data = response.content

        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')),
                      # There is some curruption in the files, so we skip first second
                      header=0, skiprows=133, delimiter=';', 
                      names=column_names, dtype=dict(zip(column_names, column_types))).to_dict('records')


        accumulated_data.extend(df)  # Accumulate the data
    
    # Create a single DataFrame directly from the accumulated data
    combined_df = pd.DataFrame(accumulated_data)

    # Convert 'ECG' column decimal separators from commas to decimal points
    combined_df['ECG'] = combined_df['ECG'].str.replace(',', '.').astype('float32')
    
    # Return the DataFrame or perform additional processing
    return combined_df

# Excecution of Functions. 
list_fold = get_partc_fold(FOLDER_PATH)
list_subfolders= get_partc_fold(list_fold[1])
combined_dfs = read_ptcp_sets_from_dropbox(list_subfolders)

