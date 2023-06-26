### Accesing the files in Google Drive Folders
import dropbox

# Set up the Dropbox API client
ACCES_TOKEN = 'sl.BgsW-iMmoGvliSYK-WjPhheeYNPKwjxgiNmdMuQA6G1HUuysD3YSStMG4qJDMsdGMLi1G9VjI1c4NC8BYiZ8FInQ5yaIRKnt_egzuC87vUE0r9k8-IT6QPokkK3DaeviGFvNvbH1hqVO'
dbx = dropbox.Dropbox(ACCES_TOKEN)

# Specify the path to the file you want to access
#folder_path = ""#'/backups/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'

FOLDER_PATH='/My Mac (glaroam2-185-117.wireless.gla.ac.uk)/Documents/Research MaxPlank/P1_propioception/Data_Wrangling/Matlab Analysis/Data_Wrangling'
#response = dbx.files_list_folder(folder_path)

try:
    response = dbx.files_list_folder(FOLDER_PATH)
    # Iterate over the entries in the root directory
    for entry in response.entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            # Display the folder path
            folder_path = entry.path_display
            print("Folder path:", folder_path)
except dropbox.exceptions.HttpError as err:
    print(f"Error listing folder: {err}")
