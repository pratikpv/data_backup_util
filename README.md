# Data Backup utility script

Earlier i was using some commercial software to backup my data. But many times it was crashing. Out of frustration, i created my own script to backup my data. It has very essential features that serves my needs. (I may add new features if someone needs)

This script creates backup archive in .zip compressed format for intended file or folder. Backup archive is saved at given path. User can choose number of copies to maintain for the backup. All 3 of these parameters are passed using a config file.

## Format of the config file.

src_path=/home/pratik/data/docs
dst_path=/home/pratik/data/backup
num_copy=4

where, 
src_path is folder or file which needs to be backup
dst_path is folder where backup would be created. Of this location does not exist, the script would create it
num_copy: these many number of backups would be maintained. If the script is run more than num_copy times then older backup would get deleted. This is to make sure the backup does not fill the storage.

## How to run the script:

python3 backup_data.py <config_file>

## How to automate:

For linux use crontab and for windows use ‘task scheduler’ to run the script automatically as per your need.

To backup more than one file/folder location, use another config file

