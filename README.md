# Landsat8-download
This python script can automate the work of downloading Landsat 8 
data using Google's gsutil tool and then extract the bz file.

## Prerequisites
You need to have the Google Cloud Storage `gsutil` command line tool 
installed on your laptop or computer. If you are using Windows, the 
installation instruction from Google is [here][]. For MacOS/Linux users, 
the installation instruction is:

1. Enter the following at a command prompt:
```sh
  curl https://sdk.cloud.google.com | bash
 ```
 2. Restart your shell:
 ```sh
  exec -l $SHELL
 ```
 3. Run gcloud init to initialize the gcloud environment:
 ```sh
  gcloud init
 ```
 
 ## Installation 
