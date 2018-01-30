import os
import zipfile
import shutil


# set the following to the directory containing the data
data_dir = "db_data"

def is_zip_file(name):
    # return true if file is zip file.  This will need to be customized
    return name.startswith("YutaMouse")
        
def unzip_files():
    for name in os.listdir(data_dir):
        if is_zip_file(name):
            name_path = os.path.join(data_dir, name)
            zip_path = name_path + ".zip"
            shutil.move(name_path, zip_path)
            with zipfile.ZipFile(zip_path,"r") as zip_ref:
                zip_ref.extractall(name_path)


unzip_files()
