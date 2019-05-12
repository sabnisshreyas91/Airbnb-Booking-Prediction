import zipfile
import os
import config

root = config.PROJECT_HOME 
data = config.DATA_FOLDER 
uncompressed_data = config.UNCOMPRESSED_DATA
zip_file_name = config.ZIP_FILE_NAME

data_folder_path = root+"\\"+data
zip_file_path = data_folder_path+"\\"+zip_file_name
uncompressed_folder_path = data_folder_path+"\\"+uncompressed_data

zip_folder_name = str.replace(zip_file_name,".zip","")

zip_ref = zipfile.ZipFile(zip_file_path, 'r')
zip_ref.extractall(uncompressed_folder_path)
zip_ref.close()

uncomp_folder = uncompressed_folder_path+"\\"+zip_folder_name+"\\"
target_folder = uncompressed_folder_path+"\\"

for file in os.listdir(uncomp_folder):
    os.rename(uncomp_folder+file,target_folder+file)

os.rmdir(uncomp_folder)

