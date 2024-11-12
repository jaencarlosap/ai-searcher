import os
import shutil

# read the resources folder and get the opus files
def move_opus_files():
    # get the current working directory
    cwd = os.getcwd()
    # get the resources folder
    resources_folder = os.path.join(cwd, 'resources')
    # get the audios folder
    audios_folder = os.path.join(resources_folder, 'audios')
    # create the audios folder if it doesn't exist
    if not os.path.exists(audios_folder):
        os.mkdir(audios_folder)
    # get the opus files
    opus_files = [f for f in os.listdir(resources_folder) if f.endswith('.opus')]
    # move the opus files to the audios folder
    for opus_file in opus_files:
        shutil.move(os.path.join(resources_folder, opus_file), os.path.join(audios_folder, opus_file))
    print('Opus files moved successfully!')


move_opus_files()