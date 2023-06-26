
import dropbox
import pandas as pd
import io

# Set up the Dropbox API client
ACCES_TOKEN = 'sl.BhAGIUhiU_B75wAN7UDWPH4QPQ07elacPi8I9oQiGk2b41S9dhnizTeVmA1j30sTJcPDTyokD_eoFV5VnlZiA5hHpzGr2qX7qBEqUT2aObe9bCpwkA3cwUE7U6JVJplsKRUKT2TzJGJI'
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
list_folders = get_partc_fold(FOLDER_PATH)
list_subfolders= get_partc_fold(list_folders[1])

def read_csv_from_dropbox(path):
    """
    read csv files
    """
    path= path + "/everything.csv"
    _, response = dbx.files_download(path)    
    csv_data = response.content    
    # Read the CSV data into a Pandas DataFrame
    df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')))   
    # Optionally, return the DataFrame or perform additional processing
    return df

df = read_csv_from_dropbox(list_subfolders[0])