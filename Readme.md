# Dropbox Downloader

Small Python script which downloads a shared folder (shared URL) from Dropbox. 
The download script is necessary if the folder contains too much content to download a zip file and if you 
do not have enough space in your own Dropbox left to add the content to your personal dropbox. 
 
The script uses `asyncio` and `aiohttp` to make parallel downloads. The maximum number of concurrent downloads is 
limited by a semaphore. The default limit is 5.
 
The script was modified from the original to use `selenium` and `PhantomJS` in order to run javascript on the
initial Dropbox page to generate the links needed for downloading.  Otherwise, the links are not present.
When running, there is a warning saying that use of `PhantomJS` has been depreciated.

## How to use the Script
 
 1. Clone the repository via `git clone git@github.com:dpdornseifer/dropbox_download.git`
 2. Install the requirements specified in `requirements.txt` via `pip install -r requirements.txt`
 3. Adjust the constants `DROPBOX_URL` and `DESTINATION_FOLDER` in the script to match your requirements
 4. Run the script `python dropbox_download.py`. You'll see a progress bar telling you the total number of files in that folder and how much already has been downloaded.  


Folders are downloaded as zip files, but without extension "zip".  So and additional script must be run to
convert these to zip and unpack them.  This script is named "fixzip.py".
 

