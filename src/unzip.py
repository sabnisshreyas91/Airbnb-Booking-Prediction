import zipfile

root = "D:\\Northwestern\\MSiA\\SQ 2019\\AVC\\Project\\Ideas\\Airbnb-Booking-Prediction\\"
data = "\\data"
uncompressed_data ="\\uncompressed_files"
zip_file_name = "AirBnb.7z"

zip_ref = zipfile.ZipFile(root+data+uncompressed_data+"\\"+zip_file_name, 'r')
zip_ref.extractall(root+data+uncompressed_data)
zip_ref.close()