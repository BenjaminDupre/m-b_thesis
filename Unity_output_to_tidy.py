
import dropbox

# Set up the Dropbox API client
ACCES_TOKEN = 'sl.BhCAwKe_oYAIwj13pA4sky3V_ydOuzO-OOX1ZZ05K68fc3HzcdnEB22_-E8IKmMRVOMEQ7fIvBiKhE6yq_Ta96_UU6JRYMgGADa-fg7UBP2Cu3a34Ef2f8RWK8w1psyl7bVjzJ_SC3-C'
dbx = dropbox.Dropbox(ACCES_TOKEN)

# Specify the path to the file you want to access

FOLDER_PATH='/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'


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
                print("Folder path:", folder_path)
                return list_folders
    except dropbox.exceptions.HttpError as err:
        print(f"Error listing folder: {err}")

'''creat function to get three folders from path'''

#response=dbx.files_list_folder(list_folders[1])

#response.entries
get_partc_fold(FOLDER_PATH)
get_partc_fold(list_folders[2])
get_partc_fold(list_folders[3])
