import zipfile
import os

root = "D:\\Northwestern\\MSiA\\SQ 2019\\AVC\\Project\\Ideas\\Airbnb-Booking-Prediction\\"
data = "\\data"
uncompressed_data ="\\uncompressed_files"
zip_file_name = "AirBnb.zip"

zip_folder_name = str.replace(zip_file_name,".zip","")

zip_ref = zipfile.ZipFile(root+data+"\\"+zip_file_name, 'r')
zip_ref.extractall(root+data+uncompressed_data)
zip_ref.close()

uncomp_folder = root+data+uncompressed_data+"\\"+zip_folder_name+"\\"
target_folder = root+data+uncompressed_data+"\\"

for file in os.listdir(uncomp_folder):
    os.rename(uncomp_folder+file,target_folder+file)

os.rmdir(uncomp_folder)
