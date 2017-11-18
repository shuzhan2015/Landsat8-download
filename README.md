# Landsat8-download
This python script can automate the work of downloading Landsat 8 data
from Google Cloud Storage using Google's gsutil tool and then extract the bz file.
You can read more about the Google Cloud Storage public datasets project for [Landsat Data][]. 

## Prerequisites
You need to have Ptyhon 2.7 installed. You also need to have the Google Cloud Storage `gsutil` command line tool 
installed on your laptop or computer. If you are using Windows, the 
installation instruction from Google is [here][]. For MacOS/Linux users, 
the installation instruction is:

 1. Enter the following at a command prompt:
 ```sh
  $ curl https://sdk.cloud.google.com | bash
 ```
 2. Restart your shell:
 ```sh
  $ exec -l $SHELL
 ```
 3. Run gcloud init to initialize the gcloud environment:
 ```sh
  $ gcloud init
 ```
 
 ## Installation 
 Clone the repository from github. For example, we clone Landsat8-download to $HOME/Landsat8-download:
 ```sh
  $ cd $HOME
  $ git clone https://github.com/shuzhan2015/Landsat8-download.git
 ```

 ## Usage 
 Once you clone the repository, `cd` to the Landsat8-download directory:
 ```sh
  $ cd $HOME/Landsat8-download
 ```
 You can run the python script by passing arguments to it. This python script can take different forms
 of arguments combinations. 
 
 The script takes three arguments, which are the path, row and the date of the data you want to download.
 The date could be in the format yyyymmdd, yyyyjjj, yymmdd, yyjjj, or mmdd. So, you could run the script by
 passing the three arguments like this:
 ```sh
  $ ./download_landsat8.py --path 22 --row 39 --date 20170401
 ```
 Or, simply like this:
 ```sh
  $ ./download_landsat8.py -p 22 -r 39 -d 20170401
 ```
  Or, If the date argument is omitted, then the latest date available will be downloaded:
 ```sh
  $ ./download_landsat8.py -p 22 -r 39
 ```
  Or, you can also specify the path and row in the config file. Change the path and row in 
  config file, do not put a zero before the path and row number: 
 ```sh
  $ vim config
  $ ./download_landsat8.py -d 20170401
 ```
  The downloaded file is in a compressed bz and tar format. The script will automatically 
  unzip the bz file and untar the tar file. It will also create the corresponding directory 
  for the unzipped files and move the files to this directory. 
  
  <!--refs-->
  [here]: https://cloud.google.com/storage/docs/gsutil_install#windows
  [Landsat Data]: https://cloud.google.com/storage/docs/public-datasets/landsat 
